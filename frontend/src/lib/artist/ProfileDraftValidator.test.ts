import { describe, expect, it } from "vitest";

import { ProfileDraftMapper } from "./ProfileDraftMapper";
import { ProfileDraftValidator } from "./ProfileDraftValidator";

const validDraft = {
  ...ProfileDraftMapper.empty(),
  professional_name: "Ana Ink",
  minimum_tattoo_value: "500",
  expected_ticket: "900",
};

describe("ProfileDraftValidator", () => {
  it("accepts a complete draft", () => {
    expect(ProfileDraftValidator.validate(validDraft)).toEqual([]);
  });

  it("requires the professional name", () => {
    expect(ProfileDraftValidator.validate({ ...validDraft, professional_name: "  " })).toContain(
      "Professional name is required.",
    );
  });

  it("refuses commercial values that are not numbers", () => {
    expect(ProfileDraftValidator.validate({ ...validDraft, expected_ticket: "abc" })).toContain(
      "Expected ticket must be a number equal to or greater than zero.",
    );
  });

  it("refuses negative commercial values", () => {
    expect(
      ProfileDraftValidator.validate({ ...validDraft, minimum_tattoo_value: "-1" }),
    ).toContain("Minimum tattoo value must be a number equal to or greater than zero.");
  });

  it("accepts an absent optional daily session value", () => {
    expect(ProfileDraftValidator.validate({ ...validDraft, daily_session_value: null })).toEqual([]);
  });

  it("requires a three-letter currency", () => {
    expect(ProfileDraftValidator.validate({ ...validDraft, currency: "REAL" })).toContain(
      "Currency must use a three-letter code.",
    );
  });
});
