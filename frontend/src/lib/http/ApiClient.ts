import { ApiError } from "./ApiError";

export class ApiClient {
  private static readonly baseUrl =
    process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

  static get<TResult>(path: string): Promise<TResult> {
    return ApiClient.send<TResult>(path);
  }

  static async mutate<TResult>(
    path: string,
    method: "POST" | "PUT" | "PATCH" | "DELETE",
    body?: unknown,
  ): Promise<TResult> {
    const token = await ApiClient.csrfToken();
    return ApiClient.send<TResult>(path, {
      method,
      headers: { "X-CSRFToken": token },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
  }

  private static async csrfToken(): Promise<string> {
    const result = await ApiClient.send<{ csrf_token: string }>("/auth/csrf/");
    return result.csrf_token;
  }

  private static async send<TResult>(path: string, init?: RequestInit): Promise<TResult> {
    const response = await fetch(`${ApiClient.baseUrl}${path}`, {
      credentials: "include",
      ...init,
      headers: { "Content-Type": "application/json", ...init?.headers },
    });
    if (!response.ok) {
      throw ApiError.fromPayload(response.status, await response.json().catch(() => ({})));
    }
    if (response.status === 204) return undefined as TResult;
    return response.json() as Promise<TResult>;
  }
}
