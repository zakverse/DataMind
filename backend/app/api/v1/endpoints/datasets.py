from typing import Any, List
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.app.models.dataset import DatasetProfileResponse, DatasetUploadResponse
from backend.app.services.dataset_service import dataset_service

router = APIRouter()


@router.post(
    "/upload",
    response_model=DatasetUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and profile CSV dataset",
)
async def upload_dataset(file: UploadFile = File(...)) -> DatasetUploadResponse:
    """Uploads a CSV file, validates its structure, performs automated profiling,

    and stores it for downstream analytics.
    """
    try:
        result = await dataset_service.save_and_profile_upload(file)
        return result
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan saat memproses dataset: {exc}",
        ) from exc


@router.get(
    "/{dataset_id}",
    response_model=DatasetProfileResponse,
    summary="Get dataset profiling and EDA summary",
)
def get_dataset(dataset_id: str) -> DatasetProfileResponse:
    """Retrieves full profiling and automated exploratory data analysis (EDA) for the given dataset ID."""
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        return profile
    except FileNotFoundError as fnf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(fnf),
        ) from fnf
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal memuat profiling dataset: {exc}",
        ) from exc


@router.get(
    "/{dataset_id}/preview",
    response_model=List[dict[str, Any]],
    summary="Get dataset preview sample rows",
)
def get_dataset_preview(dataset_id: str) -> List[dict[str, Any]]:
    """Returns the top 5 sample rows for quick UI preview."""
    profile = get_dataset(dataset_id)
    return profile.sample_preview
