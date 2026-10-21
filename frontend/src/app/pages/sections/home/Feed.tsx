import type { FeedItem } from "../../../components/FeedItem";

interface FeedProps {
  items: FeedItem[];
  onSelectItem: (item: FeedItem) => void;
}

export default function Feed({ items, onSelectItem }: FeedProps) {
  return (
    <div className="w-full flex flex-col-reverse gap-3">
      {items.map((item) => {
        if (item.kind === "session") {
          return (
            <button
              key={item.id}
              onClick={() => onSelectItem(item)}
              className="w-full text-left p-4 bg-white rounded-2xl border border-slate-100 shadow-sm active:scale-[0.99] transition-transform"
            >
              <span className="text-xs font-semibold text-slate-400">
                {item.date} • {item.subject}
              </span>
              <h3 className="text-sm font-bold text-slate-800 mt-1">
                {item.title}
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Duración: {item.durationMinutes} min
              </p>
            </button>
          );
        }

        if (item.kind === "chart") {
          return (
            <button
              key={item.id}
              onClick={() => onSelectItem(item)}
              className="w-full text-left p-4 bg-indigo-50/70 rounded-2xl border border-indigo-100 shadow-sm active:scale-[0.99] transition-transform"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-indigo-600">
                  Resumen Mensual
                </span>
                <span className="text-xs text-indigo-400">{item.period}</span>
              </div>
              <h3 className="text-sm font-bold text-slate-800 mt-2">
                {item.totalHours} hrs estudiadas ({item.completedSessions}{" "}
                sesiones)
              </h3>
              <div className="w-full h-12 mt-2 bg-indigo-100 rounded-lg flex items-center justify-center text-xs text-indigo-500">
                [Vista previa de la gráfica]
              </div>
            </button>
          );
        }

        return null;
      })}
    </div>
  );
}
