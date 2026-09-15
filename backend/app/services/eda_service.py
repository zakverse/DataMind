import logging
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd

from backend.app.models.dataset import (
    ColumnInfo,
    ColumnTypes,
    DatasetProfileResponse,
    DuplicateSummary,
    MissingSummary,
)
from backend.app.utils.data_helpers import sanitize_val

logger = logging.getLogger(__name__)


class EDAService:
    """Service for exploratory data analysis and dataset profiling."""

    def profile_dataframe(
        self,
        df: pd.DataFrame,
        dataset_id: str,
        filename: str,
        file_size_bytes: int,
    ) -> DatasetProfileResponse:
        """Generates a complete dataset profile and EDA summary from a Pandas DataFrame."""
        total_rows, total_cols = df.shape
        total_cells = total_rows * total_cols

        # Identify Column Types
        numeric_cols: List[str] = []
        categorical_cols: List[str] = []
        datetime_cols: List[str] = []
        boolean_cols: List[str] = []

        for col in df.columns:
            dtype = df[col].dtype
            if pd.api.types.is_bool_dtype(dtype):
                boolean_cols.append(col)
            elif pd.api.types.is_numeric_dtype(dtype):
                numeric_cols.append(col)
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                datetime_cols.append(col)
            else:
                categorical_cols.append(col)

        column_types = ColumnTypes(
            numeric=numeric_cols,
            categorical=categorical_cols,
            datetime=datetime_cols,
            boolean=boolean_cols,
        )

        # Columns detailed information
        columns_info: List[ColumnInfo] = []
        columns_with_missing: List[str] = []
        total_missing_cells = 0

        for col in df.columns:
            missing_count = int(df[col].isna().sum())
            missing_pct = round((missing_count / total_rows * 100), 2) if total_rows > 0 else 0.0
            unique_count = int(df[col].nunique(dropna=False))

            if missing_count > 0:
                columns_with_missing.append(col)
                total_missing_cells += missing_count

            is_num = col in numeric_cols
            is_cat = col in categorical_cols
            is_dt = col in datetime_cols

            columns_info.append(
                ColumnInfo(
                    name=str(col),
                    data_type=str(df[col].dtype),
                    missing_count=missing_count,
                    missing_percentage=missing_pct,
                    unique_count=unique_count,
                    is_numeric=is_num,
                    is_categorical=is_cat,
                    is_datetime=is_dt,
                )
            )

        # Missing Summary
        overall_missing_pct = (
            round((total_missing_cells / total_cells * 100), 2) if total_cells > 0 else 0.0
        )
        missing_summary = MissingSummary(
            total_missing_cells=total_missing_cells,
            total_cells=total_cells,
            overall_missing_percentage=overall_missing_pct,
            columns_with_missing=columns_with_missing,
        )

        # Duplicate Summary
        duplicate_rows = int(df.duplicated().sum()) if total_rows > 0 else 0
        duplicate_pct = (
            round((duplicate_rows / total_rows * 100), 2) if total_rows > 0 else 0.0
        )
        duplicate_summary = DuplicateSummary(
            duplicate_rows=duplicate_rows,
            duplicate_percentage=duplicate_pct,
        )

        # Numeric Statistics Summary
        numeric_summary: Dict[str, Dict[str, Optional[float]]] = {}
        if numeric_cols and total_rows > 0:
            for col in numeric_cols:
                series = df[col].dropna()
                if not series.empty:
                    numeric_summary[col] = {
                        "count": float(len(series)),
                        "mean": sanitize_val(round(float(series.mean()), 4)),
                        "std": sanitize_val(round(float(series.std()), 4)) if len(series) > 1 else None,
                        "min": sanitize_val(round(float(series.min()), 4)),
                        "25%": sanitize_val(round(float(series.quantile(0.25)), 4)),
                        "50%": sanitize_val(round(float(series.median()), 4)),
                        "75%": sanitize_val(round(float(series.quantile(0.75)), 4)),
                        "max": sanitize_val(round(float(series.max()), 4)),
                    }
                else:
                    numeric_summary[col] = {
                        "count": 0.0,
                        "mean": None,
                        "std": None,
                        "min": None,
                        "25%": None,
                        "50%": None,
                        "75%": None,
                        "max": None,
                    }

        # Categorical Summary
        categorical_summary: Dict[str, Dict[str, Any]] = {}
        if categorical_cols and total_rows > 0:
            for col in categorical_cols:
                series = df[col].dropna().astype(str)
                top_values = series.value_counts().head(5).to_dict()
                categorical_summary[col] = {
                    "unique_count": int(df[col].nunique()),
                    "top_values": {str(k): int(v) for k, v in top_values.items()},
                }

        # Correlation Matrix (only if >= 2 numeric columns)
        correlation: Dict[str, Dict[str, Optional[float]]] = {}
        if len(numeric_cols) >= 2 and total_rows > 1:
            try:
                corr_df = df[numeric_cols].corr(method="pearson")
                for col_a in numeric_cols:
                    correlation[col_a] = {}
                    for col_b in numeric_cols:
                        val = corr_df.loc[col_a, col_b]
                        correlation[col_a][col_b] = sanitize_val(round(float(val), 4)) if pd.notna(val) else None
            except Exception as exc:
                logger.warning(f"Failed to calculate correlation: {exc}")
                correlation = {}

        # Sample Preview (first 5 rows)
        sample_preview = []
        if total_rows > 0:
            head_df = df.head(5)
            # Replace NaNs with None for preview
            preview_records = head_df.to_dict(orient="records")
            sample_preview = [
                {str(k): sanitize_val(v) for k, v in row.items()} for row in preview_records
            ]

        return DatasetProfileResponse(
            dataset_id=dataset_id,
            filename=filename,
            file_size_bytes=file_size_bytes,
            rows=total_rows,
            columns=total_cols,
            columns_info=columns_info,
            column_types=column_types,
            missing_summary=missing_summary,
            duplicate_summary=duplicate_summary,
            numeric_summary=numeric_summary,
            categorical_summary=categorical_summary,
            correlation=correlation,
            sample_preview=sample_preview,
        )


eda_service = EDAService()
