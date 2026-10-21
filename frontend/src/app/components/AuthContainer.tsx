import React from "react";
import { COLORS } from "../constants/colors";

interface AuthContainerProps {
  title: string;
  subtitle: string;
  onBack: () => void;
  children: React.ReactNode;
}

export default function AuthContainer({
  title,
  subtitle,
  onBack,
  children,
}: AuthContainerProps) {
  return (
    <div
      className={`min-h-screen w-full flex flex-col items-center justify-between p-6 ${COLORS.light_mode.bg}`}
    >
      <div className="w-full max-w-sm flex flex-col items-center justify-center  gap-6">
        <div className="text-center w-full">
          <h1 className="text-xl font-boldtracking-tight">{title}</h1>
          <p className="text-xs py-1 ">{subtitle}</p>
        </div>

        <div className="w-full flex flex-col gap-4">{children}</div>

        <button
          type="button"
          onClick={onBack}
          className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
        >
          ← Back to welcome
        </button>
      </div>
    </div>
  );
}
