import type { ApplicationStatus } from "../types/artist";

export type StatusTone = "neutral" | "pending" | "positive" | "negative";

export class ApplicationStatusPresenter {
  private static readonly labels: Record<ApplicationStatus, string> = {
    DRAFT: "Draft",
    UNDER_REVIEW: "Under review",
    APPROVED: "Approved",
    REJECTED: "Rejected",
  };

  private static readonly tones: Record<ApplicationStatus, StatusTone> = {
    DRAFT: "neutral",
    UNDER_REVIEW: "pending",
    APPROVED: "positive",
    REJECTED: "negative",
  };

  private static readonly guidance: Record<ApplicationStatus, string> = {
    DRAFT:
      "Complete your profile and submit it. The Advisory team reviews every application before approval.",
    UNDER_REVIEW:
      "Your application is with the Advisory team. Profile changes made now are visible to the reviewer.",
    APPROVED: "Your application was approved. You can be planned into Guest operations.",
    REJECTED: "Your application was rejected. The Advisory team recorded the reason below.",
  };

  static label(status: ApplicationStatus): string {
    return ApplicationStatusPresenter.labels[status];
  }

  static tone(status: ApplicationStatus): StatusTone {
    return ApplicationStatusPresenter.tones[status];
  }

  static guidanceText(status: ApplicationStatus): string {
    return ApplicationStatusPresenter.guidance[status];
  }
}
