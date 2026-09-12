import { describe, expect, it } from "vitest";

import { StyleListParser } from "./StyleListParser";

describe("StyleListParser", () => {
  it("splits, trims and removes duplicated styles", () => {
    expect(StyleListParser.parse(" blackwork , fine line ,blackwork,  ")).toEqual([
      "blackwork",
      "fine line",
    ]);
  });

  it("returns an empty list when nothing was typed", () => {
    expect(StyleListParser.parse("   ")).toEqual([]);
  });

  it("renders stored styles back into the editable field", () => {
    expect(StyleListParser.format(["blackwork", "fine line"])).toBe("blackwork, fine line");
  });
});
