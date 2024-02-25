'''routes/users - 사용자 등록 및 로그인 처리를 위한 라우팅'''
'''
라우트 구현
사용자 / user
로그인 - signin
로그아웃 - signout
등록 - signup

이벤트 / event
생성 - POST
조회 - GET
변경 - PUT
삭제 - DELETE
'''
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from database.connection import Database

from auth.hash_password import HashPassword   #비밀번호 해싱- 암호화 하기


user_route = APIRouter(
    tags=["User"]
)
users = {}

user_database = Database(User)
hash_password = HashPassword()   #비밀번호 암호화

@user_route.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already. - 몽고 DB - 이미 있는 유저 "
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    #print(user.password,"--user.password")
    await user_database.save(user)
    return {
        "message": "User created successfully -몽고 DB- 새로운 유저 생성 성공 - 암호화성공"
    }


'''
OAuth2PasswordRequestForm 클래스를 sign_user_in() 라우트 함수에 주입하여 
해당 함수가 OAuth2 사양을 엄격하게 따르도록 함 
'''
@user_route.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist. - 몽고DB - 로그인 하려는데 유저가 없는 상황"
        )

    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return{
            "access_token" : access_token,
            "token_type" : "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed. - 몽고DB - 로그인 비밀번호 오류"
    )
