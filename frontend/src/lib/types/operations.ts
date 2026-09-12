export type Activity = {
  id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  created_at: string;
};

export type CurrencyTotal = {
  currency: string;
  total: string;
};

export type OperationsDashboard = {
  queues: Record<string, number>;
  agency_revenue_by_currency: CurrencyTotal[];
  unread_notifications: number;
  recent_activity: Activity[];
};

export type RoleWorkspace = {
  role: "ARTIST" | "STUDIO";
  cards: Array<{ key: string; label: string; value: number; detail: string }>;
  balances: CurrencyTotal[];
};

export type QueuePage<TResult> = {
  count: number;
  page: number;
  pages: number;
  results: TResult[];
};
