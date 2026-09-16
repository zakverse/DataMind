import React from "react";
import { BrainCircuit, Database, Sparkles, RefreshCw } from "lucide-react";

interface NavbarProps {
  onNewUpload?: () => void;
  datasetName?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ onNewUpload, datasetName }) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 shadow-lg shadow-indigo-500/20">
            <BrainCircuit className="h-6 w-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-white">
                Data<span className="text-indigo-400">Mind</span>
              </span>
              <span className="rounded-full bg-indigo-500/10 px-2 py-0.5 text-xs font-semibold text-indigo-400 border border-indigo-500/20">
                AI Data Analyst
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              AI-Powered Exploratory Data Analytics Platform
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          {datasetName && (
            <div className="hidden md:flex items-center gap-2 rounded-lg bg-slate-900 px-3 py-1.5 border border-slate-800 text-xs text-slate-300">
              <Database className="h-3.5 w-3.5 text-indigo-400" />
              <span className="font-medium text-white">{datasetName}</span>
            </div>
          )}

          {onNewUpload && (
            <button
              onClick={onNewUpload}
              className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 px-3.5 py-1.5 text-xs font-medium text-white shadow-md shadow-indigo-600/20 transition-all hover:from-indigo-500 hover:to-purple-500 hover:shadow-indigo-500/30 active:scale-95 cursor-pointer"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Ganti Dataset</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
