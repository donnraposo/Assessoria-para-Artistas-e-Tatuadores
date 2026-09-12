import { describe, expect, it } from "vitest";

import { formatCurrency, humanizeAction } from "./format";

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

