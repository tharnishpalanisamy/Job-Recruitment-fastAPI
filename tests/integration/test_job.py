JOB_URL = "/api/v1/jobs"


async def test_admin_create_job(client, admin_token, job_payload):

    headers = {"Authorization": f"Bearer {admin_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    assert response.status_code == 201


async def test_recruiter_create_job(client, recruiter_token, job_payload):

    headers = {"Authorization": f"Bearer {recruiter_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    assert response.status_code == 201


async def test_user_create_job(client, user_token, job_payload):

    headers = {"Authorization": f"Bearer {user_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    assert response.status_code == 403


async def test_job_seeker_create_job(client, job_seeker_token, job_payload):

    headers = {"Authorization": f"Bearer {job_seeker_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    assert response.status_code == 403


async def test_invalid_payload(client, recruiter_token):

    headers = {"Authorization": f"Bearer {recruiter_token}"}
    job_payload = {"invalid": "invalid"}
    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    assert response.status_code == 422


async def test_get_all_jobs(client, admin_token, user_token, job_payload):
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    headers = {"Authorization": f"Bearer {admin_token}"}
    response2 = await client.get(f"{JOB_URL}/", headers=headers)
    response = response.json()
    response2 = response2.json()

    assert any(job["id"] == response["id"] for job in response2)


async def test_job_by_id(client, admin_token, user_token, job_payload):
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = await client.post(f"{JOB_URL}/create", json=job_payload, headers=headers)

    headers = {"Authorization": f"Bearer {admin_token}"}
    response = response.json()
    response2 = await client.get(f"{JOB_URL}/{response['id']}", headers=headers)
    response2 = response2.json()

    assert response["id"] == response2["id"]


async def test_patch_job(client, admin_token, job_payload):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create_response = await client.post(
        f"{JOB_URL}/create", json=job_payload, headers=headers
    )
    assert create_response.status_code == 201
    job_id = create_response.json()["id"]

    response = await client.patch(
        f"{JOB_URL}/{job_id}",
        json={"title": "Senior Software Engineer"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == job_id
    assert response.json()["title"] == "Senior Software Engineer"


async def test_recruiter_cannot_patch_another_users_job(
    client, admin_token, recruiter_token, job_payload
):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    recruiter_headers = {"Authorization": f"Bearer {recruiter_token}"}
    create_response = await client.post(
        f"{JOB_URL}/create", json=job_payload, headers=admin_headers
    )
    job_id = create_response.json()["id"]

    response = await client.patch(
        f"{JOB_URL}/{job_id}",
        json={"title": "Changed by another recruiter"},
        headers=recruiter_headers,
    )

    assert response.status_code == 403


async def test_delete_job(client, admin_token, job_payload):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create_response = await client.post(
        f"{JOB_URL}/create", json=job_payload, headers=headers
    )
    assert create_response.status_code == 201
    job_id = create_response.json()["id"]

    response = await client.delete(f"{JOB_URL}/{job_id}", headers=headers)

    assert response.status_code == 204
    get_response = await client.get(f"{JOB_URL}/{job_id}", headers=headers)
    assert get_response.status_code == 404


async def test_recruiter_cannot_delete_another_users_job(
    client, admin_token, recruiter_token, job_payload
):
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    recruiter_headers = {"Authorization": f"Bearer {recruiter_token}"}
    create_response = await client.post(
        f"{JOB_URL}/create", json=job_payload, headers=admin_headers
    )
    job_id = create_response.json()["id"]

    response = await client.delete(f"{JOB_URL}/{job_id}", headers=recruiter_headers)

    assert response.status_code == 403
