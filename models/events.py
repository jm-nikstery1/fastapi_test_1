'''models/events - 이벤트 처리용 모델을 정의'''
'''
각 사용자는 Events 필드를 가지며 여러 개의 이벤트를 저장
제목 - Title
이미지 - Image
설명 - Description
태그 - Tag
위치 - Location
'''
from pydantic import BaseModel
from typing import List

'''
애플리케이션을 데이터베이스와 연동 
SQLModel의 테이블 클래스를 사용
'''
from beanie import Document
from typing import Optional, List

class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    creator: Optional[str]   # creator 필드는 해당 이벤트를 소유한 사용자만 처리를 할수있게 만든 공간

    class Config:
        '''
        Pydantic에서는 이 설정을 통해 모델 정의 시 사용자 정의 클래스나 타입을 필드 타입으로 사용할 수 있게 됩니다
        Pydantic 모델에서 임의의 데이터 유형을 필드 값으로 허용할지 여부를 결정합니다.
        '''
        schema_extra = {
            "example": {
                "title": "FastAPI Launch",
                "image": "image",  # 이미지 없음
                "description": "models _ Events _ Config _ schema_extra 설명",
                "tags": ["python", "fastapi", "launch"],
                "location": "location",
                "creator" : "creator 사용자"
            }
        }

    class Settings:
        name = "events"

'''
update 처리를 위한 pydantic 모델을 추가 
'''
class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Launch",
                "image": "image",  # 이미지 없음
                "description": "models _ Events _ Config _ schema_extra 설명",
                "tags": ["python", "fastapi", "launch"],
                "location": "location"
            }
        }
