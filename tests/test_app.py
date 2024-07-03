import unittest
import json
from main import app, get_db


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config["DATABASE"] = "test.db"
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            db = get_db()
            db.execute("DROP TABLE IF EXISTS tips")
            db.execute("""
                    CREATE TABLE tips (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT,
                        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        author TEXT
                    )
                """)
            db.commit()

    def tearDown(self):
        with app.app_context():
            db = get_db()
            db.execute("DROP TABLE IF EXISTS tips")
            db.commit()

    def test_add_tip(self):
        # Test adding a tip
        response = self.app.post("/tips", data=json.dumps({
            "title": "Test Tip",
            "content": "This is a test tip.",
            "category": "General",
            "author": "test_user"
        }), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Tip added successfully", response.data)

    def test_read_all_tips(self):
        self.app.post("/tips", data=json.dumps({
            "title": "Test Tip",
            "content": "This is a test tip.",
            "category": "General",
            "author": "test_user"
        }), content_type="application/json")

        response = self.app.get("/tips")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Tip", response.data)

    def test_get_random_tip(self):
        self.app.post("/tips", data=json.dumps({
            "title": "Test Tip",
            "content": "This is a test tip.",
            "category": "General",
            "author": "test_user"
        }), content_type="application/json")

        response = self.app.get("/random_tip")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Tip", response.data)

    def test_delete_tip(self):
        self.app.post("/tips", data=json.dumps({
            "title": "Test Tip",
            "content": "This is a test tip.",
            "category": "General",
            "author": "test_user"
        }), content_type="application/json")

        response = self.app.delete(
            "/delete_tip/1", headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tip deleted successfully", response.data)


if __name__ == "__main__":
    unittest.main()
