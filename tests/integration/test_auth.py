# import pytest

# AUTH_URL = "/api/v1/auth"


# @pytest.mark.asyncio
# async def test_signup_success(client):

#     payload = {
#         "username": "testuser",
#         "email": "testuser@gmail.com",
#         "password": "Test@123",
#     }

#     response = await client.post(f"{AUTH_URL}/signup", json=payload)

#     assert response.status_code == 201



# @pytest.mark.asyncio
# async def test_signup_duplicate_email(client):

#     payload = {
#         "username": "testuser",
#         "email": "testuser@gmail.com",
#         "password": "Test@123",
#     }

#     first_response = await client.post(f"{AUTH_URL}/signup", json=payload)

#     second_response = await client.post(f"{AUTH_URL}/signup", json=payload)

#     assert first_response.status_code == 201
#     assert second_response.status_code == 409


# @pytest.mark.asyncio 
# async def test_invalid_email(client) :
#     payload = {
#         'username' : 'test' , 
#         'email' : 'invalid-email' ,
#         'password' : 'password@2005'
#     }

#     response = await client.post(f'{AUTH_URL}/signup' , json=payload) 
#     assert response.status_code == 422 


# @pytest.mark.asyncio
# async def test_invalid_password(client):
#     payload = {
#         "username": "test",
#         "email": "email@gmail.com",
#         "password": "invalid-password",
#     }

#     response = await client.post(f"{AUTH_URL}/signup", json=payload)
#     assert response.status_code == 422


# @pytest.mark.asyncio
# async def test_signup_short_username(client):

#     payload = {"username": "ab", "email": "testuser@gmail.com", "password": "Test@123"}

#     response = await client.post(f"{AUTH_URL}/signup", json=payload)
#     assert response.status_code == 422


# @pytest.mark.asyncio 
# async def test_invalid_login(client) :
#     payload = {
#         'email' : 'dummyuser@gmail.com' , 
#         'password':'Dummy@2123'
#     } 

#     response = await client.post(f"{AUTH_URL}/login", json=payload) 
#     assert response.status_code == 401 


# @pytest.mark.asyncio
# async def test_login_success(client):

#     signup_payload = {
#         "username": "loginuser",
#         "email": "loginuser@gmail.com",
#         "password": "Test@123",
#     }

#     await client.post(f"{AUTH_URL}/signup", json=signup_payload)

#     login_payload = {"email": "loginuser@gmail.com", "password": "Test@123"}

#     response = await client.post(f"{AUTH_URL}/login", json=login_payload)

#     assert response.status_code == 200

#     data = response.json()

#     assert "access_token" in data
#     assert "refresh_token" in data
#     assert "user" in data

#     assert data["user"]["username"] == "loginuser"
#     assert data["user"]["email"] == "loginuser@gmail.com"

#     assert data["access_token"] != ""
#     assert data["refresh_token"] != ""



