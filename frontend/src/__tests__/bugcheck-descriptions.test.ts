/**
 * Unit tests for bugcheck-descriptions utility
 */

import { BUGCHECK_DESCRIPTIONS, getBugcheckDescription } from "@/lib/bugcheck-descriptions";

describe("bugcheck-descriptions", () => {
  describe("BUGCHECK_DESCRIPTIONS", () => {
    it("should contain at least 30 bugcheck descriptions", () => {
      const count = Object.keys(BUGCHECK_DESCRIPTIONS).length;
      expect(count).toBeGreaterThanOrEqual(30);
    });

    it("should have non-empty descriptions for all entries", () => {
      Object.entries(BUGCHECK_DESCRIPTIONS).forEach(([key, value]) => {
        expect(value).toBeTruthy();
        expect(value.length).toBeGreaterThan(10);
        expect(key).toBeTruthy();
      });
    });

    it("should contain IRQL_NOT_LESS_OR_EQUAL", () => {
      expect(BUGCHECK_DESCRIPTIONS["IRQL_NOT_LESS_OR_EQUAL"]).toBeDefined();
    });

    it("should contain CRITICAL_PROCESS_DIED", () => {
      expect(BUGCHECK_DESCRIPTIONS["CRITICAL_PROCESS_DIED"]).toBeDefined();
    });

    it("should contain PAGE_FAULT_IN_NONPAGED_AREA", () => {
      expect(BUGCHECK_DESCRIPTIONS["PAGE_FAULT_IN_NONPAGED_AREA"]).toBeDefined();
    });
  });

  describe("getBugcheckDescription", () => {
    it("should return description for known bugcheck", () => {
      const description = getBugcheckDescription("IRQL_NOT_LESS_OR_EQUAL");
      expect(description).toBeDefined();
      expect(description).toContain("IRQL");
    });

    it("should return undefined for unknown bugcheck", () => {
      const description = getBugcheckDescription("UNKNOWN_BUGCHECK_CODE");
      expect(description).toBeUndefined();
    });

    it("should be case-sensitive", () => {
      const description = getBugcheckDescription("irql_not_less_or_equal");
      expect(description).toBeUndefined();
    });
  });
});
