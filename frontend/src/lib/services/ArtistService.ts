import { ApiClient } from "../http/ApiClient";
import { RequestFailure } from "../http/RequestFailure";
import type {
  ArtistApplication,
  ArtistApplicationDetail,
  ArtistProfile,
  ArtistProfileDraft,
  PortfolioItem,
} from "../types/artist";

export class ArtistService {
  static async findProfile(): Promise<ArtistProfile | null> {
    return ArtistService.optional(ApiClient.get<ArtistProfile>("/artists/me/"));
  }

  static saveProfile(draft: ArtistProfileDraft): Promise<ArtistProfile> {
    return ApiClient.mutate<ArtistProfile>("/artists/me/", "PUT", draft);
  }

  static async findApplication(): Promise<ArtistApplication | null> {
    return ArtistService.optional(ApiClient.get<ArtistApplication>("/artists/me/application/"));
  }

  static submitApplication(): Promise<ArtistApplication> {
    return ApiClient.mutate<ArtistApplication>("/artists/me/application/", "POST");
  }

  static portfolio(): Promise<PortfolioItem[]> {
    return ApiClient.get<PortfolioItem[]>("/artists/me/portfolio/");
  }

  static applicationDetail(applicationId: string): Promise<ArtistApplicationDetail> {
    return ApiClient.get<ArtistApplicationDetail>(`/artists/applications/${applicationId}/`);
  }

  static reviewApplication(
    applicationId: string,
    approved: boolean,
    reason: string,
  ): Promise<ArtistApplicationDetail> {
    return ApiClient.mutate<ArtistApplicationDetail>(
      `/artists/applications/${applicationId}/review/`,
      "POST",
      { approved, reason },
    );
  }

  private static async optional<TResult>(request: Promise<TResult>): Promise<TResult | null> {
    try {
      return await request;
    } catch (error) {
      if (RequestFailure.isNotFound(error)) return null;
      throw error;
    }
  }
}
