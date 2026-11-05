# 1 Project Overview

This project is a backend for a Job Recruitment and Applicant Tracking System. It brings job postings, applicant profiles, and applications into one cetralized place. Recruiters can post vacancies and review applications; job seekers can browse jobs, maintain a profile, apply, and follow application status changes.

The sysetm is built with python, FastAPi, and PostgreSQL. It uses JWT access tokens and rotating refresh tokens for authentication, and sends email notifications for account creation, applications, and status updates. Email is best effort: a missing recipient or delivery failure does not prevent the main operation from completing.

There are four roles in the code: User, Job Seeker, Recruiter, and Admin. Each role is checked at the routes that need access control. A public signup creates a User account; there is no API for changing a user's role. The job seeker profile routes require an account that already has the Job Seeker role.

# 2 Technology Stack

These are the main tools used in the project:

1. Python 3 - application language.
2. FastAPI - API framework.
3. Uvicoen - ASGI server used to run the application (the dependency is named `uvicorn`).
4. PostgreSQL - relational database.
5. SQLAlchemy - ORM and database access layer.
6. Alembic - database migration tool.
7. Pydantic - request validation and response schemas.
8. JWT (JSON Web Tokens) - access-token format.
9. Pytest - unit and integration test framework.
10. HTTPX - asynchronous HTTP client used by integration tests.
11. Jinja2 - renders the HTML email templates.
12. Git and GitHub - source control and project hosting.
13. Swagger UI - interactive API documentation served by FastAPI.

# 3 Project Folder Structure

## 3.1 Directory Structure

```text
project/
|-- alembic/
|   |-- versions/
|-- app/
|   |-- api/v1/
|   |   |-- application/
|   |   |-- auth/
|   |   |-- health/
|   |   |-- job/
|   |   |-- job_seekers/
|   |-- client/
|   |-- core/
|   |-- database/
|   |-- dependencies/
|   |-- exception_handlers/
|   |-- exceptions/
|   |-- middleware/
|   |-- models/
|   |-- repositories/
|   |   |-- implementations/
|   |   |-- protocols/
|   |-- schemas/
|   |-- services/
|   |   |-- implementations/
|   |   |-- protocols/
|   |-- templates/
|   |-- utilities/
|   |-- create_admin.py
|   |-- main.py
|-- logs/
|-- tests/
|   |-- integration/
|   |-- unit/
|-- uploads/
|   |-- resumes/
|-- alembic.ini
|-- pytest.ini
|-- README.md
|-- requirements.txt
```

## 3.2 Directory Description

| Directory | Responsibility |
|---|---|
| `app/api/v1/` | Defines versioned API endpoints, grouped by feature. |
| `app/services/` | Contains application business logic and service protocols. |
| `app/repositories/` | Handles data access through repository protocols and SQLAlchemy implementations. |
| `app/models/` | Defines SQLAlchemy database models. |
| `app/schemas/` | Defines Pydantic request and response schemas. |
| `app/core/` | Contains configuration, security, enums, and logging setup. |
| `app/exceptions/` | Defines custom application exceptions. |
| `app/exception_handlers/` | Maps application exceptions to HTTP responses. |
| `app/database/` | Configures the database connection and declarative base. |
| `app/dependencies/` | Provides dependencies used by API routes. |
| `app/middleware/` | Contains request and response middleware. |
| `app/client/` | Provides clients for external services such as email. |
| `app/templates/` | Stores HTML email templates. |
| `app/utilities/` | Contains shared helpers, including file upload utilities. |
| `alembic/` | Contains database migration configuration and migration versions. |
| `tests/` | Contains unit and integration tests. |
| `uploads/resumes/` | Stores uploaded applicant resumes. |
| `logs/` | Stores application logs. |

# 4 Development Tools

I used PyCharm or Visual Studio Code for editing, PostgreSQL with pgAdmin for database work, Swagger UI for trying API requests, and Git/GitHub for version control.

# 5 User Roles & Authorization

The API has four roles. Route dependencies check the caller's role before allowing access to protected operations. Some actions also check resource ownership in the service layer.

## 5.1 User

A new signup creates a User account. A User can log in and access routes available to authenticated accounts, including browsing jobs. The current API does not include user account detail, user listing, or user role management endpoints.

## 5.2 Job Seeker

A Job Seeker can browse jobs, create and update a profile, apply to jobs, view their own applications, replace a resume while an application is still `APPLIED`, and delete an application that has not moved past `APPLIED`.

