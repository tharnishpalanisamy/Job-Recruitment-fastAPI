import pytest


APPLICATION_URL = "/api/v1/application"


async def test_job_seeker_apply(
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
