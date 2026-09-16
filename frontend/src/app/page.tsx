"use client";

import React, { useState } from "react";
import {
  BrainCircuit,
  Sparkles,
  BarChart2,
  ShieldCheck,
  Zap,
  TrendingUp,
  Table,
  Layers,
  Network,
  MessageSquareText,
  FileSpreadsheet,
} from "lucide-react";
import { Navbar } from "../components/Navbar";
import { DatasetUploader } from "../components/DatasetUploader";
import { DatasetOverview } from "../components/DatasetOverview";
import { ColumnTable } from "../components/ColumnTable";
import { NumericSummary } from "../components/NumericSummary";
import { CategoricalSummary } from "../components/CategoricalSummary";
import { CorrelationMatrix } from "../components/CorrelationMatrix";
import { DataPreview } from "../components/DataPreview";
import { AIChat } from "../components/AIChat";
import { DatasetProfileResponse } from "../types/dataset";

export default function Home() {
  const [profile, setProfile] = useState<DatasetProfileResponse | null>(null);
  const [activeTab, setActiveTab] = useState<
    "dashboard" | "columns" | "numeric" | "categorical" | "correlation" | "preview" | "chat"
  >("dashboard");

  const handleUploadSuccess = (newProfile: DatasetProfileResponse) => {
    setProfile(newProfile);
    setActiveTab("dashboard");
  };

  const handleReset = () => {
    setProfile(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar
        onNewUpload={profile ? handleReset : undefined}
        datasetName={profile?.filename}
      />

      <main className="flex-1">
        {!profile ? (
          /* ================= LANDING / UPLOAD PAGE ================= */
          <div className="relative overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-indigo-600/20 via-purple-600/20 to-pink-600/10 blur-[130px] -z-10 pointer-events-none rounded-full" />
            <div className="absolute top-1/2 right-10 w-[300px] h-[300px] bg-blue-600/10 blur-[100px] -z-10 pointer-events-none rounded-full" />

            <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-12 sm:py-20">
              {/* Hero Header */}
              <div className="text-center space-y-4 max-w-3xl mx-auto mb-12">
                <div className="inline-flex items-center gap-2 rounded-full bg-indigo-500/10 border border-indigo-500/20 px-3.5 py-1 text-xs font-semibold text-indigo-400">
                  <Sparkles className="h-3.5 w-3.5" />
                  <span>DataMind 1.0 • Next-Gen AI Data Analytics</span>
                </div>

                <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
                  Eksplorasi & Analisis Dataset dengan{" "}
                  <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                    Kekuatan AI & Deterministic EDA
                  </span>
                </h1>

                <p className="text-sm sm:text-base text-slate-400 leading-relaxed max-w-2xl mx-auto">
                  Cukup upload file dataset CSV Anda. Dapatkan profiling otomatis, statistik deskriptif, matriks korelasi, dan tanyakan wawasan apa pun kepada AI Agent yang bebas dari halusinasi data numerik.
                </p>
              </div>

              {/* Upload Zone */}
              <DatasetUploader onUploadSuccess={handleUploadSuccess} />

              {/* Value Props / Features */}
              <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-6 backdrop-blur-sm">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-4">
                    <BarChart2 className="h-5 w-5" />
                  </div>
                  <h4 className="text-base font-semibold text-white mb-1.5">
                    Automated EDA Engine
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                    Menghitung statistik deskriptif numerik, deteksi tipe kolom, missing values, dan ringkasan distribusi secara otomatis menggunakan Pandas.
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-6 backdrop-blur-sm">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20 mb-4">
                    <ShieldCheck className="h-5 w-5" />
                  </div>
                  <h4 className="text-base font-semibold text-white mb-1.5">
                    Zero Numeric Hallucination
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                    AI menjawab berdasarkan komputasi data asli dari tools deterministik, bukan mereka-reka angka statistik sendiri.
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800/80 bg-slate-900/40 p-6 backdrop-blur-sm">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-pink-500/10 text-pink-400 border border-pink-500/20 mb-4">
                    <Zap className="h-5 w-5" />
                  </div>
                  <h4 className="text-base font-semibold text-white mb-1.5">
                    LangChain Agent Tool Calling
                  </h4>
                  <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
                    Agent cerdas memanggil specialized tools sesuai kebutuhan pertanyaan pengguna dan merangkum wawasan secara terstruktur.
                  </p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* ================= DATASET DASHBOARD ================= */
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8 space-y-6">
            {/* Top Navigation Tabs */}
            <div className="flex flex-wrap items-center gap-2 border-b border-slate-800 pb-4">
              <button
                onClick={() => setActiveTab("dashboard")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "dashboard"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <Layers className="h-4 w-4" />
                <span>Dashboard Lengkap</span>
              </button>

              <button
                onClick={() => setActiveTab("numeric")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "numeric"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <TrendingUp className="h-4 w-4" />
                <span>Statistik Numerik</span>
              </button>

              <button
                onClick={() => setActiveTab("columns")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "columns"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <Table className="h-4 w-4" />
                <span>Struktur Kolom</span>
              </button>

              <button
                onClick={() => setActiveTab("correlation")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "correlation"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <Network className="h-4 w-4" />
                <span>Korelasi</span>
              </button>

              <button
                onClick={() => setActiveTab("preview")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "preview"
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-white"
                }`}
              >
                <FileSpreadsheet className="h-4 w-4" />
                <span>Data Preview</span>
              </button>

              <button
                onClick={() => setActiveTab("chat")}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer ${
                  activeTab === "chat"
                    ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md shadow-purple-600/20"
                    : "bg-slate-900 text-purple-400 hover:bg-slate-800 hover:text-purple-300"
                }`}
              >
                <MessageSquareText className="h-4 w-4" />
                <span>AI Assistant Chat</span>
              </button>
            </div>

            {/* Content Layout */}
            {activeTab === "dashboard" && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                {/* Left side: EDA and Visuals (7 cols) */}
                <div className="lg:col-span-7 space-y-6">
                  <DatasetOverview profile={profile} />
                  <NumericSummary summary={profile.numeric_summary} />
                  <ColumnTable columns={profile.columns_info} />
                  <CategoricalSummary
                    summary={profile.categorical_summary}
                    totalRows={profile.rows}
                  />
                  <CorrelationMatrix correlation={profile.correlation} />
                  <DataPreview preview={profile.sample_preview} />
                </div>

                {/* Right side: Persistent AI Chat Assistant (5 cols) */}
                <div className="lg:col-span-5 lg:sticky lg:top-24">
                  <AIChat
                    datasetId={profile.dataset_id}
                    datasetName={profile.filename}
                  />
                </div>
              </div>
            )}

            {activeTab === "numeric" && (
              <div className="space-y-6">
                <DatasetOverview profile={profile} />
                <NumericSummary summary={profile.numeric_summary} />
              </div>
            )}

            {activeTab === "columns" && (
              <div className="space-y-6">
                <DatasetOverview profile={profile} />
                <ColumnTable columns={profile.columns_info} />
              </div>
            )}

            {activeTab === "categorical" && (
              <div className="space-y-6">
                <DatasetOverview profile={profile} />
                <CategoricalSummary
                  summary={profile.categorical_summary}
                  totalRows={profile.rows}
                />
              </div>
            )}

            {activeTab === "correlation" && (
              <div className="space-y-6">
                <DatasetOverview profile={profile} />
                <CorrelationMatrix correlation={profile.correlation} />
              </div>
            )}

            {activeTab === "preview" && (
              <div className="space-y-6">
                <DatasetOverview profile={profile} />
                <DataPreview preview={profile.sample_preview} />
              </div>
            )}

            {activeTab === "chat" && (
              <div className="max-w-4xl mx-auto">
                <AIChat
                  datasetId={profile.dataset_id}
                  datasetName={profile.filename}
                />
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>© 2026 DataMind AI. AI-Powered Data Analytics Platform.</p>
      </footer>
    </div>
  );
}
