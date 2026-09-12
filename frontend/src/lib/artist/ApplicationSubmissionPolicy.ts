import type { ApplicationStatus } from "../types/artist";

export class ApplicationSubmissionPolicy {
  static allows(status: ApplicationStatus, styles: string[]): boolean {
    return ApplicationSubmissionPolicy.blocker(status, styles).length === 0;
  }

  static blocker(status: ApplicationStatus, styles: string[]): string {
    if (status !== "DRAFT") return "Only a draft application can be submitted.";
    if (styles.length === 0) return "Add at least one tattoo style before submitting.";
    return "";
  }
}