After public signup, a `USER` account can create a job seeker profile through the profile creation route. On successful profile creation, the account is assigned the `JOB_SEEKER` role and can use the job seeker profile and application routes. The signup request cannot choose a role; there is no separate role-management endpoint.

## 5.3 Recruiter

A Recruiter can create jobs and manage jobs they created. Recruiters can list applications for their own jobs, review application details, and update application statuses. The status flow is controlled by allowed transitions; selecting an applicant reduces the job's vacancy count, and the job is marked closed when that count reaches zero. The job update schema does not expose a status field, so recruiters cannot manually close or reopen a job through this API. There is no separate resume download route.

## 5.4 Admin

An Admin can create, update, and delete jobs and can list applications across recruiters. The routes also allow admins to request application status updates, but the service currently requires the admin's ID to match the job creator's ID. As a result, an admin cannot update status for a job created by someone else. The API does not currently provide user-management endpoints.

# 6 Database Design 

The application uses PostgreSQL as its relational database management system. SQLAlchemy ORM is used to define database models and manage database operations.

The database consists of five primary tables designed to manage user accounts, job seeker profiles, job vacancies, job applications, and refresh tokens.

# 6.1 Database Tables

1) Users Table (users)

Stores registered user account information and authentication details. 

| Column | Data Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| username | VARCHAR(50) | Not Null |
| email | VARCHAR(255) | Unique, Indexed, Not Null |
| password_hash | VARCHAR(255) | Not Null |
| role | ENUM | Not Null, Default `user` |
| created_at | TIMESTAMP WITH TIME ZONE | Not Null, Default CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP WITH TIME ZONE | Nullable, Default CURRENT_TIMESTAMP |



2) Job Seekers Table (job_seekers) 

Stores professional and personal information of registered job seekers. 

| Column Name | Data Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key, Unique, Not Null |
| full_name | VARCHAR(150) | Not Null |
| phone | VARCHAR(10) | Not Null |
| date_of_birth | DATE | Nullable |
| qualification | VARCHAR(150) | Not Null |
| specialization | VARCHAR(150) | Nullable |
| experience_years | NUMERIC(4,1) | Not Null, Default 0 |
| current_company | VARCHAR(150) | Nullable |
| current_designation | VARCHAR(150) | Nullable |
| current_salary | INTEGER | Not Null |
| created_at | TIMESTAMP WITH TIME ZONE | Not Null |
| updated_at | TIMESTAMP WITH TIME ZONE | Not Nul |


3) Jobs Table (jobs) 

Stores job vacancy details posted by recruiters.

| Column | Data Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| title | VARCHAR(150) | Not Null |
| description | TEXT | Not Null |
| requirements | TEXT | Not Null |
| qualification | VARCHAR(150) | Not Null |
| experience_min | NUMERIC(4,1) | Not Null, Default 0 |
| experience_max | NUMERIC(4,1) | Nullable |
| salary_min | NUMERIC(12,2) | Nullable |
| salary_max | NUMERIC(12,2) | Nullable |
| employment_type | ENUM | Not Null |
| location | VARCHAR(150) | Not Null |
| vacancies | INTEGER | Not Null, Default 1 |
| status | ENUM | Not Null, Default OPEN |
| created_by | INTEGER | Foreign Key, Not Null |
| created_at | TIMESTAMP WITH TIME ZONE | Not Null |
| updated_at | TIMESTAMP WITH TIME ZONE | Not Null |


4) Applications Table (applications) 

Stores job applications submitted by job seekers, including resume information and application status.

| Column | Data Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| job_seeker_id | INTEGER | Foreign Key, Not Null |
| job_id | INTEGER | Foreign Key, Not Null |
| resume_filename | VARCHAR(255) | Not Null |
| resume_path | VARCHAR(500) | Not Null |
| status | ENUM | Not Null, Default APPLIED |
| applied_at | TIMESTAMP WITH TIME ZONE | Not Null |
| updated_at | TIMESTAMP WITH TIME ZONE | Not Null |


Application status values are `APPLIED`, `UNDER_REVIEW`, `SHORTLISTED`, `REJECTED`, and `SELECTED`. A unique constraint prevents a job seeker from applying to the same job twice.

5) Refresh Tokens Table (refresh_tokens)

Stores hashed refresh tokens, their expiry and revocation times, and the link to a replacement token when a token is rotated.

