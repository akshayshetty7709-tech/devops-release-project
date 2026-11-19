import unittest

from app import build_response


class AppTests(unittest.TestCase):
    def test_root(self):
        status, body = build_response("/")
        self.assertEqual(status, 200)
        self.assertEqual(body["app"], "devops-demo")

    def test_health(self):
        status, body = build_response("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body["status"], "ok")

    def test_not_found(self):
        status, _ = build_response("/nope")
        self.assertEqual(status, 404)
   
    def test_version(self):
        status, body = build_response("/version")
        self.assertEqual(status, 200)
        self.assertIn("version",body)

if __name__ == "__main__":
    unittest.main()
