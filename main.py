import hashlib
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import config
import getcourse_api
import db
from models import User, NewUser


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str):
    return hashlib.sha1(password.encode('utf-8')).hexdigest()


def decode_token(token):
    user = jwt.decode(token, config.secret_token_key, algorithms=["HS256"])
    print(user)
    return db.session.query(
        db.User.id,
        db.User.username,
    ).filter(db.User.username == user["username"], db.User.id == user["id"]).first()


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


@app.get("/{account_name}/deals")
def get_deals(
        deals: dict = Depends(getcourse_api.get_deals),
        token: str = Depends(oauth2_scheme)
        ):
    return deals, token


@app.post("/{account_name}/deals")
def post_deals(deal: dict = Depends(getcourse_api.post_deal)):
    return deal


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.session.query(db.User.id, db.User.username, db.User.hashed_password)\
        .filter(db.User.username == form_data.username).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    if not user[2] == hash_password(form_data.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    return {
        "access_token": create_token(user),
        "token_type": "bearer"
    }


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users")
async def get_users():
    return db.session.query(
        db.User.id,
        db.User.username,
        db.User.hashed_password
    ).all()


@app.post("/users")
async def post_user(user: NewUser):
    if user.password == user.password_repeat:
        new_user = db.User(user.username, hash_password(user.password), False)
        db.session.add(new_user)
        db.session.commit()
        return {"user": new_user.username, "user_id": new_user.id, "status": "created"}
    return {"error": "Password mismatch"}
