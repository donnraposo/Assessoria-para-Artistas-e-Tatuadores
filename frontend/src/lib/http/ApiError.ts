export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }

  static fromPayload(status: number, payload: unknown): ApiError {
    return new ApiError(status, ApiError.readDetail(payload));
  }

  private static readDetail(payload: unknown): string {
    if (typeof payload !== "object" || payload === null) return "Request failed.";
    const entries = Object.entries(payload as Record<string, unknown>);
    const detail = entries.find(([key]) => key === "detail")?.[1];
    if (typeof detail === "string") return detail;
    const fieldMessage = entries
      .flatMap(([field, value]) => (Array.isArray(value) ? [`${field}: ${value[0]}`] : []))
      .at(0);
    return fieldMessage ?? "Request failed.";
  }
}
