'''models/users - 사용자 처리용 모델을 정의'''
'''
사용자 모델(user)을 models 폴더의 user.py 파일에 정의
'''
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from beanie import Document, Link
from models.events import Event   # main.py에서 실행할땐 이렇게 해야할듯

class User(Document):
    email: EmailStr
    password: str
    event: Optional[List[Event]]

    class Settings:
        name = "users"

    '''
    사용자 모델을 3개의 필드를 갖는다
    email - 사용자 이메일
    password - 사용자 패스워드
    events - 사용자가 생성한 이벤트, 처음에는 비어있음
    데이터를 어떻게 저장하고 설정하는지 보여주는 샘플 데이터 만들기
    '''
    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@test.com",
                "password": "strong!",
                "events": [],
            }
        }

'''
Token 보안 방식에 맞게 작성
'''
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

