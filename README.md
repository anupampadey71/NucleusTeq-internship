# NucleusTeq-internship
This repository is uploading my training and internship work at NucleusTeq.

# Employee Management System

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [Testing the Application](#testing-the-application)
- [Creating Docker Image](#creating-docker-image)

## Introduction
This Employee Management System is a full-stack application that includes a React frontend and a FastAPI backend. The system allows for managing employees, projects, and other related tasks.

## Prerequisites
- Node.js and npm
- Python 3.9
- Anaconda
- MySQL database
- Docker and Docker Compose

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
1. Install MySQL from [here](https://dev.mysql.com/downloads/installer/).
2. Create a MySQL database named `employee`:
    ```sql
    CREATE DATABASE employee;
    ```

3. Update the `config/databases.py` file with your MySQL database details:
    ```python
    # config/databases.py

    host = "your_mysql_host"
    user = "your_mysql_user"
    passwd = "your_mysql_password"
    database = "employee"
    ```

4. Use the `employee.sql` file to create the necessary tables in your MySQL database:
    ```bash
    mysql -u your_mysql_user -p employee < path_to_employee.sql
    ```

## Running the Application
1. For running the frontend:
    ```bash
    cd NucleusTeq-internship/Employee Management System/frontend/employee-management-system
    npm start
    ```
2. For running the backend:
    ```bash
    cd NucleusTeq-internship/Employee Management System
    uvicorn main:app --reload
    ```

## Testing the Application
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

## Creating Docker Image
1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project directory containing the `docker-compose.yaml` file.
3. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

Update the MySQL details in the `docker-compose.yaml` file based on your own parameters:

- `DB_USER`: Your MySQL username
- `DB_PASSWORD`: Your MySQL password
- `DB_NAME`: Your MySQL database name
- `MYSQL_ROOT_PASSWORD`: The root password for MySQL
