from sqlalchemy.orm import Session

import models, schemas, utils


def get_faq(db: Session):
    return db.query(models.FAQ).filter(models.FAQ.parent_id == None).all()

def get_faq_byId(db: Session, id: int):
    return db.query(models.FAQ).filter(models.FAQ.id == id).first()

def get_faq_children(db: Session, id: int):
    return db.query(models.FAQ).filter(models.FAQ.parent_id == id).all()

def create_faq(db: Session, item: schemas.FAQCreate):
    db_item = models.FAQ(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def update_faq(db: Session, item: schemas.FAQUpdate, id: int):
    db_item = db.query(models.FAQ).filter(models.FAQ.id == id)
    
    if not db_item.first():
        return None
    
    db_item.update(item.dict())

    db.commit()
    
    return db_item.first()

def delete_faq(db: Session, id: int):
    db_item = db.query(models.FAQ).filter(models.FAQ.id == id).first()
    
    if not db_item:
        return None
    
    db.delete(db_item)

    db.commit()
    
    return {"msg": "Faq was deleted"}

def get_user(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user