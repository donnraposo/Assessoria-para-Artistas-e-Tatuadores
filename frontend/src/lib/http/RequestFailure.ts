import { ApiError } from "./ApiError";

export class RequestFailure {
  static message(error: unknown): string {
    return error instanceof Error ? error.message : "Request failed.";
  }

  static isUnauthenticated(error: unknown): boolean {
    return error instanceof ApiError && (error.status === 401 || error.status === 403);
  }

  static isNotFound(error: unknown): boolean {
    return error instanceof ApiError && error.status === 404;
  }
}
