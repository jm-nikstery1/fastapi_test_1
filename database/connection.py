from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient   #이건 무슨 패키지?
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel

from models.users import User
from models.events import Event

'''
JWT 는 서버와 클라이언트만 아는 비밀키(secret key)를 사용함
Settings 클래스와 환경 파일인 .env 파일에 비밀키를 저장할 SECRET_KEY 변수를 설정

'''
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY : Optional[str] = None
    '''
    데이터베이스를 초기화 하기 위한 라이브러리 임포트
    setting 에 데이터베이스 URL 설정 
    데이터베이스 URL은 Config 서브 클래스에 정의된 환경 파일(env) 읽음
    마지막으로 initialize_database() 메서드를 정의해서 데이터베이스 초기화
    '''
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(), document_models=[Event, User])

    class Config:
        env_file = ".env"

'''
Database 클래스 추가 
클래스는 초기화시 모델을 인수로 받음
'''
class Database:
    def __init__(self, model):
        self.model = model

    '''
    save 메서드 정의
    문서의 인스턴스를 받아서 데이터베이스 인스턴스에 전달
    '''
    async def save(self, document) -> None:
        await document.create()
        return

    '''
    조회 처리 
    데이터베이스 컬렉션에서 단일 레코드를 부르던가 
    전체 레코드를 불러옴 
    '''
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs


    '''
    변경 처리 
    기존 레코드를 변경하는 메서드
    '''
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()
        des_body = {k:v for k,v in des_body.items() if v is not None}
        update_query = {"$set":{
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await  doc.update(update_query)
        return doc

    '''삭제 처리
    해당 레코드 있으면 확인하고 삭제 
    CRUD 처리용 메서드 완료 
    '''
    async def delete(self, id:PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True