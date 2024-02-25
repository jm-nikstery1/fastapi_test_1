'''routes/events - 이벤트 생성, 변경, 삭제 등의 처리를 위한 라우트'''
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

이벤트 라우트 구현 - 여기서 이벤트는 프로그래밍의 이벤트 아니라 - 이벤트 사건 으로 생각하면 됨 - 
모든 이벤트를 추출하거나 - 특정 ID의 이벤트만 추출하거나 하는식
'''

'''
이벤트 라우트 정의
'''
from fastapi import APIRouter, Body, HTTPException, status, Depends, Request
from models.events import Event, EventUpdate  #터미널에서 main.py로 실행하면 이렇게 위치를 지정해야함
from typing import List

from sqlmodel import select   # 전체 이벤트 조회 - get 라우트 사용

from beanie import PydanticObjectId
from database.connection import Database

'''
이벤트 라우트 변경
'''
from auth.authenticate import authenticate


event_router = APIRouter(
    tags=["Events"]
)

event_database = Database(Event)


'''
모든 이벤트를 추출하거나 특정 ID의 이벤트만 추출하는 라우트
'''
@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events

@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist -몽고DB- 특정 ID의 이벤트만 추출하는 라우트에서 해당 ID의 이벤트가 없다"
        )

    return event


'''
이벤트 생성 및 삭제 라우트를 정의
첫번째 라우트는 이벤트 생성
두번째 데이터베이스에 있는 단일 이벤트 삭제, 
세번째는 전체 이벤트 삭제

이벤트 라우트 변경함 - POST, PUT, DELETE 라우트 함수에 의존성 주입 
- 홈페이지 / docs에 보면 POST, PUT, DELETE 옆에 자물쇠가 생김 
'''
@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user

    await event_database.save(body)
    return {
        "message" : "Event created successfully - 이벤트 생성 성공 - 몽고DB 사용"
    }

@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    '''print(event, "event 확인")
    여기서 id 는 mongodb에 events 의 ID 
    '''
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed - event의 creator와 user가 안맞음 - 소유자 이메일틀림"
        )

    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist - 몽고 DB - PUT - UPDATE 하려는 id 없음"
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist - 몽고 DB - delete 하려는 id 없음  "
        )
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed - 소유자가 DELETE 하지 못함- 다른 소유자의 것  "
        )
    event = await event_database.delete(id)

    return {
        "message": "Event deleted successfully. - 몽고 DB - delete 성공 "
    }

