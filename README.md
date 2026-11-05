# 1 Project Abstract 

Job Recruitment and Applicant Tracking System 

The Job Recruitment and Applicant Tracking System is a system to streamline and manage the job recuitment process .
It is developed using python , FastAPi and PostgreSQL . This system provides a cetralized platform that can be used 
for job posting , managing job vacancies , job applicants etc...

The sysetm is developed using Python , FastApi , and PostgreSQL , following a structured backend architecture and solid principles to ensure maintainablity , extendability and scalability . 

The application supports four user roles which are User , Job Seeker , Recruiter and Admin where Each role has different level of permissions and authorization . 
eg : Administrators can manage users and oversee system operations, Recuiters can create and manage job vacancies and process applications, while regular users can browse available job opportunities, Job Seekers maintain their job seeker profiles, and apply for suitable positions.

The system includes secure authentication using JWT tokens and refresh tokens . It also provides application tracking capabilities, allowing Recruiters to review applications and update their statuses throughout the recruitment process.

Additionally the system also sends email notification to the users in situations like account creation , job application , application update etc... 

The application supports role based access with different permissions for User , Job Seeker , Recruiter and Admin 

Roles and Authorization level 
User - Users can register and authenticate securely using JWT-based authentication with refresh token support. 
Job Seeker - Can view and search Jobs , Apply for Jobs , maintain their application and Job Seeker profile 
Recruiter - Can post Job Vacancies , manage job posting , review applications received for Jobs they posted 
Admin - Can post Job vacancies , manage Job posting , Review applications 


# 2 Technology Stack

The Job Recruitment and Applicant Tracking System is developed using the following technologies 

1)Python 3 - programming language used for the backend development.
2) FastAPI - Backend web framework used to develop RESTful APIs. 
3) Uvicoen - ASGI server used to run the FastAPI application. 
4) PostgreSQL - Relational database used to store and manage the applications data. 
5) SQLAlchemy - ORM used for database models and database operations.
6) Alembic - Database migration management and schema version control.
7) Pydantic - Data validation, serialization, and request/response schema management.
8) JWT (JSON Web Tokens) - Secure user authentication and access control. 
9) Pytest - Unit and integration testing of application functionality.
10) HTTPX - Asynchronous HTTP client used for API integration testing. 
11) Jinja2 - Template engine used for generating dynamic HTML content using templates. 
11) Git & GitHub - Version control and source code management 
12) Swagger UI - Interactive API documentation and endpoint testing. 

# 3 Project Folder Structure

## 3.1 Directory Structure

