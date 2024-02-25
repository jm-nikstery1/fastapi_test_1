'''
패스워드를 암호화하는 함수가 포함
이 함수는 계정을 등록할 때 또는 로그인 시 패스워드를 비교할 때 사용

passlib 라이브러리로 패스워드를 암호화 하기
bcrypt를 사용해 패스워드를 암호화 함
'''
'''
bcrypt를 사용해 문자열을 해싱할 수 있도록 
CryptContext를 임포트한다
콘택스트는 pwd_context 변수에 저장되며 
이 변수를 사용해 해싱에 필요한 함수들을 호출 

create_hash - 문자열을 해싱한 값을 반환
verify_hash - 일반 텍스트 패스워드와 해싱한 패스워드를 인수로 받아 두 값이 일치하는지 비교한다 - 일치 여부에 따라 불린bool 값을 반환
'''
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
