import io
import json
import logging
import uuid
from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
from fastapi import UploadFile

from backend.app.core.config import settings
from backend.app.models.dataset import DatasetProfileResponse, DatasetUploadResponse
from backend.app.services.eda_service import eda_service

logger = logging.getLogger(__name__)


class DatasetService:
    """Service for dataset file handling, validation, storage, and retrieval."""

    def __init__(self, upload_dir: Optional[Path] = None):
        self.upload_dir = upload_dir or settings.UPLOAD_DIR
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def _get_dataset_file_path(self, dataset_id: str) -> Path:
        """Returns the file path for a given dataset ID."""
        return self.upload_dir / f"{dataset_id}.csv"

    def _get_metadata_file_path(self, dataset_id: str) -> Path:
        """Returns the metadata JSON file path for a given dataset ID."""
        return self.upload_dir / f"{dataset_id}_meta.json"

    def validate_and_read_csv(self, file_bytes: bytes, filename: str) -> pd.DataFrame:
        """Validates CSV content and returns a Pandas DataFrame."""
        if not file_bytes or len(file_bytes.strip()) == 0:
            raise ValueError("File CSV kosong (0 bytes). Silakan unggah file CSV yang valid.")

        if not filename.lower().endswith(".csv"):
            raise ValueError("Format file tidak didukung. Harap unggah file dengan format .csv.")

        # Try reading with common encodings
        encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
        df: Optional[pd.DataFrame] = None
        last_error = None

        for enc in encodings:
            try:
                df = pd.read_csv(io.BytesIO(file_bytes), encoding=enc)
                break
            except Exception as e:
                last_error = e

        if df is None:
            raise ValueError(f"Gagal membaca file CSV: Format file rusak atau tidak valid. ({last_error})")

        if df.empty and len(df.columns) == 0:
            raise ValueError("Dataset tidak memiliki baris atau kolom yang valid.")

        return df

    async def save_and_profile_upload(self, file: UploadFile) -> DatasetUploadResponse:
        """Saves uploaded CSV file, profiles the dataset, and stores metadata."""
        filename = file.filename or "uploaded_dataset.csv"

        if not filename.lower().endswith(".csv"):
            raise ValueError("Format file tidak didukung. Harap unggah file berekstensi .csv.")

        file_bytes = await file.read()
        file_size = len(file_bytes)

        # Check maximum file size
        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_bytes:
            raise ValueError(
                f"Ukuran file ({round(file_size / (1024*1024), 2)} MB) melebihi batas maksimum ({settings.MAX_FILE_SIZE_MB} MB)."
            )

        # Validate and parse with Pandas
        df = self.validate_and_read_csv(file_bytes, filename)

        # Generate unique dataset ID
        dataset_id = uuid.uuid4().hex

        # Save CSV to uploads directory
        csv_path = self._get_dataset_file_path(dataset_id)
        with open(csv_path, "wb") as f:
            f.write(file_bytes)

        # Profile Dataset with EDA service
        profile = eda_service.profile_dataframe(
            df=df,
            dataset_id=dataset_id,
            filename=filename,
            file_size_bytes=file_size,
        )

        # Save metadata JSON for fast retrieval
        metadata = {
            "dataset_id": dataset_id,
            "filename": filename,
            "file_size_bytes": file_size,
            "profile": profile.model_dump(),
        }
        meta_path = self._get_metadata_file_path(dataset_id)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        return DatasetUploadResponse(
            message="Dataset uploaded and profiled successfully",
            dataset_id=dataset_id,
            filename=filename,
            rows=profile.rows,
            columns=profile.columns,
            profile=profile,
        )

    def get_dataset_profile(self, dataset_id: str) -> DatasetProfileResponse:
        """Retrieves dataset profiling / EDA summary by dataset ID."""
        meta_path = self._get_metadata_file_path(dataset_id)
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                return DatasetProfileResponse(**metadata["profile"])
            except Exception as e:
                logger.warning(f"Failed to read metadata cache for {dataset_id}: {e}")

        # If metadata cache is missing or corrupt, try regenerating from the CSV file
        csv_path = self._get_dataset_file_path(dataset_id)
        if not csv_path.exists():
            raise FileNotFoundError(f"Dataset dengan ID '{dataset_id}' tidak ditemukan.")

        try:
            df = pd.read_csv(csv_path)
            file_size = csv_path.stat().st_size
            profile = eda_service.profile_dataframe(
                df=df,
                dataset_id=dataset_id,
                filename=f"{dataset_id}.csv",
                file_size_bytes=file_size,
            )
            return profile
        except Exception as e:
            raise RuntimeError(f"Gagal membaca dataset dari disk: {e}") from e

    def load_dataframe(self, dataset_id: str) -> Tuple[pd.DataFrame, str]:
        """Loads the Pandas DataFrame for a dataset ID (returns DataFrame and original filename)."""
        csv_path = self._get_dataset_file_path(dataset_id)
        if not csv_path.exists():
            raise FileNotFoundError(f"Dataset dengan ID '{dataset_id}' tidak ditemukan.")

        filename = f"{dataset_id}.csv"
        meta_path = self._get_metadata_file_path(dataset_id)
        if meta_path.exists():
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    filename = meta.get("filename", filename)
            except Exception:
                pass

        df = pd.read_csv(csv_path)
        return df, filename


dataset_service = DatasetService()
