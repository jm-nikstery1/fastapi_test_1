import asyncio
import httpx
import pytest

from main import app
from database.connection import Settings
from models.events import Event
from models.users import User

'''
asyncio 모듈은 활성 루프 세션을 만들어서 테스트가 단일 스레드로 실행되도록함
httpx 테스트는 HTTP CRUD 처리를 실행하기 위한 비동기 클라이언트 역할
pytest 라이브러리는 픽스처 정의를 위해 사용, 
애플리케이션 인스턴스 settings 등

테스트 환경 구축 방법 정리
'''

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


'''
Settings 클래스에 새로운 데이터베이스 인스턴스 생성
'''
async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()


'''
클라이언트 픽스처 정의
httpx를 통해 비동기로 실행되는 애플리케이션 인스턴스 반환

데이터베이스를 초기화한 후에 애플리케이션을 AsyncClient로 호출
AsyncClient는 테스트 세션이 끝날 때까지 유지 
테스트 세션이 끝나면  이벤트(Event)와 사용자(User) 컬렉션의 데이터를 모두 삭제하여 
테스트를 실행할 때마다 데이터베이스가 비어있도록 함
'''
@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # 리소스 정리
        await Event.find_all().delete()
        await User.find_all().delete()

