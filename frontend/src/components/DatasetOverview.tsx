import React from "react";
import {
  Rows3,
  Columns3,
  HardDrive,
  AlertTriangle,
  Copy,
  Hash,
  Type,
  Calendar,
} from "lucide-react";
import { DatasetProfileResponse } from "../types/dataset";

interface DatasetOverviewProps {
  profile: DatasetProfileResponse;
}

export const DatasetOverview: React.FC<DatasetOverviewProps> = ({ profile }) => {
  const formatBytes = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const statCards = [
    {
      title: "Total Baris",
      value: profile.rows.toLocaleString(),
      subtitle: `${profile.columns} Kolom`,
      icon: Rows3,
      color: "from-blue-500/20 to-cyan-500/20 text-cyan-400 border-cyan-500/30",
    },
    {
      title: "Total Kolom",
      value: profile.columns,
      subtitle: `${profile.column_types.numeric.length} Num, ${profile.column_types.categorical.length} Cat`,
      icon: Columns3,
      color: "from-indigo-500/20 to-purple-500/20 text-indigo-400 border-indigo-500/30",
    },
    {
      title: "Ukuran File",
      value: formatBytes(profile.file_size_bytes),
      subtitle: profile.filename,
      icon: HardDrive,
      color: "from-emerald-500/20 to-teal-500/20 text-emerald-400 border-emerald-500/30",
    },
    {
      title: "Missing Cells",
      value: `${profile.missing_summary.total_missing_cells.toLocaleString()}`,
      subtitle: `${profile.missing_summary.overall_missing_percentage}% dari total sel`,
      icon: AlertTriangle,
      color:
        profile.missing_summary.total_missing_cells > 0
          ? "from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30"
          : "from-slate-800 to-slate-800 text-slate-400 border-slate-700",
    },
    {
      title: "Baris Duplikat",
      value: `${profile.duplicate_summary.duplicate_rows.toLocaleString()}`,
      subtitle: `${profile.duplicate_summary.duplicate_percentage}% duplikasi`,
      icon: Copy,
      color:
        profile.duplicate_summary.duplicate_rows > 0
          ? "from-rose-500/20 to-pink-500/20 text-rose-400 border-rose-500/30"
          : "from-slate-800 to-slate-800 text-slate-400 border-slate-700",
    },
  ];

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        {statCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              className="group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 p-4 transition-all hover:border-slate-700 hover:bg-slate-900"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">
                  {card.title}
                </span>
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-br border ${card.color}`}
                >
                  <Icon className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-2">
                <p className="text-xl font-bold tracking-tight text-white">
                  {card.value}
                </p>
                <p className="text-xs text-slate-500 truncate mt-0.5" title={card.subtitle}>
                  {card.subtitle}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Column Type Badges */}
      <div className="flex flex-wrap items-center gap-2 rounded-xl bg-slate-900/40 border border-slate-800/80 p-3 text-xs">
        <span className="text-slate-400 font-medium mr-1">Tipe Kolom:</span>
        <span className="flex items-center gap-1.5 rounded-lg bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-1 text-indigo-300 font-medium">
          <Hash className="h-3 w-3" />
          Numerik: {profile.column_types.numeric.length}
        </span>
        <span className="flex items-center gap-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 px-2.5 py-1 text-purple-300 font-medium">
          <Type className="h-3 w-3" />
          Kategorikal: {profile.column_types.categorical.length}
        </span>
        {profile.column_types.datetime.length > 0 && (
          <span className="flex items-center gap-1.5 rounded-lg bg-teal-500/10 border border-teal-500/20 px-2.5 py-1 text-teal-300 font-medium">
            <Calendar className="h-3 w-3" />
            Datetime: {profile.column_types.datetime.length}
          </span>
        )}
      </div>
    </div>
  );
};
