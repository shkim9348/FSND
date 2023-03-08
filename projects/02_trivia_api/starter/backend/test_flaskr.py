import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import response

from flaskr import create_app
from models import setup_db, Question, Category

DATABASE_NAME = "trivia_test"
DATABASE_PATH = "postgresql://postgres:postgres@127.0.0.1:5432/trivia_test"

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # load test data
        os.system(f'psql "{DATABASE_PATH}" {DATABASE_NAME} -c "DROP TABLE questions, categories;"')
        os.system(f'psql "{DATABASE_PATH}" {DATABASE_NAME} < ./trivia.psql')

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DATABASE_NAME
        self.database_path = DATABASE_PATH
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_available_categories(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(len(data["categories"]), 6)
        self.assertEqual(data["categories"]["4"], "History")

        # 404, check not found the category
        response = self.client().get('/categories/500')
        self.assertEqual(response.status_code, 404)

    def test_list_questions(self):
        response = self.client().get('/questions')
        self.assertEqual(response.status_code, 200)

        # 404, check not found the page
        response = self.client().get('/questions?page=500')
        self.assertEqual(response.status_code, 404)

    def test_delete_question(self):
        # create a question to delete
        question = Question(question="new question", answer="new answer", category=1, difficulty=1)
        question.insert()
        question_id = question.id

        # delete the question
        response = self.client().delete(f'/questions/{question_id}')
        self.assertEqual(response.status_code, 200)

        # check if the question has been deleted
        question = Question.query.filter(Question.id == question.id).one_or_none()
        self.assertEqual(question, None)

        # 404, check not found the question
        response = self.client().delete(f'/questions/{question_id}')
        self.assertEqual(response.status_code, 404)

    def test_create_question(self):
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'category': 1,
            'difficulty': 1
        }
    
        # Sends POST request with the new question as JSON payload
        response = self.client().post('/questions', json=new_question)
    
        # Asserts that the new question is successfully created
        self.assertEqual(response.status_code, 200)

        # 400, invalid category
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'categoty': 100,
            'difficulty': 1,
        }

        response = self.client().post('questions', json=new_question)
        self.assertEqual(response.status_code, 400)

    def test_search_questions(self):
        search_q = {'searchTerm': 'a'}

        response = self.client().post('/questions/search', json=search_q)
        self.assertEqual(response.status_code, 200)

    def test_category_questions(self):
        response = self.client().get('/categories/1/questions')
        self.assertEqual(response.status_code, 200)

        # 404, invalid categoty_id
        response = self.client().get('/categories/1000/questions')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not Found", response.data.decode())

    def test_quizzes(self):
        new_quiz = {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1}}

        response = self.client().post('/quizzes', json=new_quiz)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('question', data)

        # 400, not input id
        new_quiz = {'previous_questions': [], 'quiz_category': {'type': 'Science', }}

        response = self.client().post('/quizzes', json=new_quiz)
        self.assertEqual(response.status_code, 400)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
