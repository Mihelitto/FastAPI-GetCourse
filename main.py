from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import authentication as au
import getcourse_api
import db
from models import NewUser


app = FastAPI()


@app.get("/deals")
def get_deals(deals: dict = Depends(getcourse_api.get_deals)):
    return deals


@app.post("/deals")
def post_deals(deal: dict = Depends(getcourse_api.post_deal)):
    return deal


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.session.query(
        db.User.id,
        db.User.username,
        db.User.hashed_password
    ).filter(db.User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    if not user[2] == au.hash_password(form_data.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    return {
        "access_token": au.create_token(user),
        "token_type": "bearer"
    }


@app.get("/users/me")
async def read_users_me(current_user: tuple = Depends(au.get_current_user)):
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
        new_user = db.User(
            user.username,
            au.hash_password(user.password),
            user.secret_key,
        )
        db.session.add(new_user)
        db.session.commit()
        return {
            "user": new_user.username,
            "user_id": new_user.id,
            "status": "created"
        }
    return {"error": "Password mismatch"}
