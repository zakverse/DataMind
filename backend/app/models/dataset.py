from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    """Information for a single column in the dataset."""

    name: str = Field(..., description="Name of the column")
    data_type: str = Field(..., description="Inferred pandas data type")
    missing_count: int = Field(..., description="Number of missing (null/NaN) values")
    missing_percentage: float = Field(..., description="Percentage of missing values (0-100)")
    unique_count: int = Field(..., description="Number of distinct unique values")
    is_numeric: bool = Field(..., description="Whether column is numeric")
    is_categorical: bool = Field(..., description="Whether column is categorical or string")
    is_datetime: bool = Field(..., description="Whether column is datetime")


class MissingSummary(BaseModel):
    """Overview of missing values across the dataset."""

    total_missing_cells: int = Field(..., description="Total count of null cells in the dataset")
    total_cells: int = Field(..., description="Total cells (rows * columns)")
    overall_missing_percentage: float = Field(..., description="Overall missing values percentage (0-100)")
    columns_with_missing: List[str] = Field(default_factory=list, description="List of columns containing missing values")


class DuplicateSummary(BaseModel):
    """Overview of duplicate rows in the dataset."""

    duplicate_rows: int = Field(..., description="Count of duplicate rows")
    duplicate_percentage: float = Field(..., description="Percentage of duplicate rows (0-100)")


class ColumnTypes(BaseModel):
    """Grouping of columns by their detected data types."""

    numeric: List[str] = Field(default_factory=list, description="List of numeric columns")
    categorical: List[str] = Field(default_factory=list, description="List of categorical/text columns")
    datetime: List[str] = Field(default_factory=list, description="List of datetime columns")
    boolean: List[str] = Field(default_factory=list, description="List of boolean columns")


class DatasetProfileResponse(BaseModel):
    """Complete dataset profiling and automated EDA response."""

    dataset_id: str = Field(..., description="Unique dataset identifier (UUID)")
    filename: str = Field(..., description="Original filename of the uploaded dataset")
    file_size_bytes: int = Field(..., description="Size of the uploaded file in bytes")
    rows: int = Field(..., description="Total number of rows")
    columns: int = Field(..., description="Total number of columns")
    columns_info: List[ColumnInfo] = Field(..., description="Detailed profile for each column")
    column_types: ColumnTypes = Field(..., description="Categorization of column names by type")
    missing_summary: MissingSummary = Field(..., description="Summary of missing values")
    duplicate_summary: DuplicateSummary = Field(..., description="Summary of duplicate rows")
    numeric_summary: Dict[str, Dict[str, Optional[float]]] = Field(
        default_factory=dict,
        description="Statistical summary metrics for numeric columns (mean, std, min, 25%, 50%, 75%, max)",
    )
    categorical_summary: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Distribution and unique counts for categorical columns",
    )
    correlation: Dict[str, Dict[str, Optional[float]]] = Field(
        default_factory=dict,
        description="Pearson correlation matrix for numeric columns",
    )
    sample_preview: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="First 5 rows of the dataset for quick UI preview",
    )


class DatasetUploadResponse(BaseModel):
    """Response returned upon successful CSV upload."""

    message: str = Field(default="Dataset uploaded and profiled successfully")
    dataset_id: str = Field(..., description="Unique dataset identifier")
    filename: str = Field(..., description="Uploaded filename")
    rows: int = Field(..., description="Total rows in dataset")
    columns: int = Field(..., description="Total columns in dataset")
    profile: DatasetProfileResponse = Field(..., description="Complete profiling & EDA data")
