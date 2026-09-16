export interface ColumnInfo {
  name: string;
  data_type: string;
  missing_count: number;
  missing_percentage: number;
  unique_count: number;
  is_numeric: boolean;
  is_categorical: boolean;
  is_datetime: boolean;
}

export interface MissingSummary {
  total_missing_cells: number;
  total_cells: number;
  overall_missing_percentage: number;
  columns_with_missing: string[];
}

export interface DuplicateSummary {
  duplicate_rows: number;
  duplicate_percentage: number;
}

export interface ColumnTypes {
  numeric: string[];
  categorical: string[];
  datetime: string[];
  boolean: string[];
}

export interface NumericMetrics {
  count: number;
  mean: number | null;
  std: number | null;
  min: number | null;
  "25%"?: number | null;
  "50%"?: number | null;
  "75%"?: number | null;
  max: number | null;
}

export interface CategoricalMetrics {
  unique_count: number;
  top_values: Record<string, number>;
}

export interface DatasetProfileResponse {
  dataset_id: string;
  filename: string;
  file_size_bytes: number;
  rows: number;
  columns: number;
  columns_info: ColumnInfo[];
  column_types: ColumnTypes;
  missing_summary: MissingSummary;
  duplicate_summary: DuplicateSummary;
  numeric_summary: Record<string, NumericMetrics>;
  categorical_summary: Record<string, CategoricalMetrics>;
  correlation: Record<string, Record<string, number | null>>;
  sample_preview: Record<string, string | number | boolean | null>[];
}

export interface DatasetUploadResponse {
  message: string;
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  profile: DatasetProfileResponse;
}

export interface DatasetAskRequest {
  question: string;
  model?: string;
}

export interface DatasetAskResponse {
  dataset_id: string;
  question: string;
  answer: string;
  tools_used: string[];
  model_used: string;
  status: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
  tools_used?: string[];
  model_used?: string;
}
