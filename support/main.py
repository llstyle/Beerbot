from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request,UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
import models, crud, schemas, utils
from database import engine, get_db

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils import ACCESS_TOKEN_EXPIRE_MINUTES
import aiofiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="upload"), name="media")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get('/faq_get_all/', response_model=list[schemas.FAQ], response_model_exclude_unset=True)
def home(db: Session = Depends(get_db)):
    return crud.get_faq(db)

@app.get('/faq_get_bot/', response_model=list[schemas.FAQBot], response_model_exclude_unset=True)
def home_bot(db: Session = Depends(get_db)):
    return crud.get_faq(db)

@app.get('/get_faq_children/{id}/', response_model=list[schemas.FAQBot], response_model_exclude_unset=True)
def get_faq_byID(id: int,db: Session = Depends(get_db)):
    return crud.get_faq_children(db, id)

@app.get('/get_faq_byId/{id}/', response_model=schemas.FAQBot, response_model_exclude_unset=True)
def get_faq_byID(id: int,db: Session = Depends(get_db)):
    return crud.get_faq_byId(db, id)

@app.post("/faq_create/", response_model=schemas.FAQ)
def create_faq(faq: schemas.FAQCreate, db: Session = Depends(get_db), current_user: schemas.Users = Depends(utils.get_current_active_user)):
    return crud.create_faq(db=db, item=faq)

@app.put("/update/{id}")
def update_faq(id: int, faq: schemas.FAQUpdate, db: Session = Depends(get_db), current_user: schemas.Users = Depends(utils.get_current_active_user)):
    updated_faq = crud.update_faq(db=db, item=faq, id=id)
    if not updated_faq:
        raise HTTPException(status_code=400, detail="Email already registered")
    return updated_faq

@app.delete("/delete/{id}")
def delete_faq(id: int, db: Session = Depends(get_db), current_user: schemas.Users = Depends(utils.get_current_active_user)):
    deleted_faq = crud.delete_faq(db=db, id=id)
    if not deleted_faq:
        raise HTTPException(status_code=400, detail="Faq doesnt exist")
    return deleted_faq

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.Users)
async def read_users_me(current_user: schemas.Users = Depends(utils.get_current_active_user)):
    return current_user

@app.post("/upload_image/")
async def post_endpoint(in_file: UploadFile=File(...), current_user: schemas.Users = Depends(utils.get_current_active_user)):
    async with aiofiles.open(f'upload/{in_file.filename}', 'wb') as out_file:
        content = await in_file.read()
        await out_file.write(content)  

    return { "link": f"http://127.0.0.1:8000/media/{in_file.filename}" }