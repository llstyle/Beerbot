from passlib.context import CryptContext

from database import SessionLocal
from models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return password_context.hash(password)

def create_users(username, password):
    with SessionLocal() as sess:

        hashed_password = get_password_hash(password)
        user = User(username=username, hashed_password=hashed_password)

        sess.add(user)
        sess.commit()
        sess.refresh(user)

        return user.username

if __name__ == "__main__":
    password = ''
    username = ''
    while True:
        username = input('Enter your username: ')

        if len(username) < 3:
            print('Email too short')
            continue
        elif len(username) > 20:
            print('Email too large')
            continue
        else:
            print(f'You entered {username}')
            break

    while True:
        password = input('Enter your password: ')

        if len(password) < 8:
            print('Password too short')
            continue
        elif len(password) > 50:
            print('Password too large')
            continue
        else:
            print(f'You entered {password}')
            break
    
    user = create_users(username=username, password=password)

    print(f"You created user with email {user}")
