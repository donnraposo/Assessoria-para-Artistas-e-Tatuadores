import { describe, expect, it } from "vitest";

import { formatCurrency, formatOperationalValue, humanizeAction, humanizeField, statusTone } from "./format";

describe("formatCurrency", () => {
  it("formats monetary values with their own currency", () => {
    expect(formatCurrency("1234.50", "USD")).toBe("$1,234.50");
  });
});

describe("humanizeAction", () => {
  it("converts audit actions into readable labels", () => {
    expect(humanizeAction("guest.status_changed")).toBe("Guest Status Changed");
  });
});

describe("operational formatting", () => {
  it("humanizes field names and statuses", () => {
    expect(humanizeField("guest_id")).toBe("Guest Id");
    expect(formatOperationalValue("status", "UNDER_REVIEW")).toBe("Under Review");
  });
});

describe("statusTone", () => {
  it("maps concluded states to the positive tone", () => {
    expect(statusTone("APPROVED")).toBe("positive");
    expect(statusTone("CONFIRMED")).toBe("positive");
  });

  it("maps refused states to the danger tone", () => {
    expect(statusTone("REJECTED")).toBe("danger");
    expect(statusTone("CANCELLED")).toBe("danger");
  });

  it("maps states waiting for a decision to the warning tone", () => {
    expect(statusTone("UNDER_REVIEW")).toBe("warning");
    expect(statusTone("PENDING")).toBe("warning");
    expect(statusTone("EXPECTED")).toBe("warning");
    expect(statusTone("DUE")).toBe("warning");
  });

  it("maps states in progress to the info tone", () => {
    expect(statusTone("IN_PROGRESS")).toBe("info");
  });

  it("falls back to the neutral tone for unknown or missing states", () => {
    expect(statusTone("DRAFT")).toBe("neutral");
    expect(statusTone(null)).toBe("neutral");
    expect(statusTone("SOMETHING_ELSE")).toBe("neutral");
  });
});
