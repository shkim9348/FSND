# Documentating Endpoints

## GET '/api/v1.0/categories'

Description: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}

## GET '/questions?page=${integer}'
Description: Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
Request Arguments: page - integer
Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'totalQuestions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}

## GET '/categories/${id}/questions'
Description: Fetches questions for a cateogry specified by id request argument 
Request Arguments: id - integer
Returns: An object with questions for the specified category, total questions, and current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'History'
}

## DELETE '/questions/${id}'
Description: Deletes a specified question using the id of the question
Request Arguments: id - integer
Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

## POST '/questions'
Description: Sends a post request in order to add a new question
Request Body: 
{
    'question':  'new question',
    'answer':  'new answer',
    'difficulty': 1,
    'category': 1,
}
Returns: Does not return any new data

## POST '/questions'
Description: Sends a post request in order to search for a specific question by search term 
Request Body: 
{
    'searchTerm': 'this is the term the user is looking for'
}
Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'totalQuestions': 100,
    'currentCategory': 'Entertainment'
}

## POST '/quizzes'
Description: Sends a post request in order to get the random next question 
Request Body: 
{'previous_questions':  an array of question id's such as [1, 4, 20, 15]
'quiz_category': a string of the current category }
Returns: a single new question object at random
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
