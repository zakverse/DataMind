import math
from typing import Any
import numpy as np
import pandas as pd


def sanitize_val(val: Any) -> Any:
    """Recursively sanitize numpy/pandas scalar values, NaNs, and Infs for JSON compliance."""
    if val is None or (isinstance(val, (float, np.floating)) and (math.isnan(val) or math.isinf(val))):
        return None
    if isinstance(val, (pd.Timestamp, pd.Timedelta)):
        return str(val)
    if isinstance(val, (np.integer, np.int64, np.int32)):
        return int(val)
    if isinstance(val, (np.floating, np.float64, np.float32)):
        return float(val)
    if isinstance(val, (np.bool_, bool)):
        return bool(val)
    if isinstance(val, dict):
        return {k: sanitize_val(v) for k, v in val.items()}
    if isinstance(val, (list, tuple)):
        return [sanitize_val(v) for v in val]
    return val


def sanitize_dict(d: dict) -> dict:
    """Sanitize all values in a dictionary."""
    return {k: sanitize_val(v) for k, v in d.items()}
