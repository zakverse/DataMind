import io
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.dataset_service import dataset_service
from backend.app.tools.dataset_tools import (
    build_dataset_context,
    get_categorical_summary,
    get_correlation_matrix,
    get_dataset_profile,
    get_missing_values,
    get_numeric_statistics,
)


class TestPhase3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

        # Upload a standard sample dataset for testing
        csv_content = (
            "product_id,product_name,category,price,quantity\n"
            "1,Laptop,Electronics,1200.0,5\n"
            "2,Mouse,Electronics,25.0,50\n"
            "3,Desk,Furniture,350.0,10\n"
            "4,Chair,Furniture,150.0,20\n"
        )
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        res = cls.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("ecommerce_test.csv", file_obj, "text/csv")},
        )
        assert res.status_code == 201, f"Failed to upload test dataset: {res.text}"
        cls.dataset_id = res.json()["dataset_id"]

    def test_build_dataset_context_structure(self):
        """Test that build_dataset_context creates rich, valid Markdown context."""
        profile = dataset_service.get_dataset_profile(self.dataset_id)
        context = build_dataset_context(profile)

        self.assertIn("Dataset Overview", context)
        self.assertIn("Column Categorization", context)
        self.assertIn("Descriptive Numerical Statistics", context)
        self.assertIn("price", context)
        self.assertIn("category", context)

    def test_dataset_tools_execution(self):
        """Test individual LangChain dataset tools invocation."""
        profile_res = get_dataset_profile.invoke({"dataset_id": self.dataset_id})
        self.assertIn("ecommerce_test.csv", profile_res)

        stats_res = get_numeric_statistics.invoke({"dataset_id": self.dataset_id})
        self.assertIn("price", stats_res)
        self.assertIn("mean", stats_res)

        missing_res = get_missing_values.invoke({"dataset_id": self.dataset_id})
        self.assertIn("total_missing_cells", missing_res)

        corr_res = get_correlation_matrix.invoke({"dataset_id": self.dataset_id})
        self.assertIn("price", corr_res)

        cat_res = get_categorical_summary.invoke({"dataset_id": self.dataset_id})
        self.assertIn("category", cat_res)

    def test_ask_dataset_success(self):
        """Test asking a dataset-grounded question via POST endpoint."""
        with patch(
            "backend.app.services.ai_service.ai_service.ask_dataset",
            return_value=(
                "Rata-rata harga produk adalah 431.25.",
                ["numeric_statistics_tool"],
                "gemini-3.6-flash",
            ),
        ):
            payload = {"question": "Berapa rata-rata harga produk pada dataset ini?"}
            response = self.client.post(
                f"/api/v1/ai/datasets/{self.dataset_id}/ask",
                json=payload,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["dataset_id"], self.dataset_id)
            self.assertEqual(data["question"], payload["question"])
            self.assertEqual(data["status"], "success")
            self.assertIn("model_used", data)
            self.assertGreater(len(data["answer"]), 0)

    def test_ask_dataset_not_found(self):
        """Test asking a question about a nonexistent dataset ID returns 404."""
        payload = {"question": "Apa isi dataset ini?"}
        response = self.client.post(
            "/api/v1/ai/datasets/non_existent_id_99999/ask",
            json=payload,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("tidak ditemukan", response.json()["detail"].lower())

    def test_ask_dataset_empty_question_validation(self):
        """Test sending an empty question returns validation error (422)."""
        payload = {"question": ""}
        response = self.client.post(
            f"/api/v1/ai/datasets/{self.dataset_id}/ask",
            json=payload,
        )
        self.assertEqual(response.status_code, 422)

    def test_ask_dataset_missing_values_question(self):
        """Test asking about missing values in a dataset that has nulls."""
        # Upload a dataset with missing values
        csv_with_missing = (
            "name,score,age\n"
            "Alice,95,\n"
            "Bob,,22\n"
            "Charlie,80,25\n"
        )
        upload_res = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("missing_test.csv", io.BytesIO(csv_with_missing.encode("utf-8")), "text/csv")},
        )
        missing_dataset_id = upload_res.json()["dataset_id"]

        with patch(
            "backend.app.services.ai_service.ai_service.ask_dataset",
            return_value=(
                "Kolom score dan age memiliki missing values.",
                ["missing_values_tool"],
                "gemini-3.6-flash",
            ),
        ):
            payload = {"question": "Kolom mana saja yang memiliki missing values?"}
            response = self.client.post(
                f"/api/v1/ai/datasets/{missing_dataset_id}/ask",
                json=payload,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertGreater(len(data["answer"]), 0)


if __name__ == "__main__":
    unittest.main()
