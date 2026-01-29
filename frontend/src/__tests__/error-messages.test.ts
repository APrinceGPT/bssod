/**
 * Unit tests for error-messages utility
 */

import { 
  getUserFriendlyError, 
  formatErrorMessage,
  ErrorCode
} from "@/lib/error-messages";

describe("error-messages", () => {
  describe("getUserFriendlyError", () => {
    it("should return network error for network error message", () => {
      const error = getUserFriendlyError("Network error - could not connect to server", 0);
      expect(error.code).toBe(ErrorCode.CONNECTION_REFUSED);
      expect(error.suggestion).toBeDefined();
    });

    it("should return bad request error for status 400", () => {
      const error = getUserFriendlyError("any message", 400);
      expect(error.code).toBe(ErrorCode.BAD_REQUEST);
    });

    it("should return server error for status 500", () => {
      const error = getUserFriendlyError("any message", 500);
      expect(error.code).toBe(ErrorCode.SERVER_ERROR);
    });

    it("should return timeout error for timeout message", () => {
      const error = getUserFriendlyError("Request timed out", 0);
      expect(error.code).toBe(ErrorCode.TIMEOUT);
    });

    it("should handle generic errors", () => {
      const error = getUserFriendlyError("Unknown error", 418);
      expect(error.title).toBeDefined();
      expect(error.message).toBeDefined();
    });

    it("should handle connection refused pattern", () => {
      const error = getUserFriendlyError("connection refused");
      expect(error.code).toBe(ErrorCode.CONNECTION_REFUSED);
    });
  });

  describe("formatErrorMessage", () => {
    it("should format error with message only", () => {
      const error = { 
        code: ErrorCode.UNKNOWN, 
        title: "Test Error", 
        message: "This is a test" 
      };
      const formatted = formatErrorMessage(error);
      expect(formatted).toContain("This is a test");
    });

    it("should include suggestion if provided", () => {
      const error = { 
        code: ErrorCode.UNKNOWN, 
        title: "Error", 
        message: "Desc", 
        suggestion: "Do this" 
      };
      const formatted = formatErrorMessage(error);
      expect(formatted).toContain("Desc");
      expect(formatted).toContain("Do this");
    });
  });
});
