JOB_SEEKER_URL = "/api/v1/job-seekers"

async def test_creating_profile_without_login(client , job_seeker_payload) :

    response = await client.post(
        f"{JOB_SEEKER_URL}/create" , json = job_seeker_payload
    )

    assert response.status_code == 401

async def test_create_profile(client, job_seeker_token, job_seeker_payload):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert response.status_code == 201

async def test_get_profile(client , job_seeker_token , job_seeker_payload):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert response.status_code == 201

    response = await client.get(f"{JOB_SEEKER_URL}/me", headers=headers)

    assert response.status_code == 200
    response = response.json()

    assert response['full_name'] == "Arun Kumar"


async def test_delete_profile(client , job_seeker_token , job_seeker_payload):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert response.status_code == 201

    response = await client.delete(f"{JOB_SEEKER_URL}/me", headers=headers)

    assert response.status_code == 204


async def test_user_delete_profile(
    client, job_seeker_token, user_token, job_seeker_payload
):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert response.status_code == 201

    user_headers = {"Authorization": f"Bearer {user_token}"}
    response = await client.delete(f"{JOB_SEEKER_URL}/me", headers=user_headers)

    assert response.status_code == 403


async def test_job_seeker_profile_edit(client, job_seeker_token, job_seeker_payload):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    create_response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert create_response.status_code == 201

    updated_name = "Arun Kumar Updated"
    response = await client.patch(
        f"{JOB_SEEKER_URL}/me",
        json={"full_name": updated_name},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["full_name"] == updated_name


async def test_get_all_job_seekers(
    client, admin_token, job_seeker_token, job_seeker_payload
):
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    create_response = await client.post(
        f"{JOB_SEEKER_URL}/create", json=job_seeker_payload, headers=headers
    )
    assert create_response.status_code == 201

    admin_headers = {"Authorization": f"Bearer {admin_token}"} 

    response = await client.get(
        f"{JOB_SEEKER_URL}/" , headers = admin_headers
    ) 

    assert len(response.json()) == 1 
    assert job_seeker_payload['full_name'] == response.json()[0]['full_name']


async def test_get_job_seeker_by_id(
    client, admin_token, job_seeker_token, job_seeker_payload
):
    job_seeker_headers = {"Authorization": f"Bearer {job_seeker_token}"}
    create_response = await client.post(
        f"{JOB_SEEKER_URL}/create",
        json=job_seeker_payload,
        headers=job_seeker_headers,
    )
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    response = await client.get(
        f"{JOB_SEEKER_URL}/{profile_id}", headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == profile_id
    assert response.json()["full_name"] == job_seeker_payload["full_name"]

