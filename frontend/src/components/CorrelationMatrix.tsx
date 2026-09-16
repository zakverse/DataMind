import React from "react";
import { Network, Info } from "lucide-react";

interface CorrelationMatrixProps {
  correlation: Record<string, Record<string, number | null>>;
}

export const CorrelationMatrix: React.FC<CorrelationMatrixProps> = ({
  correlation,
}) => {
  const columns = Object.keys(correlation);

  if (columns.length < 2) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-center text-slate-400">
        <Network className="h-8 w-8 text-slate-600 mx-auto mb-2" />
        <p className="text-sm">
          Memerlukan minimal 2 kolom numerik untuk menghitung matriks korelasi Pearson.
        </p>
      </div>
    );
  }

  const getCellColor = (val: number | null) => {
    if (val === null || val === undefined) return "bg-slate-800/40 text-slate-500";
    if (val === 1.0) return "bg-indigo-600/60 text-white font-bold";
    if (val > 0.6) return "bg-indigo-500/40 text-indigo-200 font-semibold";
    if (val > 0.2) return "bg-indigo-500/20 text-indigo-300";
    if (val > -0.2) return "bg-slate-800/60 text-slate-400";
    if (val > -0.6) return "bg-rose-500/20 text-rose-300";
    return "bg-rose-500/40 text-rose-200 font-semibold";
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Network className="h-4 w-4" />
          </div>
          <div>
            <h4 className="text-base font-semibold text-white">
              Matriks Korelasi Pearson
            </h4>
            <p className="text-xs text-slate-400">
              Analisis hubungan linear antar variabel numerik (-1.0 s.d. +1.0).
            </p>
          </div>
        </div>

        {/* Mini Legend */}
        <div className="flex items-center gap-2 text-[11px] text-slate-400">
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-rose-500/40 border border-rose-500/60 inline-block" />
            Negatif
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-slate-700 inline-block" />
            Netral
          </span>
          <span className="flex items-center gap-1">
            <span className="h-2.5 w-2.5 rounded bg-indigo-500/50 border border-indigo-500/60 inline-block" />
            Positif
          </span>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-800 p-2 bg-slate-950/40">
        <table className="w-full text-center text-xs">
          <thead>
            <tr>
              <th className="p-2.5 text-left text-slate-400 font-medium"></th>
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  className="p-2.5 font-semibold text-white truncate max-w-[100px]"
                  title={col}
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {columns.map((rowCol, rIdx) => (
              <tr key={rIdx}>
                <td
                  className="p-2.5 text-left font-semibold text-white truncate max-w-[120px]"
                  title={rowCol}
                >
                  {rowCol}
                </td>
                {columns.map((colCol, cIdx) => {
                  const val = correlation[rowCol]?.[colCol];
                  return (
                    <td key={cIdx} className="p-1">
                      <div
                        className={`rounded-lg p-2 font-mono transition-all hover:scale-105 border border-slate-800/40 ${getCellColor(
                          val
                        )}`}
                        title={`Korelasi (${rowCol}, ${colCol}): ${
                          val !== null && val !== undefined ? val.toFixed(4) : "N/A"
                        }`}
                      >
                        {val !== null && val !== undefined ? val.toFixed(2) : "-"}
                      </div>
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
