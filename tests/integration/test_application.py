from unittest.mock import AsyncMock

APPLICATION_URL = "/api/v1/application"


async def test_job_seeker_apply(
    client, admin_token, job_seeker_token, job_payload, job_seeker_payload, monkeypatch
):

    monkeypatch.setattr(
        "app.client.email_client.EmailClient.send_email", AsyncMock()
    )

    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    job_response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=admin_headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    profile_response = await client.post(
        "/api/v1/job-seekers/create",
        json=job_seeker_payload,
        headers=headers,
    )
    assert profile_response.status_code == 201

    resume_content = b"%PDF-1.4\nDummy resume content"

    files = {"resume": ("resume.pdf", resume_content, "application/pdf")}

    data = {"job_id": str(job_id)}

    response = await client.post(
        f"{APPLICATION_URL}/apply", data=data, files=files, headers=headers
    )

    assert response.status_code == 201


async def test_get_applications_of_user(
    client, admin_token, job_seeker_token, job_payload, job_seeker_payload
):

    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    job_response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=admin_headers
    )

    assert job_response.status_code == 201

    job_id = job_response.json()["id"]

    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    profile_response = await client.post(
        "/api/v1/job-seekers/create",
        json=job_seeker_payload,
        headers=headers,
    )
    assert profile_response.status_code == 201

    resume_content = b"%PDF-1.4\nDummy resume content"
    files = {"resume": ("resume.pdf", resume_content, "application/pdf")}
    data = {"job_id": str(job_id)}
    response = await client.post(
        f"{APPLICATION_URL}/apply", data=data, files=files, headers=headers
    )

    assert response.status_code == 201

    headers = {"Authorization": f"Bearer {job_seeker_token}"}

    response = await client.get(
        f"{APPLICATION_URL}/me",
        headers=headers,
    )

    assert len(response.json()) == 1
    assert response.json()[0]["job_id"] == int(data["job_id"])


async def _create_application(client, job_creator_token, job_seeker_token, job_payload, job_seeker_payload):
    creator_headers = {"Authorization": f"Bearer {job_creator_token}"}
    job_response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=creator_headers
    )
    assert job_response.status_code == 201 
    job_id = job_response.json()["id"]


    seeker_headers = {"Authorization": f"Bearer {job_seeker_token}"}
    profile_response = await client.post(
        "/api/v1/job-seekers/create",
        json=job_seeker_payload,
        headers=seeker_headers,
    )
    assert profile_response.status_code == 201

    files = {"resume": ("resume.pdf", b"%PDF-1.4\nDummy resume content", "application/pdf")}
    response = await client.post(
        f"{APPLICATION_URL}/apply",
        data={"job_id": str(job_id)},
        files=files,
        headers=seeker_headers,
    )
    assert response.status_code == 201
    return job_id, response.json()["id"]


async def test_delete_application_by_id(
    client, admin_token, job_seeker_token, job_payload, job_seeker_payload
):
    _, application_id = await _create_application(
        client, admin_token, job_seeker_token, job_payload, job_seeker_payload
    )
    headers = {"Authorization": f"Bearer {job_seeker_token}"}

    response = await client.delete(f"{APPLICATION_URL}/{application_id}", headers=headers)

    assert response.status_code == 204



async def test_application_resume_update(
    client, admin_token, job_seeker_token, job_payload, job_seeker_payload
):
    _, application_id = await _create_application(
        client, admin_token, job_seeker_token, job_payload, job_seeker_payload
    )
    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    files = {"resume": ("updated_resume.pdf", b"%PDF-1.4\nUpdated resume", "application/pdf")}

    response = await client.patch(
        f"{APPLICATION_URL}/{application_id}/update_resume",
        files=files,
        headers=headers,
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == application_id
    assert response.json()["resume_filename"] == "updated_resume.pdf"



async def test_get_all_applications(
    client, recruiter_token, job_seeker_token, job_payload, job_seeker_payload
):
    job_id, application_id = await _create_application(
        client, recruiter_token, job_seeker_token, job_payload, job_seeker_payload
    )
    recruiter_headers = {"Authorization": f"Bearer {recruiter_token}"}

    response = await client.get(f"{APPLICATION_URL}/", headers=recruiter_headers)

    assert response.status_code == 200, response.text
    applications = response.json()
    assert len(applications) == 1
    assert applications[0]["id"] == application_id
    assert applications[0]["job_id"] == job_id

    filtered_response = await client.get(
        f"{APPLICATION_URL}/?job_id={job_id}&limit=1&offset=0",
        headers=recruiter_headers,
    )
    assert filtered_response.status_code == 200
    assert [application["id"] for application in filtered_response.json()] == [application_id]


async def test_application_status_update(
    client, recruiter_token, job_seeker_token, job_payload, job_seeker_payload
):
    _, application_id = await _create_application(
        client, recruiter_token, job_seeker_token, job_payload, job_seeker_payload
    )
    recruiter_headers = {"Authorization": f"Bearer {recruiter_token}"}

    response = await client.patch(
        f"{APPLICATION_URL}/{application_id}/status?status=UNDER_REVIEW",
        headers=recruiter_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["status"] == "UNDER_REVIEW"