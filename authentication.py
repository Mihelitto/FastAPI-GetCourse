import hashlib
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import config
import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def decode_token(token):
    user = jwt.decode(token, config.secret_token_key, algorithms=["HS256"])
    return db.session.query(
        db.User.id,
        db.User.username,
        db.User.secret_key
    ).filter(
        db.User.username == user["username"],
        db.User.id == user["id"]
    ).first()


def create_token(user):
    return jwt.encode(
        {"id": user[0], "username": user[1]},
        config.secret_token_key,
        algorithm="HS256"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
