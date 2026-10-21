export interface SessionItem {
  id: string;
  kind: "session";
  title: string;
  subject: string;
  durationMinutes: number;
  date: string; // ISO string o formato fecha
  summary?: string;
}

export interface MonthlyChartItem {
  id: string;
  kind: "chart";
  period: string; // Ej: "Octubre 2026"
  totalHours: number;
  completedSessions: number;
  date: string;
}

// Unión de ambos tipos de tarjetas
export type FeedItem = SessionItem | MonthlyChartItem;
