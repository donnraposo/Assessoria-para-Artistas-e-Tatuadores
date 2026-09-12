import { describe, expect, it } from "vitest";

import { buildAdvisoryForms } from "./operationsForms";

const referenceData = {
  artists: [{ id: "artist-1", professional_name: "Nova Ink", currency: "EUR" }],
  studios: [{ id: "studio-1", name: "Black Room", city: "Lisbon", country_code: "PT" }],
  guests: [{ id: "guest-1", artist_id: "artist-1", city: "Lisbon", country_code: "PT", currency: "EUR", starts_on: "2026-10-01", ends_on: "2026-10-10", status: "CONFIRMED" }],
};

describe("buildAdvisoryForms", () => {
  it("includes the complete operational creation journey", () => {
    const forms = buildAdvisoryForms(referenceData, "Europe/Lisbon");

    expect(forms.map((form) => form.id)).toEqual([
      "proposal",
      "reservation",
      "lead",
      "appointment",
      "campaign",
      "travel",
      "accommodation",
    ]);
  });

  it("uses reference data instead of duplicated operational values", () => {
    const forms = buildAdvisoryForms(referenceData, "Europe/Lisbon");
    const travel = forms.find((form) => form.id === "travel");

    expect(travel?.fields.find((field) => field.name === "guest")?.options?.[0]?.value).toBe("guest-1");
    expect(travel?.fields.find((field) => field.name === "currency")?.options).toEqual([{ label: "EUR", value: "EUR" }]);
    expect(travel?.fields.find((field) => field.name === "origin_timezone")?.defaultValue).toBe("Europe/Lisbon");
  });
});
