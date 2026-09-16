import React from "react";
import { Calculator, BarChart3, TrendingUp } from "lucide-react";
import { NumericMetrics } from "../types/dataset";

interface NumericSummaryProps {
  summary: Record<string, NumericMetrics>;
}

export const NumericSummary: React.FC<NumericSummaryProps> = ({ summary }) => {
  const columns = Object.keys(summary);

  if (columns.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-center text-slate-400">
        <Calculator className="h-8 w-8 text-slate-600 mx-auto mb-2" />
        <p className="text-sm">Tidak ada kolom numerik pada dataset ini.</p>
      </div>
    );
  }

  const formatNumber = (val: number | null | undefined) => {
    if (val === null || val === undefined) return "-";
    if (Number.isInteger(val)) return val.toLocaleString();
    return Number(val.toFixed(2)).toLocaleString();
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 backdrop-blur-sm">
      <div className="flex items-center gap-2.5 mb-4">
        <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
          <TrendingUp className="h-4 w-4" />
        </div>
        <div>
          <h4 className="text-base font-semibold text-white">
            Analisis Statistik Numerik
          </h4>
          <p className="text-xs text-slate-400">
            Metrik statistik deskriptif lengkap (Mean, Median, Standar Deviasi, Kuartil, Min/Max).
          </p>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-800">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-800/80 uppercase tracking-wider text-slate-400 text-[11px] font-semibold border-b border-slate-700/80">
            <tr>
              <th className="px-4 py-3">Kolom</th>
              <th className="px-3 py-3 text-right">Count</th>
              <th className="px-3 py-3 text-right font-bold text-indigo-300">Mean</th>
              <th className="px-3 py-3 text-right">Std Dev</th>
              <th className="px-3 py-3 text-right">Min</th>
              <th className="px-3 py-3 text-right">25% (Q1)</th>
              <th className="px-3 py-3 text-right font-bold text-purple-300">50% (Median)</th>
              <th className="px-3 py-3 text-right">75% (Q3)</th>
              <th className="px-3 py-3 text-right">Max</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-900/40 font-mono">
            {columns.map((colName, idx) => {
              const stats = summary[colName];
              return (
                <tr
                  key={idx}
                  className="hover:bg-slate-800/40 transition-colors"
                >
                  <td className="px-4 py-3 font-semibold text-white font-sans">
                    {colName}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-400">
                    {formatNumber(stats.count)}
                  </td>
                  <td className="px-3 py-3 text-right font-bold text-indigo-400">
                    {formatNumber(stats.mean)}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-400">
                    {formatNumber(stats.std)}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-300">
                    {formatNumber(stats.min)}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-400">
                    {formatNumber(stats["25%"])}
                  </td>
                  <td className="px-3 py-3 text-right font-bold text-purple-400">
                    {formatNumber(stats["50%"])}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-400">
                    {formatNumber(stats["75%"])}
                  </td>
                  <td className="px-3 py-3 text-right text-slate-300">
                    {formatNumber(stats.max)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
