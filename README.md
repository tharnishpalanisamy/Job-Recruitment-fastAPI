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

# 3 Development Tools

IDE: PyCharm / Visual Studio Code

Database Management: pgAdmin / PostgreSQL

API Testing: Swagger UI

Version Control: Git and GitHub

# 4 User Roles & Authorization

The Job Recruitment and Applicant Tracking System implements Role-Based Access Control (RBAC) to manage user permissions and restrict access to specific functionalities based on roles. 

The system consists of four roles 

# 4.1 User 

The User role represents a registered user who has access to basic account functionalities. 
# Permissions 
1) Register and log in to the application. 
2) Manage personal account details.
3) Access authorized user functionalities. 
4) Access Protected routes like jobs etc.. 


# 4.2 Job Seeker 

The Job Seeker role represents an user looking for job ooportunities 

# Permissions 
1) All regular user permissions 
2) Create and Manage job seeker profile 
3) Browse available job opportunities 
4) view individual job details 
5) Apply to available jobs 
6) Manage their applications 
7) Track application status 

# 4.3 Recruiter 

The recruiter role represents a HR , Reponsible for managing job vacancies , handling recruitment activities and selecting candidates . 

# Permissions:

1) Create and publish job vacancies.
2) View and manage job postings.
3) Update job vacancy details.
4) Close or reopen job vacancies.
5) View applications submitted for job vacancies.
6) Review applicant information and resumes.
7) Update application statuses throughout the recruitment process.

# 4.4 Admin 

The Admin role has administrative privileges and is responsible for managing and overseeing the system.

# Permissions:

1) Access administrative functionalities.
2) View and manage registered users.
3) Manage user roles and permissions.
4) View and manage job vacancies.
5) Monitor job applications.
6) Oversee overall system operations.