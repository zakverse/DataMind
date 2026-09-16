import {
  DatasetAskRequest,
  DatasetAskResponse,
  DatasetProfileResponse,
  DatasetUploadResponse,
} from "../types/dataset";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
    this.name = "ApiError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorDetail = `Request failed with status ${response.status}`;
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorJson.message || errorDetail;
    } catch {
      // Ignore fallback if not json
    }
    throw new ApiError(response.status, errorDetail);
  }
  return response.json();
}

/**
 * Uploads a CSV file to the DataMind backend and returns the initial profiling response.
 */
export async function uploadDataset(file: File): Promise<DatasetUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/v1/datasets/upload`, {
    method: "POST",
    body: formData,
  });

  return handleResponse<DatasetUploadResponse>(response);
}

/**
 * Retrieves the full EDA profile and statistics for a given dataset ID.
 */
export async function getDatasetProfile(
  datasetId: string
): Promise<DatasetProfileResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/datasets/${encodeURIComponent(datasetId)}`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    }
  );

  return handleResponse<DatasetProfileResponse>(response);
}

/**
 * Retrieves the first sample rows of a dataset.
 */
export async function getDatasetPreview(
  datasetId: string
): Promise<Record<string, string | number | boolean | null>[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/datasets/${encodeURIComponent(datasetId)}/preview`,
    {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    }
  );

  return handleResponse<Record<string, string | number | boolean | null>[]>(
    response
  );
}

/**
 * Sends a natural language question about a specific dataset to the AI Assistant.
 */
export async function askDatasetAI(
  datasetId: string,
  question: string,
  model?: string
): Promise<DatasetAskResponse> {
  const payload: DatasetAskRequest = {
    question: question.trim(),
    model,
  };

  const response = await fetch(
    `${API_BASE_URL}/api/v1/ai/datasets/${encodeURIComponent(datasetId)}/ask`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  return handleResponse<DatasetAskResponse>(response);
}

/**
 * Checks system health status.
 */
export async function checkSystemHealth(): Promise<{
  status: string;
  app_name: string;
  version: string;
  llm_configured: boolean;
}> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  });

  return handleResponse(response);
}
