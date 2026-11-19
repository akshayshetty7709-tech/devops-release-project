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


if __name__ == "__main__":
    unittest.main()
