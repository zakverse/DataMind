import React from "react";
import { PieChart, Tags } from "lucide-react";
import { CategoricalMetrics } from "../types/dataset";

interface CategoricalSummaryProps {
  summary: Record<string, CategoricalMetrics>;
  totalRows: number;
}

export const CategoricalSummary: React.FC<CategoricalSummaryProps> = ({
  summary,
  totalRows,
}) => {
  const columns = Object.keys(summary);

  if (columns.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-center text-slate-400">
        <Tags className="h-8 w-8 text-slate-600 mx-auto mb-2" />
        <p className="text-sm">Tidak ada kolom kategorikal pada dataset ini.</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center gap-2.5 mb-4">
        <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
          <PieChart className="h-4 w-4" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-white">
            Distribusi Kolom Kategorikal
          </h4>
          <p className="text-xs text-slate-400">
            Nilai unik dan frekuensi kategori teratas untuk setiap kolom teks.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {columns.map((colName, idx) => {
          const cat = summary[colName];
          const topValues = Object.entries(cat.top_values || {});

          return (
            <div
              key={idx}
              className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 hover:border-slate-700 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between pb-2 border-b border-slate-800/80 mb-3">
                  <span className="font-semibold text-white text-sm truncate" title={colName}>
                    {colName}
                  </span>
                  <span className="rounded-md bg-purple-500/10 px-2 py-0.5 text-[11px] font-medium text-purple-300 border border-purple-500/20">
                    {cat.unique_count} Unique
                  </span>
                </div>

                <div className="space-y-2.5">
                  {topValues.length > 0 ? (
                    topValues.map(([valName, count], vIdx) => {
                      const pct = totalRows > 0 ? (count / totalRows) * 100 : 0;
                      return (
                        <div key={vIdx} className="space-y-1">
                          <div className="flex justify-between text-xs">
                            <span className="text-slate-300 font-medium truncate max-w-[140px]" title={valName}>
                              {valName || "(empty/null)"}
                            </span>
                            <span className="text-slate-400 font-mono text-[11px]">
                              {count.toLocaleString()} ({pct.toFixed(1)}%)
                            </span>
                          </div>
                          <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full"
                              style={{ width: `${Math.min(pct, 100)}%` }}
                            />
                          </div>
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-xs text-slate-500 italic">
                      Tidak ada data nilai kategori.
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
