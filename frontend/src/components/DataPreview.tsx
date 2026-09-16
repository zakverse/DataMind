import React from "react";
import { Table, Eye } from "lucide-react";

interface DataPreviewProps {
  preview: Record<string, string | number | boolean | null>[];
}

export const DataPreview: React.FC<DataPreviewProps> = ({ preview }) => {
  if (!preview || preview.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-center text-slate-400">
        <Table className="h-8 w-8 text-slate-600 mx-auto mb-2" />
        <p className="text-sm">Tidak ada sampel data untuk ditampilkan.</p>
      </div>
    );
  }

  const columns = Object.keys(preview[0] || {});

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center gap-2.5 mb-4">
        <div className="p-2 rounded-xl bg-teal-500/10 text-teal-400 border border-teal-500/20">
          <Eye className="h-4 w-4" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-white">
            Data Preview (Sampel Baris Teratas)
          </h4>
          <p className="text-xs text-slate-400">
            Tampilan cuplikan {preview.length} baris pertama dataset asli.
          </p>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-800">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-800/80 uppercase tracking-wider text-slate-400 text-[11px] font-semibold border-b border-slate-700/80">
            <tr>
              <th className="px-3 py-2.5 w-12 text-center text-slate-500">#</th>
              {columns.map((col, idx) => (
                <th key={idx} className="px-4 py-2.5 font-mono text-white">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/40 font-mono">
            {preview.map((row, rIdx) => (
              <tr
                key={rIdx}
                className="hover:bg-slate-800/40 transition-colors"
              >
                <td className="px-3 py-2.5 text-center text-slate-500 text-[11px]">
                  {rIdx + 1}
                </td>
                {columns.map((col, cIdx) => {
                  const val = row[col];
                  return (
                    <td
                      key={cIdx}
                      className={`px-4 py-2.5 truncate max-w-[200px] ${
                        val === null || val === undefined
                          ? "text-amber-500/60 italic"
                          : "text-slate-300"
                      }`}
                      title={String(val)}
                    >
                      {val === null || val === undefined ? "null" : String(val)}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
