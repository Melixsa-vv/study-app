export interface SessionItem {
  id: string;
  kind: "session";
  title: string;
  subject: string;
  durationMinutes: number;
  date: string;
  summary?: string;
}

export interface MonthlyChartItem {
  id: string;
  kind: "chart";
  period: string;
  totalHours: number;
  completedSessions: number;
  date: string;
}

export type FeedItem = SessionItem | MonthlyChartItem;
