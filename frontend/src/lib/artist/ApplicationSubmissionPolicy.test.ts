import { describe, expect, it } from "vitest";

import { ApplicationSubmissionPolicy } from "./ApplicationSubmissionPolicy";

describe("ApplicationSubmissionPolicy", () => {
  it("allows a draft that declares at least one style", () => {
    expect(ApplicationSubmissionPolicy.allows("DRAFT", ["blackwork"])).toBe(true);
    expect(ApplicationSubmissionPolicy.blocker("DRAFT", ["blackwork"])).toBe("");
  });

  it("blocks a draft without styles, matching the backend rule", () => {
    expect(ApplicationSubmissionPolicy.allows("DRAFT", [])).toBe(false);
    expect(ApplicationSubmissionPolicy.blocker("DRAFT", [])).toBe(
      "Add at least one tattoo style before submitting.",
    );
  });

  it("blocks an application that is no longer a draft", () => {
    expect(ApplicationSubmissionPolicy.allows("UNDER_REVIEW", ["blackwork"])).toBe(false);
    expect(ApplicationSubmissionPolicy.blocker("APPROVED", ["blackwork"])).toBe(
      "Only a draft application can be submitted.",
    );
  });
});
