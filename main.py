'''main - 이벤트 플래너 애플리케이션 개발 '''
'''
사용자 처리용 라우트를 정의함 
main.py에 라우트를 등록하고 
애플리케이션 실행을 해봄
'''

'''
애플리케이션이 시작될때 데이터베이스를 생성하도록 함
애플리케이션을 실행하면 데이터베이스가 생성
시작시 conn() 함수를 호출해서 데이터베이스를 생성함 
'''
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database.connection import Settings

from routes.users import user_route
from routes.events import event_router

from fastapi.middleware.cors import CORSMiddleware    # CORS 미들웨어 라이브러리 추가

import uvicorn

app = FastAPI()
settings = Settings()

# 출처 등록 - 허용된 도메인 혹은 IP주소로 사용자가 리소스를 사용가능하게 함
# 즉 API와 도메인이 동일한 경우 또는 API가 허가한 도메인만 리소스에 접근

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 모든 IP 리스소 접근 허용


#라우트 등록
app.include_router(user_route, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

