import unittest

from corbado_python_sdk import Config


class TestConfig(unittest.TestCase):

    def test_set_frontend_api(self):

        for frontend_api, valid in self.provide_urls():
            try:
                Config(
                    project_id="pro-123",
                    api_secret="corbado1_123",
                    frontend_api=frontend_api,
                    backend_api="https://backendapi.cloud.corbado.io",
                )
                error = False
            except ValueError:
                error = True
            self.assertEqual(valid, not error)

    def test_set_backend_api(self):
        for backend_api, valid in self.provide_urls():
            try:
                config = Config(
                    project_id="pro-123", api_secret="corbado1_123", backend_api=backend_api, frontend_api="https://test.com"
                )
                config.backend_api = backend_api
                error = False
            except ValueError:
                error = True
            self.assertEqual(valid, second=not error)

    def test_get_backend_api(self):
        test_url = "https://backendapi.cloud.corbado.io"
        config = Config(project_id="pro-123", api_secret="corbado1_123", frontend_api="https://test.com", backend_api=test_url)
        self.assertTrue(config.backend_api.endswith("/v2"))

    def provide_urls(self):
        return [
            ("", False),
            ("xxx", False),
            ("http://auth.acme.com", False),  # Only HTTPS
            ("https://user@auth.acme.com", False),  # No user
            ("https://user:pass@auth.acme.com", False),  # No user no password
            ("https://auth.acme.com/", False),  # No path
            ("https://auth.acme.com?xxx", False),  # No query string
            ("https://auth.acme.com#xxx", False),  # No fragment
            ("https://auth.acme.com", True),
        ]


if __name__ == "__main__":
    unittest.main()
