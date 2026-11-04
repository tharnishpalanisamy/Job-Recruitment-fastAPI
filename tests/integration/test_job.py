JOB_URL = "/api/v1/jobs"


async def test_admin_create_job(client, admin_token):

    headers = {"Authorization": f"Bearer {admin_token}"}
    job_payload = {
        "title": "Software Engineer",
        "description": "We are looking for a passionate Software Engineer to design, develop, and install software solutions. Your responsibilities will include gathering user requirements, defining system functionality, and writing code in various languages.",
        "requirements": "Proficiency in Python or Java, experience with cloud platforms like AWS, and a solid understanding of software development life cycles.",
        "qualification": "Bachelor's degree in Computer Science, Information Technology, or a related field.",
        "experience_min": 2,
        "experience_max": 5,
        "salary_min": 60000,
        "salary_max": 95000,
        "employment_type": "full_time",
        "location": "Remote",
        "vacancies": 3,
    }

    response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=headers
    )

    assert response.status_code == 201


async def test_recruiter_create_job(client, recruiter_token):

    headers = {"Authorization": f"Bearer {recruiter_token}"}
    job_payload = {
        "title": "Software Engineer",
        "description": "We are looking for a passionate Software Engineer to design, develop, and install software solutions. Your responsibilities will include gathering user requirements, defining system functionality, and writing code in various languages.",
        "requirements": "Proficiency in Python or Java, experience with cloud platforms like AWS, and a solid understanding of software development life cycles.",
        "qualification": "Bachelor's degree in Computer Science, Information Technology, or a related field.",
        "experience_min": 2,
        "experience_max": 5,
        "salary_min": 60000,
        "salary_max": 95000,
        "employment_type": "full_time",
        "location": "Remote",
        "vacancies": 3,
    }

    response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=headers
    )

    assert response.status_code == 201


async def test_user_create_job(client, user_token):

    headers = {"Authorization": f"Bearer {user_token}"}
    job_payload = {
        "title": "Software Engineer",
        "description": "We are looking for a passionate Software Engineer to design, develop, and install software solutions. Your responsibilities will include gathering user requirements, defining system functionality, and writing code in various languages.",
        "requirements": "Proficiency in Python or Java, experience with cloud platforms like AWS, and a solid understanding of software development life cycles.",
        "qualification": "Bachelor's degree in Computer Science, Information Technology, or a related field.",
        "experience_min": 2,
        "experience_max": 5,
        "salary_min": 60000,
        "salary_max": 95000,
        "employment_type": "full_time",
        "location": "Remote",
        "vacancies": 3,
    }

    response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=headers
    )

    assert response.status_code == 403


async def test_job_seeker_create_job(client, job_seeker_token):

    headers = {"Authorization": f"Bearer {job_seeker_token}"}
    job_payload = {
        "title": "Software Engineer",
        "description": "We are looking for a passionate Software Engineer to design, develop, and install software solutions. Your responsibilities will include gathering user requirements, defining system functionality, and writing code in various languages.",
        "requirements": "Proficiency in Python or Java, experience with cloud platforms like AWS, and a solid understanding of software development life cycles.",
        "qualification": "Bachelor's degree in Computer Science, Information Technology, or a related field.",
        "experience_min": 2,
        "experience_max": 5,
        "salary_min": 60000,
        "salary_max": 95000,
        "employment_type": "full_time",
        "location": "Remote",
        "vacancies": 3,
    }

    response = await client.post(
        "/api/v1/jobs/create", json=job_payload, headers=headers
    )

    assert response.status_code == 403
