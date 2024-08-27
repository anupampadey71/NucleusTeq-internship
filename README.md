# NucleusTeq-internship
This repsoitry is uploading my training and internship work at nucleus teq

# Employee Management System

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
- [Database Configuration](#database-configuration)
- [Database Schema](#database-schema)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)

## Introduction
This Employee Management System is a full-stack application that includes a React frontend and a FastAPI backend. The system allows for managing employees, projects, and other related tasks.

## Prerequisites
- Node.js and npm
- Python 3.9
- Anaconda
- MySQL database

## Setup Instructions

### Frontend Setup
1. Navigate to the frontend directory:
    ```bash
    cd NucleusTeq-internship/Employee Management System/frontend/employee-management-system
    ```
2. Install the dependencies:
    ```bash
    npm install
    npm install react-scripts
    ```

### Backend Setup
1. Download and install Anaconda from [here](https://www.anaconda.com/products/distribution).

2. Navigate to the backend directory and create a conda environment:
    ```bash
    cd NucleusTeq-internship/Employee Management System
    conda create -p venv python==3.9 -y
    ```

3. Activate the conda environment:
    ```bash
    conda activate venv/
    ```

4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Database Configuration
1. Update the `config/databases.py` file with your MySQL database details:
    ```python
    # config/databases.py

    host = "your_mysql_host"
    user = "your_mysql_user"
    passwd = "your_mysql_password"
    database = "your_database_name"
    ```

2. Use the `schema.txt` file to create the necessary tables in your MySQL database.

## Database Schema
Execute the SQL statements in `schema.txt` to set up the database schema. Here is an example of what `schema.txt` might contain:

```sql
CREATE TABLE employee (
    employeeId VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255),
    department VARCHAR(255)
);

CREATE TABLE project (
    projectId VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    managerId VARCHAR(255),
    FOREIGN KEY (managerId) REFERENCES employee(employeeId)
);
```
## running the application 
1. for running frontend
   ```bash
    cd NucleusTeq-internship/Employee Management System/frontend/employee-management-system
    npm start
    ```
2. for running backend
   ```bash
    cd NucleusTeq-internship/Employee Management System
    uvicorn main:app --reload
    ```

## Testing the application
1. Ensure the backend server is running.
2. Navigate to the test directory and run your tests using pytest:
   ```bash
    cd NucleusTeq-internship/Employee Management System/Test
    pytest test_nameoftestfile.py
    ```
3. To generate a test coverage report, run the following command:
   ```bash
    cd NucleusTeq-internship/Employee Management System/Test
    coverage run -m pytest test_assignment.py test_auth.py test_department.py test_employee.py test_employeeskill.py test_manager.py test_project.py test_request.py test_skillset.py
    coverage html && start htmlcov/index.html
    ```
