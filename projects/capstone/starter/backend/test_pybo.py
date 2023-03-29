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
        response = self.client.get("/question/list")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["questions"]), 10)

        # 404, Not found questions
        response = self.client.get("/question/list?page=9999")
        self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()
