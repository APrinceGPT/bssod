/**
 * Unit tests for constants
 */

import { UPLOAD_CONFIG, API_CONFIG, PROGRESS_PHASES, PROGRESS_MESSAGES } from "@/lib/constants";

describe("constants", () => {
  describe("UPLOAD_CONFIG", () => {
    it("should have MAX_FILE_SIZE_MB defined", () => {
      expect(UPLOAD_CONFIG.MAX_FILE_SIZE_MB).toBeDefined();
      expect(UPLOAD_CONFIG.MAX_FILE_SIZE_MB).toBeGreaterThan(0);
    });

    it("should have MAX_FILE_SIZE_BYTES matching MB value", () => {
      const expectedBytes = UPLOAD_CONFIG.MAX_FILE_SIZE_MB * 1024 * 1024;
      expect(UPLOAD_CONFIG.MAX_FILE_SIZE_BYTES).toBe(expectedBytes);
    });

    it("should have ACCEPTED_FILE_TYPES defined", () => {
      expect(UPLOAD_CONFIG.ACCEPTED_FILE_TYPES).toBeDefined();
      expect(UPLOAD_CONFIG.ACCEPTED_FILE_TYPES).toContain(".zip");
    });
  });

  describe("API_CONFIG", () => {
    it("should have BASE_URL defined", () => {
      expect(API_CONFIG.BASE_URL).toBeDefined();
      expect(typeof API_CONFIG.BASE_URL).toBe("string");
    });

    it("should have TIMEOUT_MS defined and reasonable", () => {
      expect(API_CONFIG.TIMEOUT_MS).toBeDefined();
      expect(API_CONFIG.TIMEOUT_MS).toBeGreaterThanOrEqual(30000);
    });
  });

  describe("PROGRESS_PHASES", () => {
    it("should have UPLOAD phase starting at 0", () => {
      expect(PROGRESS_PHASES.UPLOAD_START).toBe(0);
      expect(PROGRESS_PHASES.UPLOAD_END).toBe(40);
    });

    it("should have ANALYSIS phase", () => {
      expect(PROGRESS_PHASES.ANALYSIS_START).toBeDefined();
      expect(PROGRESS_PHASES.ANALYSIS_END).toBeDefined();
    });

    it("should have COMPLETE phase ending at 100", () => {
      expect(PROGRESS_PHASES.COMPLETE_END).toBe(100);
    });

    it("should have phases in correct order", () => {
      expect(PROGRESS_PHASES.UPLOAD_END).toBeLessThanOrEqual(PROGRESS_PHASES.VALIDATION_START);
      expect(PROGRESS_PHASES.VALIDATION_END).toBeLessThanOrEqual(PROGRESS_PHASES.ANALYSIS_START);
      expect(PROGRESS_PHASES.ANALYSIS_END).toBeLessThanOrEqual(PROGRESS_PHASES.COMPLETE_START);
    });
  });

  describe("PROGRESS_MESSAGES", () => {
    it("should have all progress messages defined", () => {
      expect(PROGRESS_MESSAGES.UPLOADING).toBeDefined();
      expect(PROGRESS_MESSAGES.VALIDATING).toBeDefined();
      expect(PROGRESS_MESSAGES.ANALYZING).toBeDefined();
      expect(PROGRESS_MESSAGES.PREPARING).toBeDefined();
    });
  });
});
