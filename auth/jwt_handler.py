'''
JWT 문자열을 인코딩, 디코딩하는 함수가 포함

'''
import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError   # JWT를 인코딩, 디코딩하는 jose 라이브러리
from database.connection import Settings

settings = Settings()

'''
토큰 생성 함수는 문자열 하나를 받아서 payload 딕셔너리에 전달
payload 딕셔너리는 사용자명과 만료 시간을 포함하며 JWT가 디코딩될 때 반환
expires 값은 생성 시점에서 한 시간 후로 설정

encode() 메서드는 다음과 같이 세 개의 인수를 받으며 payload를 암호화
페이로드 : 값이 저장된 딕셔너리로, 인코딩할 대상
키 : 페이로드를 사인하기 위한 키
알고리즘 : 페이로드를 사인 및 암호화 하는 알고리즘 
'''
def create_access_token(user: str):
    payload ={
        "user": user,
        "expires": time.time() + 3600
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

'''
애플리케이션에 전달된 토큰을 검증하는 함수
token에 있는 expires 를 중심으로 판단하는 메서드
'''
def verify_access_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        expire = data.get("expires")

        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token supplied - token에 expires 정보가 없다"
            )
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired - token의 expires 시간이 만료됨"
            )
        return data

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token - token 자체에 문제가 있음"
        )