```text
project/
├── alembic/
│   └── versions/
├── app/
│   ├── api/v1/
│   │   ├── application/
│   │   ├── auth/
│   │   ├── health/
│   │   ├── job/
│   │   └── job_seekers/
│   ├── client/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── exception_handlers/
│   ├── exceptions/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   │   ├── implementations/
│   │   └── protocols/
│   ├── schemas/
│   ├── services/
│   │   ├── implementations/
│   │   └── protocols/
│   ├── templates/
│   ├── utilities/
│   ├── create_admin.py
│   └── main.py
├── logs/
├── tests/
│   ├── integration/
│   └── unit/
├── uploads/
│   └── resumes/
├── alembic.ini
├── pytest.ini
├── README.md
└── requirements.txt
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

IDE: PyCharm / Visual Studio Code

Database Management: pgAdmin / PostgreSQL

API Testing: Swagger UI

Version Control: Git and GitHub

# 5 User Roles & Authorization

The Job Recruitment and Applicant Tracking System implements Role-Based Access Control (RBAC) to manage user permissions and restrict access to specific functionalities based on roles. 

The system consists of four roles 

# 5.1 User 

The User role represents a registered user who has access to basic account functionalities. 
# Permissions 
1) Register and log in to the application. 
2) Manage personal account details.
3) Access authorized user functionalities. 
4) Access Protected routes like jobs etc.. 


# 5.2 Job Seeker 

The Job Seeker role represents an user looking for job ooportunities 

# Permissions 
1) All regular user permissions 
2) Create and Manage job seeker profile 
3) Browse available job opportunities 
4) view individual job details 
5) Apply to available jobs 
6) Manage their applications 
7) Track application status 

# 5.3 Recruiter 

The recruiter role represents a HR , Reponsible for managing job vacancies , handling recruitment activities and selecting candidates . 

# Permissions:

1) Create and publish job vacancies.
2) View and manage job postings.
3) Update job vacancy details.
4) Close or reopen job vacancies.
5) View applications submitted for job vacancies.
6) Review applicant information and resumes.
7) Update application statuses throughout the recruitment process.

# 5.4 Admin 

The Admin role has administrative privileges and is responsible for managing and overseeing the system.

# Permissions:

1) Access administrative functionalities.
2) View and manage registered users.
3) Manage user roles and permissions.
4) View and manage job vacancies.
5) Monitor job applications.
6) Oversee overall system operations.


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
| email | VARCHAR(255) | Unique, Indexed |
| password_hash | VARCHAR(255) | Not Null |
| role | ENUM | Not Null, Default USER |
| is_active | BOOLEAN | Not Null, Default TRUE |
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


5) Refresh Tokens Table (refresh_tokens)

Stores refresh token information to support secure authentication, token rotation, and logout functionality.

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
| Users → Job Seekers | One-to-One | A user can have one job seeker profile. |
| Users → Jobs | One-to-Many | A recruiter can create multiple job vacancies. |
| Users → Refresh Tokens | One-to-Many | A user can have multiple refresh tokens. |
| Job Seekers → Applications | One-to-Many | A job seeker can submit multiple applications. |
| Jobs → Applications | One-to-Many | A job vacancy can receive multiple applications. |
| Refresh Tokens → Refresh Tokens | Self-referencing | A refresh token can reference its replacement token. |


# 7 API Documentation

All routes are mounted under `/api/v1`. FastAPI provides interactive documentation at `/docs` and the OpenAPI document at `/openapi.json`.

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
| POST | `/api/v1/job-seekers/create` | Job seeker | Create own profile |
| GET | `/api/v1/job-seekers/me` | Job seeker | Get own profile |
| PATCH | `/api/v1/job-seekers/me` | Job seeker | Update own profile |
| DELETE | `/api/v1/job-seekers/me` | Job seeker | Delete own profile |
| GET | `/api/v1/job-seekers/` | Recruiter or admin | Search profiles with filters and pagination |
| GET | `/api/v1/job-seekers/{job_seeker_id}` | Recruiter or admin | Get a profile by ID |

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
| PATCH | `/api/v1/application/{application_id}/status?status={status}` | Recruiter or admin | Update status using allowed transition rules |

There are no user-management CRUD routes in the current API. Application responses differ by endpoint; the detailed recruiter/admin list response includes the stored resume path.


# 8. Authentication Flow 

The Job Recruitment and Applicant Tracking System implements a secure authentication mechanism using JSON Web Tokens (JWT) and refresh tokens. The authentication system verifies user identity and controls access to protected API endpoints. 

# 8.1 User Authentication 

1) A user registers using the signup endpoint with the required account details.
2) The password is hashed and then stored in the database. 
3) during login the system fetches the user corresponding to the user and verifies the password with the hashed password stored in the database 
4) When verifed the system returns a access token and a refresh token to the user . where access token is used to authenticate the user and refresh token is used to renew or get new access token 

# 8,2 JWT Access Token 

JWT access tokens are used to authenticate users when accessing protected API endpoints. 

1) The token is generated after successful login.
2) It contains the required user identification and authentication claims.
3) The client sends the token through the HTTP Authorization header.
4) The server validates the token's signature and expiration.
5) If valid, the authenticated user is identified and allowed to proceed, subject to authorization checks.

# 8.3 Refresh Token Management 

Refresh tokens allow users to obtain new access tokens without logging in again.

this application implements server side token management 

1) refresh tokens are generate during login 
2) when access token expires a new token can be acquired using the refresh token 
3) when a new access token is generated the system rotates or issues new refresh token as well and revokes the old one
4) when a revoked token is used again it logs out the user 
5) it ensures Expired or revoked refresh tokens cannot be reused. 

# 8.4 Role-Based Authorization 

The application implements Role-Based Access Control (RBAC) to restrict API access according to the authenticated user's role.

The system supports four roles:

| Role       | Access Permissions                                      |
| ---------- | ------------------------------------------------------- |
| USER       | Basic account functionalities                           |
| JOB_SEEKER | Job browsing, profile management, and job applications  |
| RECRUITER  | Job vacancy management and applicant management         |
| ADMIN      | Administrative operations and overall system management |



# 9 Validations & Exception Handling 

The Job Recruitment and Applicant Tracking System implements input validation and centralized exception handling to maintain data integrity, prevent invalid operations, and provide meaningful error responses. 


# 9.1 Input Validation 

Pydantic schemas are used to validate incoming request data before processing it through the application.

1) User Validation
- Username and email are required during registration.
- Email must follow a valid email format.
- Password must have atleast one capital letter , one number and one symbol.
- Duplicate email addresses are not allowed.
- User roles must match the predefined role values.

2) Job Seeker Profile Validation
- Full name, phone number, and qualification are required.
- Phone number must contain exactly 10 digits.
- Date of birth must be a valid date.
- Experience must be a non-negative value.

3) Job Validation
- Job title, description, requirements, qualification, and location are mandatory.
- Minimum experience must be non-negative.
- Maximum experience must not be less than minimum experience.
- Salary values must be non negative .
- Employment type must match the predefined enum values.
- Vacancy count must be a valid positive integer.
- Job status must be a valid predefined value.

4) Application Validation
- The referenced job must exist.
- The job seeker must have a valid profile.
- A job seeker cannot apply for the same job multiple time.
- Resume uploads must satisfy the configured file type and size restrictions.
- Application status must match the predefined application status values.

# 9.2 Database-level validations 

1) Added Primary to ensure unique identification 
2) Added Foriegn Key to maintain relationship between tables 
3) Added Index to ensure Quick lookup 
4) Added Unique constraint to Prevents duplicate email addresses, job seeker profiles, and duplicate applications.
5) Added NotNull constraint to restrict null values
6) Added Check Constraint to restrict values 
7) Added Enum to only allow specified values
8) Added Cascase Delete to remove dependent records when configured parent records are deleted.


# 9.3 Custom Exception Handling

The application has many custom exception classes to handler business logic errors 

Examples 

1) UserNotFoundException - Raised when a requested user does not exist. 
2) InvalidCredentialsException - Raise when user logs in with invalid credentials 
3) JobNotAcceptingApplicationsException - Raised when user Tries to apply to a job with no vacancies or closed 
4) EmailAlreadyExists - Raised when registering with an existing email address. 
5) NotAuthorizedException - Raise when user tries to access routes which they are not authorized to access 


# 9.4 Centralized Exception Handling
FastAPI exception handlers are registered centrally in the application to provide consistent error responses.

The system handles:
- Custom application exceptions.
- HTTP exceptions.
- Request validation errors.
- Unexpected internal server errors.


# 10. Testing

The Job Recruitment and Applicant Tracking System is tested using Pytest to verify the correctness, reliability, and expected behaviour of its API endpoints and backend operations.

HTTPX is used as an asynchronous HTTP client for testing API endpoints, while test cases verify successful operations, validation failures, authentication, authorization, and exception handling.


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
