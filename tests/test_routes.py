'''
데이터베이스 CRUD 라우트 테스트
생성 Create = POST
읽기 Read = GET
업데이트 Update = PATCH(PUT이 많이 사용되는듯)
삭제 Delete = DELETE

HTTP 요청의 Method도 다음과 같이 CRUD에 기반하고 있다.

!! 중요 !!
여기서 에러가 나오는데
pytest-asyncio==0.18.3 이 버젼에 맞게 해야함
'''
import httpx
import pytest

from auth.jwt_handler import create_access_token
from models.events import Event

'''
일반적인 라이블러ㅣ, create_access_token(user) 함수,
이벤트 모델도 불러옴
접속 토큰도 사용해야함
이 픽스처는 module 범위를 갖는다 - 즉 테스트 파일이 실행될 때 한 번만 실행되고 다른 함수가 호출될 때는 실행되지 않음
'''
@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("testuser@test.com")

'''
Event를 데이터베이스에 추가하는 픽스처 만듬
CRUD 라우트 테스트에 대한 사전 테스트를 진행하는데 사용
'''
@pytest.fixture(scope="module")
async def mock_event() -> Event:
    new_event = Event(
        creator="testuser@test.com",
        title="FastAPI test routes - pytest CRUD 라우트 테스트",
        image="이미지 없음",
        description="설명 description 없음",
        tags=["python", "test_route", "테스트"],
        location="google me",
    )

    await Event.insert_one(new_event)

    yield new_event

'''
조회 라우트 테스트
/event 이벤트 라우트의 GET 메서드를 테스트 하는 함수

!! 중요 !!
여기서 에러가 나오는데 
pytest-asyncio==0.18.3 이 버젼에 맞게 해야함 
'''
@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


'''
/event/{id} 라우트 테스트 함수
'''
@pytest.mark.asyncio
async def test_get_evnet(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)

"""
생성 라우트 테스트 
앞서 만든 픽스처를 사용해 접속 토큰을 추출하고 테스트 함수 정의
서버로 전송될 요청 페이로드 생성
요청 페이로드에는 콘텐츠 유형과 인증 헤더가 포함
테스트 응답도 정의되는데 실행되면 실제 결과와 응답이 비교됨
"""
@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "FastAPI test - 생성 라우트 테스트",
        "image": "이미지 없음",
        "description": "설명 없음 - 생성 라우트 테스트중",
        "tags": ["python","fastapi","launch"],
        "location": "Google Me1",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # test_response는 routes / events.py 에 있는 post 함수의 응답이랑 동일해야함
    test_response = {
        "message": "Event created successfully - 이벤트 생성 성공 - 몽고DB 사용"
    }

    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


'''
데이터베이스에 저장된 이벤트 개수를 확인하기 위한 테스트를 작성
이벤트 개수 2개임
'''
@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient) -> None:
    response = await default_client.get("/event/")

    events = response.json()

    assert response.status_code == 200
    assert len(events) == 2
    # 2개가 맞냐? - 맞음 - 테스트용으로 생성한 event 2개

'''
변경 및 삭제 라우트 테스트
UPDATE, DELETE 라우트
(PUT, DELETE)
'''
@pytest.mark.asyncio
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_payload = {
        "title": "Updated FastAPI event - UPDATE 라우트 테스트"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{str(mock_event.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["title"] == "Updated FastAPI event - UPDATE 라우트 테스트"   # 일부러 틀리면 반응다름


'''
삭제 라우트 테스트
DELETE
'''
@pytest.mark.asyncio
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    # test_response는 routes / events.py 에 있는 delete 함수의 응답이랑 동일해야함
    test_response = {
        "message": "Event deleted successfully. - 몽고 DB - delete 성공 "
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response

'''
문서가 실제로 삭제되었는지 확인하는 테스트
'''
@pytest.mark.asyncio
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 404    # id에 관한 문서가 없으니 404 응답코드가 나와야함
    #assert response.json()["creator"] == mock_event.creator
    #assert response.json()["_id"] == str(mock_event.id)