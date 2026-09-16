"use client";

import React, { useState } from "react";
import { Search, Hash, Type, Calendar, HelpCircle } from "lucide-react";
import { ColumnInfo } from "../types/dataset";

interface ColumnTableProps {
  columns: ColumnInfo[];
}

export const ColumnTable: React.FC<ColumnTableProps> = ({ columns }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredColumns = columns.filter((col) =>
    col.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    col.data_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const renderTypeBadge = (col: ColumnInfo) => {
    if (col.is_numeric) {
      return (
        <span className="inline-flex items-center gap-1 rounded-md bg-indigo-500/10 px-2 py-0.5 text-xs font-medium text-indigo-400 border border-indigo-500/20">
          <Hash className="h-3 w-3" />
          Numeric
        </span>
      );
    }
    if (col.is_datetime) {
      return (
        <span className="inline-flex items-center gap-1 rounded-md bg-teal-500/10 px-2 py-0.5 text-xs font-medium text-teal-400 border border-teal-500/20">
          <Calendar className="h-3 w-3" />
          Datetime
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 rounded-md bg-purple-500/10 px-2 py-0.5 text-xs font-medium text-purple-400 border border-purple-500/20">
        <Type className="h-3 w-3" />
        Categorical
      </span>
    );
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
        <div>
          <h4 className="text-base font-semibold text-white">
            Informasi Struktur Kolom
          </h4>
          <p className="text-xs text-slate-400">
            Detail tipe data, persentase nilai kosong, dan jumlah nilai unik setiap kolom.
          </p>
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Cari kolom..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full rounded-xl bg-slate-800/80 border border-slate-700/80 pl-9 pr-4 py-1.5 text-xs text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-all"
          />
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-800">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-800/80 uppercase tracking-wider text-slate-400 text-[11px] font-semibold border-b border-slate-700/80">
            <tr>
              <th className="px-4 py-3">Nama Kolom</th>
              <th className="px-4 py-3">Tipe Data</th>
              <th className="px-4 py-3">Kategori</th>
              <th className="px-4 py-3">Missing Values</th>
              <th className="px-4 py-3 text-right">Unique Values</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/40">
            {filteredColumns.map((col, idx) => (
              <tr
                key={idx}
                className="hover:bg-slate-800/40 transition-colors group"
              >
                <td className="px-4 py-3 font-semibold text-white font-mono">
                  {col.name}
                </td>
                <td className="px-4 py-3 text-slate-400 font-mono">
                  {col.data_type}
                </td>
                <td className="px-4 py-3">{renderTypeBadge(col)}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span
                      className={`font-medium ${
                        col.missing_count > 0 ? "text-amber-400" : "text-slate-400"
                      }`}
                    >
                      {col.missing_count} ({col.missing_percentage}%)
                    </span>
                    {col.missing_percentage > 0 && (
                      <div className="w-16 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-amber-500 rounded-full"
                          style={{ width: `${Math.min(col.missing_percentage, 100)}%` }}
                        />
                      </div>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3 text-right font-medium text-slate-300">
                  {col.unique_count.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
