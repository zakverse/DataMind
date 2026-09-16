import io
import json
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.tools.dataset_tools import (
    ALL_DATASET_TOOLS,
    categorical_summary_tool,
    correlation_tool,
    dataset_profile_tool,
    missing_values_tool,
    numeric_statistics_tool,
)


class TestPhase4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

        # Upload a standard sample dataset for testing Phase 4
        csv_content = (
            "product,category,price,quantity\n"
            "Laptop,Electronics,10000000,2\n"
            "Mouse,Electronics,150000,10\n"
            "Keyboard,Electronics,300000,5\n"
            "Chair,Furniture,1200000,3\n"
            "Desk,Furniture,2500000,2\n"
        )
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        res = cls.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("sales_phase4.csv", file_obj, "text/csv")},
        )
        assert res.status_code == 201, f"Failed to upload test dataset: {res.text}"
        cls.dataset_id = res.json()["dataset_id"]

    def test_1_all_tools_initialization(self):
        """Test that all 5 LangChain dataset analyst tools are correctly initialized."""
        self.assertEqual(len(ALL_DATASET_TOOLS), 5)
        tool_names = [t.name for t in ALL_DATASET_TOOLS]
        self.assertIn("dataset_profile_tool", tool_names)
        self.assertIn("missing_values_tool", tool_names)
        self.assertIn("numeric_statistics_tool", tool_names)
        self.assertIn("categorical_summary_tool", tool_names)
        self.assertIn("correlation_tool", tool_names)

    def test_2_dataset_profile_tool(self):
        """Test dataset_profile_tool output."""
        res_str = dataset_profile_tool.invoke({"dataset_id": self.dataset_id})
        data = json.loads(res_str)
        self.assertEqual(data["dataset_id"], self.dataset_id)
        self.assertEqual(data["rows"], 5)
        self.assertEqual(data["columns"], 4)
        self.assertIn("price", data["column_names"])
        self.assertIn("product", data["column_names"])

    def test_3_missing_values_tool(self):
        """Test missing_values_tool output."""
        res_str = missing_values_tool.invoke({"dataset_id": self.dataset_id})
        data = json.loads(res_str)
        self.assertEqual(data["total_missing_cells"], 0)
        self.assertEqual(data["overall_missing_percentage"], 0.0)
        self.assertEqual(len(data["columns_with_missing"]), 0)

    def test_4_numeric_statistics_tool(self):
        """Test numeric_statistics_tool output for all columns and specific column."""
        # All columns
        res_all = numeric_statistics_tool.invoke({"dataset_id": self.dataset_id})
        data_all = json.loads(res_all)
        self.assertIn("price", data_all)
        self.assertIn("quantity", data_all)
        self.assertIn("mean", data_all["price"])

        # Specific column
        res_col = numeric_statistics_tool.invoke({"dataset_id": self.dataset_id, "column": "price"})
        data_col = json.loads(res_col)
        self.assertIn("price", data_col)
        self.assertEqual(data_col["price"]["min"], 150000.0)
        self.assertEqual(data_col["price"]["max"], 10000000.0)

    def test_5_categorical_summary_tool(self):
        """Test categorical_summary_tool output."""
        res_str = categorical_summary_tool.invoke({"dataset_id": self.dataset_id})
        data = json.loads(res_str)
        self.assertIn("category", data)
        self.assertIn("Electronics", data["category"]["top_values"])

    def test_6_correlation_tool(self):
        """Test correlation_tool output."""
        res_str = correlation_tool.invoke({"dataset_id": self.dataset_id})
        data = json.loads(res_str)
        self.assertIn("price", data)
        self.assertIn("quantity", data["price"])

    def test_7_agent_numeric_question_and_tool_trace(self):
        """Test agent answering a numeric question and recording tools_used."""
        # Test endpoint with agent execution (mocked to protect live Gemini rate limits)
        with patch(
            "backend.app.agents.analyst_agent.dataset_analyst_agent.run",
            return_value=(
                "Rata-rata harga produk adalah 2,830,000.",
                ["numeric_statistics_tool"],
                "gemini-3.6-flash",
            ),
        ):
            payload = {"question": "Berapa rata-rata harga (price) produk pada dataset ini?"}
            response = self.client.post(
                f"/api/v1/ai/datasets/{self.dataset_id}/ask",
                json=payload,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["dataset_id"], self.dataset_id)
            self.assertEqual(data["status"], "success")
            self.assertIn("2,830,000", data["answer"])
            self.assertIn("numeric_statistics_tool", data["tools_used"])

    def test_8_agent_missing_values_question(self):
        """Test agent answering a missing values question with tool trace."""
        with patch(
            "backend.app.agents.analyst_agent.dataset_analyst_agent.run",
            return_value=(
                "Tidak ada missing values pada dataset ini (0 missing cells).",
                ["missing_values_tool"],
                "gemini-3.6-flash",
            ),
        ):
            payload = {"question": "Apakah terdapat missing values pada dataset ini?"}
            response = self.client.post(
                f"/api/v1/ai/datasets/{self.dataset_id}/ask",
                json=payload,
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertIn("missing_values_tool", data["tools_used"])

    def test_9_agent_invalid_dataset_id_returns_404(self):
        """Test that asking about a nonexistent dataset ID returns 404."""
        payload = {"question": "Berapa jumlah barisnya?"}
        response = self.client.post(
            "/api/v1/ai/datasets/non_existent_dataset_id_9999/ask",
            json=payload,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("tidak ditemukan", response.json()["detail"].lower())

    def test_10_dataset_without_numeric_columns_handling(self):
        """Test tools behavior when dataset has no numeric columns."""
        csv_no_num = "city,country\nJakarta,Indonesia\nTokyo,Japan\n"
        upload_res = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("no_numeric.csv", io.BytesIO(csv_no_num.encode("utf-8")), "text/csv")},
        )
        no_num_id = upload_res.json()["dataset_id"]

        corr_res = correlation_tool.invoke({"dataset_id": no_num_id})
        self.assertIn("Insufficient", corr_res)

        num_res = numeric_statistics_tool.invoke({"dataset_id": no_num_id})
        self.assertIn("No numeric", num_res)


if __name__ == "__main__":
    unittest.main()
