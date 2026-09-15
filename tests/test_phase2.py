import io
import unittest
from fastapi.testclient import TestClient
from backend.app.main import app


class TestPhase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_upload_valid_csv(self):
        """Test uploading a standard valid CSV dataset."""
        csv_content = (
            "product_id,product_name,category,price,quantity,sales_date\n"
            "1,Laptop,Electronics,1200.0,5,2026-01-15\n"
            "2,Mouse,Electronics,25.5,50,2026-01-16\n"
            "3,Desk,Furniture,350.0,10,2026-01-17\n"
            "4,Chair,Furniture,150.0,20,2026-01-18\n"
            "5,Headphones,Electronics,80.0,30,2026-01-19\n"
        )
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("sales_data.csv", file_obj, "text/csv")},
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("dataset_id", data)
        self.assertEqual(data["filename"], "sales_data.csv")
        self.assertEqual(data["rows"], 5)
        self.assertEqual(data["columns"], 6)

        profile = data["profile"]
        self.assertEqual(len(profile["columns_info"]), 6)
        self.assertIn("price", profile["numeric_summary"])
        self.assertIn("category", profile["categorical_summary"])
        self.assertEqual(len(profile["sample_preview"]), 5)

        # Verify we can also retrieve it via GET /api/v1/datasets/{dataset_id}
        dataset_id = data["dataset_id"]
        get_response = self.client.get(f"/api/v1/datasets/{dataset_id}")
        self.assertEqual(get_response.status_code, 200)
        get_data = get_response.json()
        self.assertEqual(get_data["dataset_id"], dataset_id)
        self.assertEqual(get_data["rows"], 5)

    def test_upload_non_csv_file(self):
        """Test uploading a non-CSV file returns 400 Bad Request."""
        text_content = "This is a plain text file, not CSV."
        file_obj = io.BytesIO(text_content.encode("utf-8"))
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("document.txt", file_obj, "text/plain")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("detail", response.json())

    def test_upload_empty_csv(self):
        """Test uploading an empty CSV returns 400 Bad Request."""
        file_obj = io.BytesIO(b"")
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("empty.csv", file_obj, "text/csv")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("kosong", response.json()["detail"].lower())

    def test_dataset_with_missing_and_duplicates(self):
        """Test dataset containing missing values (nulls) and duplicate rows."""
        csv_content = (
            "id,age,city,income\n"
            "1,25,Jakarta,5000\n"
            "2,,Surabaya,7000\n"
            "3,30,,8500\n"
            "1,25,Jakarta,5000\n"  # duplicate row
        )
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("customers.csv", file_obj, "text/csv")},
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        profile = data["profile"]

        # Rows and Duplicates
        self.assertEqual(profile["rows"], 4)
        self.assertEqual(profile["duplicate_summary"]["duplicate_rows"], 1)
        self.assertEqual(profile["duplicate_summary"]["duplicate_percentage"], 25.0)

        # Missing values
        self.assertEqual(profile["missing_summary"]["total_missing_cells"], 2)
        self.assertIn("age", profile["missing_summary"]["columns_with_missing"])
        self.assertIn("city", profile["missing_summary"]["columns_with_missing"])

    def test_dataset_without_numeric_columns(self):
        """Test dataset that has only categorical/text columns (no numeric columns)."""
        csv_content = (
            "department,status,country\n"
            "Sales,Active,Indonesia\n"
            "Marketing,Active,Singapore\n"
            "Engineering,Inactive,Indonesia\n"
        )
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("departments.csv", file_obj, "text/csv")},
        )
        self.assertEqual(response.status_code, 201)
        profile = response.json()["profile"]

        self.assertEqual(len(profile["column_types"]["numeric"]), 0)
        self.assertEqual(len(profile["column_types"]["categorical"]), 3)
        self.assertEqual(profile["numeric_summary"], {})
        self.assertEqual(profile["correlation"], {})
        self.assertIn("department", profile["categorical_summary"])

    def test_dataset_single_column(self):
        """Test dataset with a single column."""
        csv_content = "score\n100\n95\n80\n"
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        response = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("scores.csv", file_obj, "text/csv")},
        )
        self.assertEqual(response.status_code, 201)
        profile = response.json()["profile"]
        self.assertEqual(profile["columns"], 1)
        self.assertEqual(profile["rows"], 3)
        self.assertIn("score", profile["numeric_summary"])

    def test_dataset_not_found(self):
        """Test GET dataset with nonexistent ID returns 404."""
        response = self.client.get("/api/v1/datasets/non_existent_uuid_12345")
        self.assertEqual(response.status_code, 404)
        self.assertIn("tidak ditemukan", response.json()["detail"].lower())

    def test_dataset_preview_endpoint(self):
        """Test GET preview endpoint returns top sample rows."""
        csv_content = "col_a,col_b\n1,a\n2,b\n3,c\n4,d\n5,e\n6,f\n"
        file_obj = io.BytesIO(csv_content.encode("utf-8"))
        res_upload = self.client.post(
            "/api/v1/datasets/upload",
            files={"file": ("sample.csv", file_obj, "text/csv")},
        )
        dataset_id = res_upload.json()["dataset_id"]

        preview_res = self.client.get(f"/api/v1/datasets/{dataset_id}/preview")
        self.assertEqual(preview_res.status_code, 200)
        rows = preview_res.json()
        self.assertEqual(len(rows), 5)  # Should return top 5 rows


if __name__ == "__main__":
    unittest.main()
