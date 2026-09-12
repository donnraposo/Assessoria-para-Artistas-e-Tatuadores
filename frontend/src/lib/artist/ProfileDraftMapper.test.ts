import { describe, expect, it } from "vitest";

import { ProfileDraftMapper } from "./ProfileDraftMapper";

describe("ProfileDraftMapper", () => {
  it("starts an empty draft in the default currency", () => {
    const draft = ProfileDraftMapper.empty();

    expect(draft.currency).toBe("BRL");
    expect(draft.styles).toEqual([]);
    expect(draft.daily_session_value).toBeNull();
  });

  it("keeps only the editable fields of a stored profile", () => {
    const draft = ProfileDraftMapper.fromProfile({
      id: "0b6c0a2e-1d55-4a5f-9f2a-1a2b3c4d5e6f",
      created_at: "2026-09-01T10:00:00Z",
      updated_at: "2026-09-02T10:00:00Z",
      professional_name: "Ana Ink",
      biography: "Fine line.",
      years_experience: 6,
      styles: ["fine line"],
      currency: "BRL",
      minimum_tattoo_value: "500.00",
      expected_ticket: "900.00",
      daily_session_value: null,
    });

    expect(draft).not.toHaveProperty("id");
    expect(draft).not.toHaveProperty("created_at");
    expect(draft.professional_name).toBe("Ana Ink");
  });
});
