from app import app
import unittest


class TestViews(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        assert statuscode == 200


if __name__ == '__main__':
    unittest.main()
