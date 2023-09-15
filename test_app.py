import unittest
from app import app


class TestCurrencyConverterApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_conversion(self):
        response = self.app.post(
            "/", data={"from_currency": "USD", "to_currency": "USD", "amount": "1"}
        )
        self.assertEqual(response.status_code, 200)

        # Extract the conversion result from the response
        result = response.data.decode("utf-8")

        # Check if the expected information is present in the response
        self.assertIn("1 USD =", result)
        self.assertIn("1.0 USD", result)

    def test_invalid_input(self):
        response = self.app.post(
            "/", data={"from_currency": "", "to_currency": "EUR", "amount": "10"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid input", response.data)


if __name__ == "__main__":
    unittest.main()