| Column | Data Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key, Not Null |
| token_hash | VARCHAR(64) | Unique, Not Null |
| expires_at | TIMESTAMP WITH TIME ZONE | Not Null |
| revoked_at | TIMESTAMP WITH TIME ZONE | Nullable |
| replaced_by_id | INTEGER | Self-referencing Foreign Key, Nullable |
| created_at | TIMESTAMP WITH TIME ZONE | Not Null |



# 6.2 Database Relationships 

| Relationship | Type | Description |
|---|---|---|
| Users -> Job Seekers | One-to-One | A user can have one job seeker profile. |
| Users -> Jobs | One-to-Many | A recruiter can create multiple job vacancies. |
| Users -> Refresh Tokens | One-to-Many | A user can have multiple refresh tokens. |
| Job Seekers -> Applications | One-to-Many | A job seeker can submit multiple applications. |
| Jobs -> Applications | One-to-Many | A job vacancy can receive multiple applications. |
| Refresh Tokens -> Refresh Tokens | Self-referencing | A refresh token can reference its replacement token. |


# 7 API Documentation

All application routes are mounted under `/api/v1`. FastAPI serves Swagger UI at `/docs`, ReDoc at `/redoc`, and the OpenAPI document at `/openapi.json`.

## 7.1 Health

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/v1/health/` | Public | Liveness check |
| GET | `/api/v1/health/ready` | Public | Checks database readiness |

## 7.2 Authentication

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/v1/auth/signup` | Public | Register a `USER` account |
| POST | `/api/v1/auth/login` | Public | Authenticate and return access and refresh tokens |
| POST | `/api/v1/auth/refresh` | Refresh token supplied in request body | Rotate refresh token and issue a new access token |
| POST | `/api/v1/auth/logout` | Refresh token supplied in request body | Revoke the supplied refresh token |

Signup accepts `username`, `email`, and `password`. The request does not allow a caller to choose an account role.

## 7.3 Job seeker profiles

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/v1/job-seekers/create` | Account with `JOB_SEEKER` role | Create profile |
| GET | `/api/v1/job-seekers/me` | Job seeker | Get own profile |
| PATCH | `/api/v1/job-seekers/me` | Job seeker | Update own profile |
| DELETE | `/api/v1/job-seekers/me` | Job seeker | Delete own profile |
| GET | `/api/v1/job-seekers/` | Recruiter or admin | Search profiles with filters and pagination |
| GET | `/api/v1/job-seekers/{job_seeker_id}` | Recruiter or admin | Get a profile by ID |

The profile creation route is available to accounts with the `USER` role and assigns `JOB_SEEKER` after creating the profile. Other job seeker profile routes require the resulting `JOB_SEEKER` role.

## 7.4 Jobs

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/v1/jobs/create` | Recruiter or admin | Create a job |
| GET | `/api/v1/jobs/` | Authenticated | Search jobs with filters and pagination |
| GET | `/api/v1/jobs/{job_id}` | Authenticated | Get job details |
| PATCH | `/api/v1/jobs/{job_id}` | Recruiter or admin; recruiters may edit their own jobs | Update a job |
| DELETE | `/api/v1/jobs/{job_id}` | Recruiter or admin; recruiters may delete their own jobs | Delete a job |

