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
This API uses JWT-based authentication. To access any of the endpoints that require authentication, you need to include an `Authorization` header in your request with a valid JWT token.

## Auth0 User permissions
#### User1. manager : all permissions  
>ID: manager@ver.team / PW: !verteam1   

`get:question` - Get the list and detail of questions on the board.
`post:question` - Write the question.
`put:question` - Edit existed questions.
`delete:question` - Delete existed questions.
`vote:question` - Vote existed questions.
`get:answer` - Get registered answers to questions.
`post:answer` - Write answers to existed questions.
`put:answer` - Edit existed answers.
`delete:answer` - Delete existed answers.
`vote:answer` - Vote existed answers.  

#### User2. boarder2 : All permissions to the question and get:answer, vote:answer  
> ID: boarder2@ver.team / PW: !verteam1   

`get:question` - Get the list and detail of questions on the board.
`post:question` - Write the question.
`put:question` - Edit existed questions.
`delete:question` - Delete existed questions.
`vote:question` - Vote existed questions.
`get:answer` - Get registered answers to questions.
`vote:answer` - Vote existed answers.  

## API endpoints

### GET '/question'
- Get the list of questions on the board

#### Query Parameters

- `page` (optional): Page number to retrieve. Default is 1.  
- `kw` (optional): Keyword to search for in the question title, content, answer content and answer author username. Default is empty.  

### Response
Body: JSON object with the following keys:  

- questions: An array of objects, each representing a question and its associated answers. Each object contains the following keys:  
  - id: Unique identifier of the question.  
  - subject: Title of the question.  
  - content: Content of the question.  
  - create_date: Date and time when the question was created.  
  - user_id: Unique identifier of the user who created the question.  
  - username: Username of the user who created the question.  
  - answers: An array of objects, each representing an answer to the question. Each object contains the following keys:  
    - id: Unique identifier of the answer.  
    - question_id: Unique identifier of the question to which the answer belongs.  
    - content: Content of the answer.  
    - create_date: Date and time when the answer was created.  
    - user_id: Unique identifier of the user who created the answer.  
    - username: Username of the user who created the answer.  
- total: Total number of questions found.  
- page: Current page number.  
- per_page: Number of questions per page.  
- has_prev: Boolean indicating whether there is a previous page.  
- prev_num: Page number of the previous page.  
- page_nums: An array of page numbers for pagination navigation.  
- has_next: Boolean indicating whether there is a next page.  
- next_num: Page number of the next page.  
- kw: Keyword used for searching.  

Sample curl request:  
`curl -X GET http://127.0.0.1:5000/question`

Sample response:  
```
{
  "has_next": true,
  "has_prev": false,
  "kw": "",
  "next_num": 2,
  "page": 1,
  "page_nums": [
    1,
    2,
    3,
    4,
    5,
    null,
    29,
    30
  ],
  "per_page": 10,
  "prev_num": null,
  "questions": [
    {
      "answer_set": [],
      "id": 1,
      "subject": "How do I create a virtual environment in Python?",
      "content": "I want to create a virtual environment for my Python project. How can I do this?",
      "create_date": "Sat, 08 Apr 2023 02:17:12 GMT",
      "modify_date": null,
      "user": {
        "email": "johndoe@aaa.com",
        "username": "johndoe"
      },
      "voter": [
        {
          "email": "janedoe@aaa.com",
          "username": "janedoe"
        }
      ]
      ...
      "total": 200,
    }
```
### Get '/question/<int:question_id>'
- Get detail of the question(id)  
- Returns: a JSON object with question inofermation.  

Sample curl request:  
`curl -X GET http://127.0.0.1:5000/question/1`

Sample response:  
```
{
  "answer_set": [
    {
      "content": "this is answer 1.",
      "create_date": "Sat, 18 Feb 2023 23:31:19 GMT",
      "id": 1,
      "modify_date": null,
      "user": {
        "email": "johndoe@aaa.com",
        "username": "johndoe"
      },
      "voter": []
    }
  ],
  "content": "This is new Content",
  "create_date": "Sat, 18 Feb 2023 22:28:02 GMT",
  "id": 1,
  "modify_date": null,
  "subject": "This is new Subject",
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### POST '/question'
- Create the question on the board  
- Request arguments: a JSON formatted oject with optional keys 'subject','content','user(username,email)'.
- Returns: a JSON object with success status true when new question was successfully added into the database.  

Sample curl request:  
`curl -X POST http://127.0.0.1:5000/question -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"subject": "Test Subject", "content": "Test Content"}'`  

