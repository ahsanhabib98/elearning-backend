# Learning Platform Backend

This is the repository of Learning Platform

## Running with Docker and Docker Compose

Run all the commands from project root directory.

### Running Backend service

1. Copy example environment file

```
cp backend/.env.example backend/.env
```

2. Build and run backend service

```
docker-compose -p learning-platform -f docker-compose.yml up --build
```

After waiting for while, visit following urls:

* UI: http://localhost:8000
* API documentation: [API collection](https://documenter.getpostman.com/view/8714749/UzQrRn9e)

## Git branching model
I follow Git Flow as my branching model.
Please read this article to know about [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)