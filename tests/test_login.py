'''
애플리케이션의 각 라우트(GET,POST,PUT...)를 테스트 하는 코드

'''
import httpx
import pytest

'''
사용자 등록 라우트 테스트

사용자 등록 라우트 - pytest.mark.asyncio 데코레이터 추가 - user singup
비동기 테스트 진행 
'''
@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@test.com",
        "password": "testpassword",
    }
    '''
    요청 헤더와 응답을 정의
    '''
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # 응답이 다를수도 있는데?
    test_response = {
        "message": "User created successfully -몽고 DB- 새로운 유저 생성 성공 - 암호화성공"
    }
    # routes / users.py 에서 찾음 - 동일하게 해야함 json으로 비교하니까

    '''
    요청에 대한 예상 응답을 정의
    '''
    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


'''
로그인 라우트 테스트 

로그인 - user singin

참고로 OAuth2 가 적용됨 - 책에서 그 내용을 빼고 Body 부분 - payload 부분에 내용을 빼먹음
'''
@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    # payload 주의 - email이 아니라 username이다
    payload ={
        "username": "testuser@test.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await default_client.post("/user/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"