import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app


class TestPhase1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        """Test GET / returns valid app metadata."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["app_name"], "DataMind API")
        self.assertIn("version", data)
        self.assertIn("health_check", data)

    def test_health_endpoint(self):
        """Test GET /api/v1/health returns ok status."""
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertTrue(data["llm_configured"])

    def test_ai_ask_get_endpoint(self):
        """Test GET /api/v1/ai/ask with query param."""
        with patch("backend.app.services.ai_service.ai_service.ask", return_value="Hasilnya adalah 2"):
            response = self.client.get("/api/v1/ai/ask?question=Sebutkan+1+tambah+1+dalam+angka")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertIn("2", data["answer"])
            self.assertIn("model_used", data)

    def test_ai_ask_post_endpoint(self):
        """Test POST /api/v1/ai/ask with JSON body."""
        with patch("backend.app.services.ai_service.ai_service.ask", return_value="Saya siap membantu analisis data Anda."):
            payload = {"question": "Apakah kamu siap membantu analisis data?"}
            response = self.client.post("/api/v1/ai/ask", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertGreater(len(data["answer"]), 0)

    def test_compatibility_ask_endpoint(self):
        """Test GET /ask backwards compatibility route."""
        with patch("backend.app.main.ask_gemini", return_value="Halo! Ada yang bisa saya bantu?"):
            response = self.client.get("/ask?question=Halo")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["question"], "Halo")
            self.assertGreater(len(data["answer"]), 0)


if __name__ == "__main__":
    unittest.main()
