const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export type CurrentUser = {
  id: string;
  email: string;
  full_name: string;
  roles: string[];
};

export type Activity = {
  id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  created_at: string;
};

export type OperationsDashboard = {
  queues: Record<string, number>;
  agency_revenue_by_currency: Array<{ currency: string; total: string }>;
  unread_notifications: number;
  recent_activity: Activity[];
};

export type RoleWorkspace = {
  role: "ARTIST" | "STUDIO";
  cards: Array<{ key: string; label: string; value: number; detail: string }>;
  balances: Array<{ currency: string; total: string }>;
};

function errorMessageFrom(body: unknown): string {
  if (body && typeof body === "object") {
    const record = body as Record<string, unknown>;
    if (typeof record.detail === "string") return record.detail;
    const fieldMessage = Object.values(record)
      .flat()
      .find((entry): entry is string => typeof entry === "string");
    if (fieldMessage) return fieldMessage;
  }
  return "Request failed.";
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    credentials: "include",
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(errorMessageFrom(body));
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

async function csrfToken(): Promise<string> {
  const result = await requestJson<{ csrf_token: string }>("/auth/csrf/");
  return result.csrf_token;
}

export async function login(email: string, password: string): Promise<CurrentUser> {
  const token = await csrfToken();
  return requestJson<CurrentUser>("/auth/login/", {
    method: "POST",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify({ email, password }),
  });
}

export type SelfServiceRole = "ARTIST" | "STUDIO";

export async function register(
  fullName: string,
  email: string,
  password: string,
  role: SelfServiceRole,
): Promise<CurrentUser> {
  const token = await csrfToken();
  return requestJson<CurrentUser>("/auth/register/", {
    method: "POST",
    headers: { "X-CSRFToken": token },
    body: JSON.stringify({ full_name: fullName, email, password, role }),
  });
}

export async function logout(): Promise<void> {
  const token = await csrfToken();
  await requestJson<void>("/auth/logout/", {
    method: "POST",
    headers: { "X-CSRFToken": token },
  });
}

export function getCurrentUser(): Promise<CurrentUser> {
  return requestJson<CurrentUser>("/auth/me/");
}

export function getOperationsDashboard(): Promise<OperationsDashboard> {
  return requestJson<OperationsDashboard>("/operations/dashboard/");
}

export function getRoleWorkspace(): Promise<RoleWorkspace> {
  return requestJson<RoleWorkspace>("/operations/workspace/");
}
