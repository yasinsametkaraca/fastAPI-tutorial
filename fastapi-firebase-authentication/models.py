from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@mail.com",
                "password": "example123"
            }
        }