Sample response:  
```
{
  "answer_set": [],
  "content": "Test Content",
  "create_date": "Sat, 18 Feb 2023 22:28:02 GMT",
  "id": 1,
  "modify_date": null,
  "subject": "Test Subject",
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### PUT '/question/<int:question_id>'
- Edit subject or content of existed question  
- Request arguments: a JSON formatted oject with optional keys 'subject','content'.  
- Returns: a JSON object with success status true when the question information was successfully updated into the database.  

Sample curl request:  
`curl -X PUT http://127.0.0.1:5000/question -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"subject": "Update Subject", "content": "Update Content"}'`  

Sample response:  
```
{
  "answer_set": [],
  "content": "Update Content",
  "create_date": "Sat, 18 Feb 2023 22:28:02 GMT",
  "id": 1,
  "modify_date": "Sun, 19 Feb 2023 15:10:11 GMT",
  "subject": "Update Subject",
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### DELETE '/question/<int:question_id>'
- Delte existed question  
- Returns: a JSON object with success status true when the question was successfully deleted from the database.  

Sample curl request:  
`curl -X DELETE http://127.0.0.1:5000/question -H "Authorization: Bearer <ACCESS_TOKEN>"`  

Sample response:  
```
{
  'success': True, status_code: 200
}
```

### GET '/question/<int:question_id>/answer/<int:answer_id>'
- This endpoint returns the answer information corresponding to the given `question_id` and `answer_id`. If there is no answer that matches the given IDs, it returns a 404 error.  
- Returns: a JSON object with answer inofermation.  

Sample curl request:  
`curl -X GET http://127.0.0.1:5000/question/1/answer/2`  

Sample response:  
```
{
  "content": "this is answer.",
  "create_date": "Sat, 18 Feb 2023 23:31:19 GMT",
  "id": 2,
  "modify_date": null,
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### POST '/question/<int:question_id>/answer'
- This endpoint allows users to create an answer for a given question.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the answer information was successfully added into the database.  

Sample curl request:  
`curl -X POST http://127.0.0.1:5000/question/1/answer -H "Authorization: Bearer {ACCESS_TOKEN}" -H "Content-Type: application/json" -d '{"content":"This is an example answer."}'`  
Sample response:  
```
{
  "content": "This is an example answer.",
  "create_date": "Sun, 19 Feb 2023 23:31:19 GMT",
  "id": 3,
  "modify_date": null,
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### PUT '/question/<int:question_id>/answer/<int:answer_id>'
- Modify an existing answer to a question.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the answer information was successfully updated into the database.  

Sample curl request:  
`curl -X PUT http://127.0.0.1:5000/question/1/answer/3 -H "Authorization: Bearer {ACCESS_TOKEN}" -H "Content-Type: application/json" -d '{"content":"Update Content"}'`  
Sample response:  
```
{
  "content": "Update Content",
  "create_date": "Sun, 19 Feb 2023 23:31:19 GMT",
  "id": 3,
  "modify_date": null,
  "user": {
    "email": "johndoe@aaa.com",
    "username": "johndoe"
  },
  "voter": []
}
```

### DELETE '/question/<int:question_id>/answer/<int:answer_id>'
- Delete an existing answer to a question.
- Request arguments: a JSON formatted object with optional keys 'content'
- Returns: a JSON object with success status true when the answer information was successfully deleted into the database.  

Sample curl request:  
`curl -X PUT http://127.0.0.1:5000/question/1/answer/3 -H "Authorization: Bearer {ACCESS_TOKEN}"`  
Sample response:  
```
{
  'success': True, status_code: 200
}
```

## Testing
The testing of all endpoints was implemented with unittest. The command line interface run the test file:  
`python test_pybo.py`
