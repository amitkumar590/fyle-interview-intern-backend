# Fyle Interview Intern Backend

This repository contains the backend application for the Fyle interview intern project. The application is built using Flask and is containerized using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed  and running on your machine.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/amitkumar590/fyle-interview-intern-backend
cd fyle-interview-intern-backend
```

## Building and Running the Application

To build the Docker images and start the containers, run:

```bash
    docker-compose up --build
```

This command will:

- Build the Docker image for the Flask application.
- Start the container and make the Flask application available at http://localhost:7755.

## Accessing the Application

Once the containers are up and running, you can access the application by navigating to http://localhost:7755 in your web browser.

## Environment Variables

- FLASK_APP: Entry point for the Flask application, set to core/server.py.
- FLASK_ENV: Environment mode, set to production for production deployment.

## Important Notes

Ensure that no other service is running on port 7755 as it will be used by the Flask application.

## Example Endpoints

You can test the application using tools like curl, Postman, or your web browser. For example:

```bash
    curl -X GET \ -H "X-Principal: {\"user_id\": 5, \"principal_id\": 1}" \http://localhost:7755/principal/assignments
```    

This should return a JSON response indicating the status and time:

```
    {
    "data": [
        {
        "content": "test content",
        "created_at": "2024-05-20T23:09:41.125361",
        "grade": "D",
        "id": 1,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2024-05-20T23:09:41.125367"
        },
        {
        "content": "test content",
        "created_at": "2024-05-20T23:09:41.125774",
        "grade": "D",
        "id": 2,
        "state": "GRADED",
        "student_id": 1,
        "teacher_id": 1,
        "updated_at": "2024-05-20T23:09:41.125777"
        },
        ...
    }
```

