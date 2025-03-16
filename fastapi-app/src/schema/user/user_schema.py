from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., max_length=255, strip_whitespace=True)  # 최대 길이 255, 공백 제거
    password: str = Field(..., min_length=8, max_length=255, strip_whitespace=True)  # 최소 8자, 최대 255자
    password2: str = Field(..., min_length=8, max_length=255, strip_whitespace=True)  # 최소 8자, 최대 255자
    email: EmailStr

    @classmethod
    def validate_passwords_match(cls, values):
        password = values.get("password")
        password2 = values.get("password2")
        if password != password2:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return values
    

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str