import { ApiClient } from "../http/ApiClient";
import type { CurrentUser } from "../types/identity";

export class IdentityService {
  static login(email: string, password: string): Promise<CurrentUser> {
    return ApiClient.mutate<CurrentUser>("/auth/login/", "POST", { email, password });
  }

  static async logout(): Promise<void> {
    await ApiClient.mutate<void>("/auth/logout/", "POST");
  }

  static currentUser(): Promise<CurrentUser> {
    return ApiClient.get<CurrentUser>("/auth/me/");
  }
}
