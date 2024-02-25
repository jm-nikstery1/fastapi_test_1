'''
authenticate 의존 라이브러리가 포함되며
인증 및 권한을 위해 라우트에 주입된다
'''
'''
사용자인증 
의존 함수를 구현해서 이벤트 라우트에 주입할것
이 함수는 활성 세션에 존재하는 사용자 정보를 추출하는 단일 창구 역할
'''
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")
'''
Depends - oauth2_scheme을 의존 라이브러리 함수에 주입
OAuth2PasswordBearer - 보안 로직이 존재한다는 것을 애플리케이션에 알림
verify_access_token - jwt_handler에 성의한 토큰 생성 및 검증 함수로, 토큰의 유효성 확인

보안 적용을 위한 의존 라이브러리를 완성 
'''
async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access -error 쪽인데 오타인듯 - token으로 사용자인증하니 에러발생"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]