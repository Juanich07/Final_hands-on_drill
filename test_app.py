import unittest
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_country(self):
        response = self.app.get('/countries/XYZ')
        self.assertEqual(response.status_code, 404)

    # Add more test cases for other API endpoints

if __name__ == '__main__':
    unittest.main()
