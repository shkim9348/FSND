import unittest
import json
from pybo.database.models import Question, Answer, User
from datetime import datetime
from pybo import create_app

class PyboTestCase(unittest.TestCase):
    """This class represents the pybo test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        """Excute after reach test"""
        pass

    # Quesstion tests
    """get_questions"""

    def test_get_questions(self):
        res = self.client.get("/question/list?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 10)

    def test_get_questions_fail(self):
        res = self.client.get("/question?page=-1")
        self.assertEqual(res.status_code, 404)

    """get_question_detail"""

    def test_get_question_detail(self):
        question_id = 1
        res = self.client.get(f"/question/detail/{question_id}")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

    def test_get_question_detail_fail(self):
        # Set a non-existing Notice ID
        non_existing_question_id = 9999
        res = self.client.get(f"/question/detail/{non_existing_question_id}")
        self.assertEqual(res.status_code, 404)

    """test_create_question """

    def test_create_question(self):
        new_question = {
            "subject": "New Test Subject",
            "content": "This is a new test question content.",
            "create_date": datetime.now()
        }
        res = self.client.post("/question/create", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["id"])

    def test_create_question_fail(self):
        invalid_question = {
            "subject": "", # Empty subject
            "content": "This is a new test question content.",
            "create_date": datetime.now()
        }
        res = self.client.post("/question/create", json=invalid_question)
        self.assertEqual(res.status_code, 400)

    """modify_question"""

    def test_modify_question(self):
        question_id = 1
        update_question = {
            "subject": "Updated Subject",
            "content": "This is an updated test question content.",
            "create_date": datetime.now()
        }
        res = self.client.post(f"/question/modify/{question_id}", json=update_question)
        data = json.loads(res.data)
        question = data["question"]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question["subject"], "Updated Subject")

    def test_modify_question_fail(self):
        non_existing_question_id = 9999
        update_question = {
            "subject": "Updated Subject",
            "content": "This is an updated test question content.",
            "create_date": datetime.now()
        }
        res = self.client.post(f"/question/modify/{non_existing_question_id}", json=update_question)
        self.assertEqual(res.status_code, 404)

    """ delete_question """

    def test_delete_question(self):
        new_question = {
            "subject": "Test Subject",
            "content": "This is a test question content.",
            "create_date": datetime.now()
        }
        res = self.client.post("/question/create", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["id"])

        question_id = data["id"]

        res = self.client.delete(f"/question/delete/{question_id}")
        self.assertEqual(res.status_code, 204)

    def test_delete_question_fail(self):
        non_existing_question_id = 9999
        res = self.client.delete(f"/question/delete/{non_existing_question_id}")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
