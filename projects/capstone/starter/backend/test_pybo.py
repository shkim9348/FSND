import json
import unittest
from datetime import datetime

from pybo import create_app, db
from pybo.models import Answer, Question, User

BASE_URL = "http://127.0.0.1:5000/question"


# manager token
MANAGER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkcydlAwb2xzdTFPQ25ZbVFWSi1uQSJ9.eyJlbWFpbCI6Im1hbmFnZXJAdmVyLnRlYW0iLCJuYW1lIjoibWFuYWdlckB2ZXIudGVhbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2Rldi1od2diOGQxZjNyM3p0cWFxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDBlY2NjM2JlNDY0NDlhMzcyNWIzZmYiLCJhdWQiOlsicHlibyIsImh0dHBzOi8vZGV2LWh3Z2I4ZDFmM3IzenRxYXEudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4MDkwMDUzNiwiZXhwIjoxNjgxNzY0NTM2LCJhenAiOiJSbGoydzZ0bHpycnhJNFFYRlB3eEJJNENPa0MxTVllYiIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YW5zd2VyIiwiZGVsZXRlOnF1ZXN0aW9uIiwiZ2V0OmFuc3dlciIsImdldDpxdWVzdGlvbiIsInBvc3Q6YW5zd2VyIiwicG9zdDpxdWVzdGlvbiIsInB1dDphbnN3ZXIiLCJwdXQ6cXVlc3Rpb24iLCJ2b3RlOmFuc3dlciIsInZvdGU6cXVlc3Rpb24iXX0.CEjS5l9ILCcsol8jtlNx_1bHaNQG11e1usogSgDGWuEWtsB0VABUki6ItG84hRVj7Y2o9Zt0CSu5tV2gzKWBBXMWeFZBxMxjeFDpTA9AupdwpmNLXWR31To3h51DGYabsGiWFkCJ0Zmc5CxW0ylkfPgxrBY4oTczIxflQBXg5vrxJ5rDxqUKclPkThNDIOcK7P1vncgiUiz_alkQfIcGXzOdfIr7sQ1T2_VO3P5D9EgCG-xd2zDZbheQOPCQ_P1BhX4l2jsrcDiY58epO6o9okHd7-55xVv1WG5sOdzMrbhRfvt4-syKfqsmHIKQa6gpi-Ol-w52XvH-Hzw-JcFMeg"
BOARDER2_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkcydlAwb2xzdTFPQ25ZbVFWSi1uQSJ9.eyJlbWFpbCI6ImJvYXJkMkB2ZXIudGVhbSIsIm5hbWUiOiJib2FyZDJAdmVyLnRlYW0iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9kZXYtaHdnYjhkMWYzcjN6dHFhcS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjQyZDIzMDU5OGMzYzNlYzEzNjZmNDgyIiwiYXVkIjpbInB5Ym8iLCJodHRwczovL2Rldi1od2diOGQxZjNyM3p0cWFxLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2ODEwNDg1MDQsImV4cCI6MTY4MTkxMjUwNCwiYXpwIjoiUmxqMnc2dGx6cnJ4STRRWEZQd3hCSTRDT2tDMU1ZZWIiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnF1ZXN0aW9uIiwiZ2V0OmFuc3dlciIsImdldDpxdWVzdGlvbiIsInBvc3Q6cXVlc3Rpb24iLCJwdXQ6cXVlc3Rpb24iLCJ2b3RlOmFuc3dlciIsInZvdGU6cXVlc3Rpb24iXX0.gcQJBJN0BuOKwbFg5aI7WbsKxC5O5LEDxaEZfGcrDr-msmjo2gIe2-hISJL0Ai7u4Idzx9Bg1zDZmumq_J5JxOVduMIq3J4yd1vxjkdiWBkO4T9RgkIaB5CUlVnPGY5e_zHE79SZLnA0iQkqXcK9o15Zk25e5ON3-PnQ3VocQQS_lyWyJQM07qlz1Qf6RDJ4q6f9J__YJj_xEWCfrxaXEzY1wpMhkULcVU53mbhBYENNyAr2EOrqlPdfOHSPH4paClH7_U4pA_4cRiXKCJIF5rhKYc9qyNZH29X6uvq0EmI-6KA9Hld-yq4iixT9Adu4M5NzUySpzyC_GgZwYrXgEg"


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app(SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client

    def tearDown(self):
        pass

    def test_questions(self):
        response = self.client().get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_question_read(self):
        self.create_question(username="user1", email="user1@example.com")

        question_id = 1
        response = self.client().get(f"{BASE_URL}/{question_id}/")
        self.assertEqual(response.status_code, 200)

    def test_question_create(self):
        self.create_question(username="manager", email="manager@ver.team")

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANAGER_TOKEN}"}
        data = {"subject": "Test Question", "content": "This is a test question."}
        response = self.client().post(BASE_URL, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_question_modify(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANAGER_TOKEN}"}
        data = {
            "subject": "Modified Test Question",
            "content": "This is a modified test question.",
        }
        response = self.client().put(
            f"{BASE_URL}/{question_id}/", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

    def test_question_delete(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        headers = {"Authorization": f"Bearer {MANAGER_TOKEN}"}
        response = self.client().delete(f"{BASE_URL}/{question_id}", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_question_vote(self):
        self.create_question(username="manager", email="manager@ver.team")
        self.create_question(username="user1", email="user1@example.com")

        # manager vote to user1's question
        question_id = 2
        headers = {"Authorization": f"Bearer {MANAGER_TOKEN}"}
        response = self.client().post(f"{BASE_URL}/{question_id}/vote", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_answer_read(self):
        self.create_question(username="user1", email="user1@example.com")

        question_id = 1
        answer_id = 1
        response = self.client().get(f"{BASE_URL}/{question_id}/answer/{answer_id}")
        self.assertEqual(response.status_code, 200)

    def test_answer_modify(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        answer_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANAGER_TOKEN}"}
        data = {"content": "This is a modified test answer."}
        response = self.client().put(
            f"{BASE_URL}/{question_id}/answer/{answer_id}", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

    def test_answer_create(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANAGER_TOKEN}"}
        data = {"content": "This is a test answer."}
        response = self.client().post(
            f"{BASE_URL}/{question_id}/answer", headers=headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 200)

    def test_answer_delete(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        answer_id = 1
        headers = {"Authorization": f"Bearer {MANAGER_TOKEN}"}
        response = self.client().delete(
            f"{BASE_URL}/{question_id}/answer/{answer_id}", headers=headers
        )
        self.assertEqual(response.status_code, 200)

    def test_permission(self):
        self.create_question(username="manager", email="manager@ver.team")

        question_id = 1
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {BOARDER2_TOKEN}"}
        data = {"content": "This is a test answer."}
        response = self.client().post(
            f"{BASE_URL}/{question_id}/answer", headers=headers, data=json.dumps(data)
        )

        # boarder2 does not have "post:answer" permission
        self.assertEqual(response.status_code, 403)

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANAGER_TOKEN}"}
        data = {"content": "This is a test answer."}
        response = self.client().post(
            f"{BASE_URL}/{question_id}/answer", headers=headers, data=json.dumps(data)
        )

        # manager has "post:answer" permission
        self.assertEqual(response.status_code, 200)

    def create_question(self, username, email):
        # test user
        user = User(username=username, email=email, password="password")
        db.session.add(user)
        db.session.commit()

        # test question
        question = Question(
            subject="hello world", content="hello content", create_date=datetime.now(), user=user
        )
        db.session.add(question)
        db.session.commit()

        # test.answer
        answer = Answer(
            content="hello answer", user=user, question=question, create_date=datetime.now()
        )
        db.session.add(answer)
        db.session.commit()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