## 7.5 Applications

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/v1/application/apply` | Job seeker | Apply using multipart form fields `job_id` and `resume` |
| GET | `/api/v1/application/me` | Job seeker | List own applications |
| GET | `/api/v1/application/` | Recruiter or admin | List applications; recruiters see applications for their jobs |
| GET | `/api/v1/application/{application_id}` | Job seeker, recruiter, or admin | Get application details, subject to ownership checks for job seekers and recruiters |
| DELETE | `/api/v1/application/{application_id}` | Job seeker, recruiter, or admin | Delete an application, subject to role and ownership rules |
| PATCH | `/api/v1/application/{application_id}/update_resume` | Job seeker | Replace resume while application is still `APPLIED` |
| PATCH | `/api/v1/application/{application_id}/status?status={status}` | Recruiter or admin | Update status using allowed transition rules; service also requires the caller to have created the job |

There are no user-management CRUD routes or resume-download route in the current API. Application responses differ by endpoint; the detailed recruiter/admin list response includes the stored resume path. Recruiters are restricted to their own jobs. Although the status route accepts admins, the service checks that the caller created the job, so an admin cannot update status on another user's job.


# 8. Authentication Flow

A user signs up with a username, email address, and password. The password is hashed before it is stored. Public signup assigns the `user` role; the signup request cannot set a role.

On login, the API verifies the password and returns a short-lived JWT access token and a refresh token. Protected routes expect the access token in the `Authorization: Bearer <token>` header. The token contains the user ID and role. The users table does not currently include an account activity flag.

Refresh tokens are generated randomly. The database stores only their SHA-256 hashes, along with expiry and revocation details. Refreshing rotates the token: the old token is revoked and linked to its replacement. Reuse of a revoked token revokes the user's remaining refresh tokens. Logging out revokes the supplied refresh token; an already issued access token remains usable until it expires.

The role table below summarizes route access at a high level. Resource ownership checks also apply in some service methods, as described in Sections 5 and 7.

| Role       | Access Permissions                                      |
| ---------- | ------------------------------------------------------- |
| USER       | Authenticated job browsing and other routes available to a regular user. |
| JOB_SEEKER | Job browsing, profile management, and job applications, when the account already has this role. |
| RECRUITER  | Job management and applications for jobs they created. |
| ADMIN      | Job management and application listing; some application status changes are limited by a creator check in the service. |

# 9. Validations & Exception Handling

Pydantic schemas validate request fields before the service layer handles them. The database adds foreign keys, unique constraints, not-null constraints, enum columns, and a non-negative experience check on job seeker profiles.

## 9.1 Input Validation

- Signup requires a username of 3-50 characters, a valid email address, and a password of 8-50 characters containing an uppercase letter, a number, and one of `!@#$%&*`.
- Job seeker profile creation requires a 10-digit phone number, date of birth, qualification, non-negative experience, and a non-negative current salary. Experience supports one decimal place.
- Job creation checks required text fields, non-negative salary and experience values, positive vacancy count, and valid employment type. It rejects minimum/maximum salary or experience ranges where the maximum is below the minimum.
- Applications require an existing job, a job seeker profile, a job that is accepting applications, and a resume with an allowed filename extension. Uploads are limited to 5 MB. The service prevents duplicate applications for the same job seeker and job.
- Application status values are restricted to the defined enum and allowed transitions. Selecting a candidate requires an open job with at least one vacancy.

Resume checks use the filename extension and size; the server does not inspect the file contents to verify its actual format.

## 9.2 Database-level validations

The schema uses primary keys, foreign keys, indexes, uniqueness constraints, not-null columns, and enum types. It prevents duplicate emails, duplicate job seeker profiles for one user, and duplicate applications by the same job seeker to the same job. Job seeker experience also has a database check requiring a value of zero or greater. Foreign keys configured with cascade deletion remove dependent job seeker profiles or applications when their parent records are deleted.

## 9.3 Custom Exception Handling

The application defines exceptions for expected service errors, including missing users, invalid credentials, duplicate email addresses, missing jobs or profiles, duplicate applications, invalid status changes, and unauthorized actions. These are mapped to HTTP responses in `app/exception_handlers/handler.py`.

## 9.4 Framework Error Responses

FastAPI handles request validation errors and HTTP exceptions using its built-in handlers. The application also registers a generic handler for unexpected exceptions, which returns a 500 response and logs the failure. Email template or delivery errors are logged by the email service and do not fail the main request.

# 10. Testing

The test suite has unit tests for service behavior and integration tests that send requests to the FastAPI application. The cases cover core success paths along with selected validation and authorization failures.


## 10.1 Testing Frameworks and Tools

| Tool | Purpose |
|---|---|
| Pytest | Test execution and test case management |
| HTTPX | API integration testing |
| HTTPX AsyncClient with ASGITransport | Sending asynchronous requests to the FastAPI app in-process |
| PostgreSQL | Database operations and data persistence testing |

## 10.2 Test Cases

The repository contains 50 asynchronous test functions: 17 unit tests and 33 integration tests. This section describes the test cases present in the files; it does not indicate that the suite was run or passed.

### Unit tests

| Test file | Cases covered |
|---|---|
| `tests/unit/test_auth_service.py` (4) | Successful authentication, unknown user, incorrect password, and successful account creation. |
| `tests/unit/test_job_service.py` (5) | Job creation, listing, successful lookup, missing-job error, and update. |
| `tests/unit/test_job_seeker_service.py` (4) | Profile creation, duplicate-profile error, getting the current profile, and profile update. |
| `tests/unit/test_application_service.py` (4) | Application creation, duplicate application, closed job rejection, and selecting an applicant while reducing vacancies. |

### Integration tests

