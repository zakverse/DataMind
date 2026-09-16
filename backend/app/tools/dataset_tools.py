import json
from typing import List, Optional
from langchain_core.tools import BaseTool, tool
from backend.app.models.dataset import DatasetProfileResponse
from backend.app.services.dataset_service import dataset_service


def build_dataset_context(profile: DatasetProfileResponse) -> str:
    """Builds a compact, structured Markdown summary of the dataset for LLM prompt context."""
    sections: List[str] = []

    # 1. Overview
    sections.append(
        f"**Dataset Overview:**\n"
        f"- Filename: `{profile.filename}`\n"
        f"- Total Rows: {profile.rows:,}\n"
        f"- Total Columns: {profile.columns}\n"
        f"- File Size: {round(profile.file_size_bytes / 1024, 2)} KB"
    )

    # 2. Column Types
    types = profile.column_types
    sections.append(
        f"**Column Categorization:**\n"
        f"- Numeric ({len(types.numeric)}): {', '.join(types.numeric) if types.numeric else 'None'}\n"
        f"- Categorical ({len(types.categorical)}): {', '.join(types.categorical) if types.categorical else 'None'}\n"
        f"- Datetime ({len(types.datetime)}): {', '.join(types.datetime) if types.datetime else 'None'}\n"
        f"- Boolean ({len(types.boolean)}): {', '.join(types.boolean) if types.boolean else 'None'}"
    )

    # 3. Columns Details & Missing Values
    col_details = []
    for c in profile.columns_info:
        col_details.append(
            f"- `{c.name}` ({c.data_type}): {c.missing_count} missing ({c.missing_percentage}%), {c.unique_count} unique values"
        )
    sections.append("**Columns Detail & Missing:**\n" + "\n".join(col_details))

    # 4. Data Quality & Duplicates
    dup = profile.duplicate_summary
    miss = profile.missing_summary
    sections.append(
        f"**Data Quality Summary:**\n"
        f"- Total Missing Cells: {miss.total_missing_cells} ({miss.overall_missing_percentage}% of total cells)\n"
        f"- Columns with Missing Values: {', '.join(miss.columns_with_missing) if miss.columns_with_missing else 'None'}\n"
        f"- Duplicate Rows: {dup.duplicate_rows} ({dup.duplicate_percentage}%)"
    )

    # 5. Numerical Statistics Summary
    if profile.numeric_summary:
        num_lines = []
        for col, stats in profile.numeric_summary.items():
            num_lines.append(
                f"- `{col}` -> Mean: {stats.get('mean')}, Median: {stats.get('50%')}, Std: {stats.get('std')}, "
                f"Min: {stats.get('min')}, 25%: {stats.get('25%')}, 75%: {stats.get('75%')}, Max: {stats.get('max')}"
            )
        sections.append("**Descriptive Numerical Statistics:**\n" + "\n".join(num_lines))
    else:
        sections.append("**Descriptive Numerical Statistics:** No numeric columns present.")

    # 6. Categorical Distributions
    if profile.categorical_summary:
        cat_lines = []
        for col, data in profile.categorical_summary.items():
            top_vals = data.get("top_values", {})
            formatted_top = ", ".join([f"'{k}': {v}" for k, v in top_vals.items()])
            cat_lines.append(
                f"- `{col}` ({data.get('unique_count')} unique) -> Top frequencies: [{formatted_top}]"
            )
        sections.append("**Categorical Column Distributions:**\n" + "\n".join(cat_lines))

    # 7. Correlation Matrix
    if profile.correlation:
        corr_lines = []
        for col_a, relations in profile.correlation.items():
            for col_b, val in relations.items():
                if col_a < col_b and val is not None:
                    corr_lines.append(f"- Correlation(`{col_a}`, `{col_b}`): {val}")
        if corr_lines:
            sections.append("**Pearson Correlation Matrix:**\n" + "\n".join(corr_lines))
        else:
            sections.append("**Pearson Correlation Matrix:** No pairwise correlation available.")
    else:
        sections.append("**Pearson Correlation Matrix:** Insufficient numeric columns for correlation.")

    # 8. Sample Preview
    if profile.sample_preview:
        sample_str = json.dumps(profile.sample_preview[:3], indent=2, ensure_ascii=False)
        sections.append(f"**Sample Preview (First 3 Rows):**\n```json\n{sample_str}\n```")

    return "\n\n".join(sections)


