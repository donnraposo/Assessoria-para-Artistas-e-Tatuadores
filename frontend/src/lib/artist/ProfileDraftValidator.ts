import type { ArtistProfileDraft } from "../types/artist";

export class ProfileDraftValidator {
  static validate(draft: ArtistProfileDraft): string[] {
    const messages: string[] = [];
    if (draft.professional_name.trim().length === 0) {
      messages.push("Professional name is required.");
    }
    if (draft.currency.trim().length !== 3) {
      messages.push("Currency must use a three-letter code.");
    }
    if (!ProfileDraftValidator.isNonNegativeAmount(draft.minimum_tattoo_value)) {
      messages.push("Minimum tattoo value must be a number equal to or greater than zero.");
    }
    if (!ProfileDraftValidator.isNonNegativeAmount(draft.expected_ticket)) {
      messages.push("Expected ticket must be a number equal to or greater than zero.");
    }
    if (
      draft.daily_session_value !== null &&
      !ProfileDraftValidator.isNonNegativeAmount(draft.daily_session_value)
    ) {
      messages.push("Daily session value must be a number equal to or greater than zero.");
    }
    if (!Number.isInteger(draft.years_experience) || draft.years_experience < 0) {
      messages.push("Years of experience must be a whole number.");
    }
    return messages;
  }

  private static isNonNegativeAmount(value: string): boolean {
    if (value.trim().length === 0) return false;
    const amount = Number(value);
    return Number.isFinite(amount) && amount >= 0;
  }
}
