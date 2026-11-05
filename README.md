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

the application contains RESTful APIs developed using FastAPI . These endpoints allows user to login , view jobs , apply to jobs ,manage job vacancies, maintain job seeker profiles, and process job applications.

# 7.1 Health check APIs (/api/health)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /health | Check application health status | Public |
| GET | /health/db | Check database connectivity | Public |

example response 
{
  "status": "Healthy",
  "message": "Application is running"
}

# 7.2 Authentication APIs (/api/auth) 

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/auth/signup | Register a new user | Public |
| POST | /api/auth/login | Authenticate user and generate tokens | Public |
| POST | /api/auth/refresh | Generate new access and refresh tokens | Authenticated refresh token |
| POST | /api/auth/logout | Revoke refresh token | Authenticated |

example singup request body 
{
  "username": "tharnish",
  "email": "tharnish@gmail.com",
  "password": "tharnish@123"
}


# 7.3 User Management APIs (/api/users) 

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /api/users/me | Retrieve logged-in user details | Authenticated |
| GET | /api/users/ | Retrieve all users | Admin |
| GET | /api/users/{id} | Retrieve user by ID | Admin |
| PATCH | /api/users/me | Update logged-in user details | Authenticated |
| DELETE | /api/users/{id} | Delete a user | Admin |

Example – User Response 
{
  "id": 1,
  "username": "tharnish",
  "email": "tharnish@gmail.com",
  "role": "JOB_SEEKER",
  "is_active": true
} 

# 7.4 Job Seeker APIs (/api/job-seekers) 

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/job-seekers/profile | Create job seeker profile | Job Seeker |
| GET | /api/job-seekers/me | Retrieve own profile | Job Seeker |
| PATCH | /api/job-seekers/me | Update own profile | Job Seeker |
| DELETE | /api/job-seekers/me | Delete own profile | Job Seeker |
| GET | /api/job-seekers/ | Retrieve job seeker profiles | Recruiter / Admin |
| GET | /api/job-seekers/{id} | Retrieve a specific job seeker profile | Recruiter / Admin |

Example – Create Profile Request
{
  "full_name": "Tharnish",
  "phone": "9876543210",
  "date_of_birth": "2002-05-15",
  "qualification": "B.Sc Computer Science",
  "specialization": "Data Analytics",
  "experience_years": 1.5,
  "current_company": "ABC Technologies",
  "current_designation": "Software dev",
  "current_salary": 300000
}


# 7.5 Job Management APIs (/api/jobs) 

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/jobs/ | Create a new job vacancy | Recruiter |
| GET | /api/jobs/ | Retrieve available job vacancies | Authenticated |
| GET | /api/jobs/{id} | Retrieve job details | Authenticated |
| PATCH | /api/jobs/{id} | Update job vacancy details | Recruiter / Admin |
| DELETE | /api/jobs/{id} | Delete a job vacancy | Recruiter / Admin |


Example – Create Job Request 
{
  "title": "Python Backend Developer",
  "description": "Develop and maintain backend applications.",
  "requirements": "Python, FastAPI, PostgreSQL",
  "qualification": "B.Sc Computer Science",
  "experience_min": 0,
  "experience_max": 2,
  "salary_min": 300000,
  "salary_max": 500000,
  "employment_type": "FULL_TIME",
  "location": "Coimbatore",
  "vacancies": 3
}

Example – Job Response
{
  "id": 1,
  "title": "Python Backend Developer",
  "qualification": "B.Sc Computer Science",
  "employment_type": "FULL_TIME",
  "location": "Coimbatore",
  "vacancies": 3,
  "status": "OPEN"
}


# 7.6 Application Management APIs (/api/applications)

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/v1/application/apply | Apply for a job vacancy | Authenticated Job Seeker |
| GET | /api/v1/application/me | Retrieve applications submitted by the logged-in user | Authenticated Job Seeker |
| DELETE | /api/v1/application/{application_id} | Delete a job application using its ID | Authenticated |
| GET | /api/v1/application/{application_id} | Retrieve application details by ID | Authenticated |
| PATCH | /api/v1/application/{application_id}/update_resume | Update the resume attached to an application | Authenticated Job Seeker |
| GET | /api/v1/application/ | Retrieve all job applications | Recruiter / Admin |
| PATCH | /api/v1/application/{application_id}/status | Update the status of a job application | Recruiter / Admin |




