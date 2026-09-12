import { describe, expect, it } from "vitest";

import { ApplicationStatusPresenter } from "./ApplicationStatusPresenter";

describe("ApplicationStatusPresenter", () => {
  it("labels every application state", () => {
    expect(ApplicationStatusPresenter.label("UNDER_REVIEW")).toBe("Under review");
    expect(ApplicationStatusPresenter.label("DRAFT")).toBe("Draft");
  });

  it("separates approved and rejected by tone", () => {
    expect(ApplicationStatusPresenter.tone("APPROVED")).toBe("positive");
    expect(ApplicationStatusPresenter.tone("REJECTED")).toBe("negative");
  });

  it("explains what the Artist should expect next", () => {
    expect(ApplicationStatusPresenter.guidanceText("REJECTED")).toContain("reason");
  });
});
