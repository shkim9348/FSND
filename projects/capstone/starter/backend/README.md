# Pybo Board  
This project is a backend application for a Q&amp;A web application called Pybo. The project structure is as follows:  

## Project Structure
```
├── README.md
├── config.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── package-lock.json
├── package.json
├── pybo
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   └── views.py
├── pybo.db
└── requirements-dev.txt
```

To run the project, first install the necessary dependencies by running  
`pip install -r requirements-dev.txt`  
Then, run the Flask development server with `flask run`. The server should start on `http://127.0.0.1:5000`.

## Authentication
---
This API uses JWT-based authentication. To access any of the endpoints that require authentication, you need to include an `Authorization` header in your request with a valid JWT token.

## Auth0 User permissions
User1. manager : all permissions
```
get:question
post:question
put:question
delete:question
vote:question
get:answer
post:answer
put:answer
delete:answer
vote:answer
```
User2. boarder2 : All permissions except put:answer and delete:answer
```
get:question
post:question
put:question
delete:question
vote:question
get:answer
post:answer
put:answer
delete:answer
vote:answer
```