| Test file | Cases covered |
|---|---|
| `tests/integration/test_auth.py` (7) | Signup, duplicate email, invalid email, invalid password, short username, invalid login, and successful login with token fields. |
| `tests/integration/test_job.py` (11) | Job creation for admin and recruiter, forbidden creation for user and job seeker, invalid payload, listing, lookup, update, deletion, and recruiter ownership checks for updates and deletion. |
| `tests/integration/test_job_seeker.py` (8) | Unauthenticated profile creation, profile creation, own-profile retrieval/update/deletion, role restriction on deletion, listing, and lookup by ID. |
| `tests/integration/test_application.py` (6) | Applying with a resume, listing own applications, deleting an application, replacing a resume, recruiter application listing/filtering, and a status update to `UNDER_REVIEW`. |
| `tests/integration/test_db.py` (1) | Basic database connectivity using `SELECT 1`. |

Integration tests use an async SQLAlchemy session configured from `TEST_DATABASE_URL`; the fixture creates and drops the mapped tables around each test. The test suite does not currently include explicit cases for refresh-token rotation/logout, email delivery failure handling, invalid resume format/size, or most application status transitions and ownership scenarios.

## 10.3 Test Execution

Run the complete test suite from the project root with:

```powershell
.venv\Scripts\python.exe -m pytest -q
```

The integration-test fixture uses `TEST_DATABASE_URL` and creates and drops the mapped tables for each test. Configure it to point to a dedicated test database before running the suite.

## 10.4 Test Result

Last recorded execution on 2026-11-05: `50 passed, 1 warning in 163.27s` using the project virtual environment. The warning was from pytest being unable to create a cache file because the cache path already existed (`WinError 183`); no tests failed. This result describes that execution and may differ on another machine or run.

## 10.5 Test Conclusion

All current unit and integration test cases passed in the recorded run. The suite provides coverage for core authentication, jobs, job seeker profiles, applications, and database connectivity. It does not cover every documented or implemented behavior; see the coverage gaps listed in Section 10.2.




# 11. Setup Instructions

The steps below set up the API on a local machine. The database and mail settings are read from `.env` when the application starts.

## 11.1 Prerequisites

- Python 3.11 or newer (`datetime.UTC` is used by the application).
- PostgreSQL.
- Git and pip.

## 11.2 Clone the Repository

```bash
git clone https://github.com/tharnishpalanisamy/Job-Recruitment-fastAPI.git
cd Job-Recruitment-fastAPI
```

## 11.3 Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it before installing packages.

**Windows:**

```powershell
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

## 11.4 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 11.5 Database and Environment Configuration

Create a PostgreSQL database for the application and a separate database for tests. Copy `.env.example` to `.env` (`cp .env.example .env` on Linux/macOS, or `Copy-Item .env.example .env` in PowerShell), then fill in the required values. The test fixtures create and drop the mapped tables in `TEST_DATABASE_URL`, so it must point to a disposable test database rather than the application database.

The settings used by the application include:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=job_recruitment
DATABASE_URL=postgresql+asyncpg://your_database_user:your_database_password@localhost:5432/job_recruitment
TEST_DATABASE_URL=postgresql+asyncpg://your_database_user:your_database_password@localhost:5432/job_recruitment_test

JWT_SECRET_KEY=replace_with_a_long_random_secret_value
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

MAIL_USERNAME=your_mail_username
MAIL_PASSWORD=your_mail_password
MAIL_FROM=your_sender_address
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=true
MAIL_SSL_TLS=false
```

`MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_FROM` are required settings. Email delivery is best effort once the application is running, but these settings must still be present for startup configuration.

## 11.6 Run Database Migrations

From the project root, apply the schema migrations to the application database:

```bash
alembic upgrade head
```

## 11.7 Run the Application

```bash
uvicorn app.main:app --reload
```

The API listens at `http://127.0.0.1:8000` by default.

## 11.8 Open the API Documentation

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## 11.9 Run Tests

With the virtual environment active and `TEST_DATABASE_URL` pointing to the test database, run `python -m pytest -q`. See Section 10 for the test inventory and the last recorded result.

# 12. Conclusion

This repository contains a FastAPI backend for job postings, job seeker profiles, and application tracking. It includes JWT authentication with refresh-token rotation, role checks, resume uploads, email templates, SQLAlchemy persistence, and Alembic migrations.

The current API covers the main job and application workflows. User role provisioning and user-management endpoints are not exposed, and application status updates are limited by the job-creator check described above. The test suite currently passes its 50 existing cases; the remaining coverage gaps are listed in Section 10.2.
