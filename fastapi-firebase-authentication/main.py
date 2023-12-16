import uvicorn
import firebase_admin
import pyrebase

from fastapi import FastAPI
from firebase_admin import credentials, auth
from config.firebase import firebase_config as config
from models import UserSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

app = FastAPI(
    title="FastAPI Firebase Authentication",
    description="Firebase Authentication with FastAPI",
    docs_url="/",
)


if not firebase_admin._apps:
    cred = credentials.Certificate("config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

firebase = pyrebase.initialize_app(config)


@app.post("/signup")
async def create_an_account(user: UserSchema):
    email = user.email
    password = user.password
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return JSONResponse(
            status_code=201,
            content={
                "message": f"Successfully created an account! {user.uid}",
            }
        )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )


@app.post("/login")
async def login(user: UserSchema):
    email = user.email
    password = user.password
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email,
            password=password
        )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Successfully logged in!",
                "token": user['idToken'],
                "refreshToken": user['refreshToken'],
                "expiresIn": user['expiresIn'],
                "localId": user['localId'],
            }
        )
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password."
        )


@app.post("/ping")
async def validate_token(request: Request):
    headers = request.headers
    jwt_token = headers.get('Authorization').split(' ')[1]
    try:
        user = auth.verify_id_token(jwt_token)
        return JSONResponse(
            status_code=200,
            content={
                "message": "Successfully pinged!",
                "user": user['user_id'],
            }
        )
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid token."
        )


# @app.post("/logout")
# async def logout(request: Request):
#     headers = request.headers
#     jwt_token = headers.get('Authorization').split(' ')[1]
#     try:
#         user = auth.verify_id_token(jwt_token)
#         auth.revoke_refresh_tokens(user['user_id'])
#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "Successfully logged out!",
#             }
#         )
#     except:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid token."
#         )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