@tool
def dataset_profile_tool(dataset_id: str) -> str:
    """Useful for getting general metadata about the dataset, such as filename, total rows,

    total columns, column names, column data types, and row duplicates.
    Input must be the dataset_id string.
    """
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        result = {
            "dataset_id": profile.dataset_id,
            "filename": profile.filename,
            "rows": profile.rows,
            "columns": profile.columns,
            "column_names": [c.name for c in profile.columns_info],
            "column_types": profile.column_types.model_dump(),
            "duplicate_rows": profile.duplicate_summary.duplicate_rows,
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve dataset profile: {e}"})


@tool
def missing_values_tool(dataset_id: str) -> str:
    """Useful for checking missing (null/NaN) values in the dataset.

    Returns the total missing cells, percentage of missing data, and missing counts per column.
    Input must be the dataset_id string.
    """
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        result = {
            "total_missing_cells": profile.missing_summary.total_missing_cells,
            "overall_missing_percentage": profile.missing_summary.overall_missing_percentage,
            "columns_with_missing": profile.missing_summary.columns_with_missing,
            "missing_per_column": {
                c.name: {
                    "missing_count": c.missing_count,
                    "missing_percentage": c.missing_percentage,
                }
                for c in profile.columns_info
                if c.missing_count > 0
            },
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve missing values: {e}"})


@tool
def numeric_statistics_tool(dataset_id: str, column: Optional[str] = None) -> str:
    """Useful for retrieving descriptive numerical statistics (count, mean, std, min, 25%, 50% median, 75%, max)

    for numeric columns in the dataset.
    Optional 'column' parameter specifies a single column name to retrieve.
    Input: dataset_id (string), column (optional string).
    """
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        if not profile.numeric_summary:
            return json.dumps({"message": "No numeric columns present in this dataset."})

        if column:
            # Case-insensitive column matching
            matched_col = next((c for c in profile.numeric_summary if c.lower() == column.strip().lower()), None)
            if matched_col:
                return json.dumps({matched_col: profile.numeric_summary[matched_col]}, indent=2)
            return json.dumps({
                "error": f"Column '{column}' is not a numeric column in the dataset.",
                "available_numeric_columns": list(profile.numeric_summary.keys()),
            })

        return json.dumps(profile.numeric_summary, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve numeric statistics: {e}"})


@tool
def categorical_summary_tool(dataset_id: str, column: Optional[str] = None) -> str:
    """Useful for retrieving summaries of categorical or text columns, including distinct unique count

    and top most frequent values/categories.
    Optional 'column' parameter specifies a single column name to retrieve.
    Input: dataset_id (string), column (optional string).
    """
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        if not profile.categorical_summary:
            return json.dumps({"message": "No categorical columns present in this dataset."})

        if column:
            matched_col = next((c for c in profile.categorical_summary if c.lower() == column.strip().lower()), None)
            if matched_col:
                return json.dumps({matched_col: profile.categorical_summary[matched_col]}, indent=2)
            return json.dumps({
                "error": f"Column '{column}' is not a categorical column in the dataset.",
                "available_categorical_columns": list(profile.categorical_summary.keys()),
            })

        return json.dumps(profile.categorical_summary, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve categorical summary: {e}"})


@tool
def correlation_tool(dataset_id: str) -> str:
    """Useful for retrieving the Pearson correlation matrix between numeric columns in the dataset

    to understand linear relationships, dependencies, and patterns between variables.
    Input must be the dataset_id string.
    """
    try:
        profile = dataset_service.get_dataset_profile(dataset_id)
        if not profile.correlation:
            return json.dumps({"message": "Insufficient numeric columns to compute correlation matrix."})
        return json.dumps(profile.correlation, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve correlation matrix: {e}"})


# Phase 4 Dataset Analyst Tools
ALL_DATASET_TOOLS: List[BaseTool] = [
    dataset_profile_tool,
    missing_values_tool,
    numeric_statistics_tool,
    categorical_summary_tool,
    correlation_tool,
]

# Aliases for Phase 3 backward compatibility
get_dataset_profile = dataset_profile_tool
get_missing_values = missing_values_tool
get_numeric_statistics = numeric_statistics_tool
get_categorical_summary = categorical_summary_tool
get_correlation_matrix = correlation_tool
DATASET_TOOLS = ALL_DATASET_TOOLS
