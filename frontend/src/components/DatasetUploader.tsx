"use client";

import React, { useState, useRef } from "react";
import {
  UploadCloud,
  FileSpreadsheet,
  AlertCircle,
  Loader2,
  CheckCircle2,
  FileText,
  Sparkles,
} from "lucide-react";
import { uploadDataset } from "../services/api";
import { DatasetProfileResponse } from "../types/dataset";

interface DatasetUploaderProps {
  onUploadSuccess: (profile: DatasetProfileResponse) => void;
}

export const DatasetUploader: React.FC<DatasetUploaderProps> = ({
  onUploadSuccess,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const validateAndSetFile = (selectedFile: File) => {
    setError(null);
    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Format file tidak didukung. Harap pilih file dengan ekstensi .csv");
      return;
    }
    if (selectedFile.size === 0) {
      setError("File CSV kosong (0 bytes). Harap pilih file yang berisi data.");
      return;
    }
    setFile(selectedFile);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await uploadDataset(file);
      onUploadSuccess(response.profile);
    } catch (err: any) {
      setError(
        err.detail || err.message || "Gagal mengunggah dan memproses dataset. Pastikan backend aktif."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadSample = async () => {
    const sampleCsv = `product,category,price,quantity
Laptop,Electronics,10000000,2
Mouse,Electronics,150000,10
Keyboard,Electronics,300000,5
Chair,Furniture,1200000,3
Desk,Furniture,2500000,2
Monitor,Electronics,2100000,4
Headset,Electronics,450000,8
Bookshelf,Furniture,1800000,2
`;
    const sampleBlob = new Blob([sampleCsv], { type: "text/csv" });
    const sampleFile = new File([sampleBlob], "sample_supermarket_sales.csv", {
      type: "text/csv",
    });
    setFile(sampleFile);
    setError(null);
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-8 sm:p-12 text-center transition-all duration-200 ${
          isDragging
            ? "border-indigo-500 bg-indigo-500/10 scale-[1.01]"
            : "border-slate-800 bg-slate-900/50 hover:border-slate-700 hover:bg-slate-900/80"
        } ${isLoading ? "pointer-events-none opacity-80" : ""}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileInputChange}
          className="hidden"
          id="csv-file-input"
        />

        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-tr from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 text-indigo-400 mb-5 shadow-inner">
          <UploadCloud className="h-8 w-8" />
        </div>

        <h3 className="text-lg font-semibold text-white mb-1">
          Upload Dataset CSV
        </h3>
        <p className="text-sm text-slate-400 max-w-sm mb-6">
          Tarik dan lepas file CSV Anda di sini, atau klik tombol di bawah untuk memilih file dari komputer.
        </p>

        {file ? (
          <div className="flex flex-col items-center gap-3 w-full max-w-md p-4 rounded-xl bg-slate-800/80 border border-slate-700/80 mb-6">
            <div className="flex items-center gap-3 w-full">
              <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400">
                <FileSpreadsheet className="h-6 w-6" />
              </div>
              <div className="flex-1 text-left truncate">
                <p className="text-sm font-medium text-white truncate">
                  {file.name}
                </p>
                <p className="text-xs text-slate-400">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
              <CheckCircle2 className="h-5 w-5 text-emerald-400 shrink-0" />
            </div>

            <button
              onClick={handleUpload}
              disabled={isLoading}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition-all hover:from-indigo-600 hover:to-purple-700 hover:shadow-indigo-500/40 active:scale-[0.99] disabled:opacity-50 cursor-pointer mt-1"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Sedang Menganalisis & Profiling Dataset...</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  <span>Mulai Analisis Otomatis</span>
                </>
              )}
            </button>
          </div>
        ) : (
          <div className="flex flex-col sm:flex-row items-center gap-3">
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-2.5 text-sm font-semibold text-white shadow-md shadow-indigo-600/20 transition-all hover:bg-indigo-500 active:scale-95 cursor-pointer"
            >
              <FileText className="h-4 w-4" />
              <span>Pilih File CSV</span>
            </button>

            <button
              type="button"
              onClick={handleLoadSample}
              className="flex items-center justify-center gap-2 rounded-xl bg-slate-800 px-4 py-2.5 text-sm font-medium text-slate-300 border border-slate-700 hover:bg-slate-700 hover:text-white transition-all cursor-pointer"
            >
              <span>Gunakan Sample Data</span>
            </button>
          </div>
        )}

        <div className="mt-6 flex items-center gap-4 text-xs text-slate-500">
          <span>Format didukung: <strong>.CSV</strong></span>
          <span>•</span>
          <span>Batas Maks: <strong>50 MB</strong></span>
          <span>•</span>
          <span>Zero Hallucination</span>
        </div>
      </div>

      {error && (
        <div className="mt-4 flex items-start gap-3 rounded-xl bg-rose-500/10 border border-rose-500/20 p-4 text-rose-400 text-sm animate-in fade-in slide-in-from-top-2 duration-200">
          <AlertCircle className="h-5 w-5 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold text-rose-300">Gagal Memproses Dataset</p>
            <p className="mt-0.5 text-rose-400/90">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
};
