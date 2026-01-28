"use client";

import { useMemo } from "react";

interface MarkdownRendererProps {
  content: string;
}

/**
 * Simple Markdown renderer for AI analysis output.
 * Handles basic markdown: headers, bold, italic, lists, code blocks.
 */
export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const rendered = useMemo(() => {
    return parseMarkdown(content);
  }, [content]);

  return <div className="space-y-4">{rendered}</div>;
}

function parseMarkdown(text: string): React.ReactNode[] {
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];
  let currentList: string[] = [];
  let currentNumberedList: string[] = [];
  let inCodeBlock = false;
  let codeBlockContent: string[] = [];
  let key = 0;

  const flushList = () => {
    if (currentList.length > 0) {
      elements.push(
        <ul key={key++} className="list-disc list-inside space-y-1 ml-2">
          {currentList.map((item, i) => (
            <li key={i} className="text-foreground">
              {parseInlineMarkdown(item)}
            </li>
          ))}
        </ul>
      );
      currentList = [];
    }
  };

  const flushNumberedList = () => {
    if (currentNumberedList.length > 0) {
      elements.push(
        <ol key={key++} className="list-decimal list-inside space-y-1 ml-2">
          {currentNumberedList.map((item, i) => (
            <li key={i} className="text-foreground">
              {parseInlineMarkdown(item)}
            </li>
          ))}
        </ol>
      );
      currentNumberedList = [];
    }
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Code block handling
    if (line.startsWith("```")) {
      if (inCodeBlock) {
        // End code block
        elements.push(
          <pre key={key++} className="bg-muted p-4 rounded-lg overflow-x-auto">
            <code className="text-sm font-mono">{codeBlockContent.join("\n")}</code>
          </pre>
        );
        codeBlockContent = [];
        inCodeBlock = false;
      } else {
        // Start code block
        flushList();
        flushNumberedList();
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockContent.push(line);
      continue;
    }

    // Empty line
    if (line.trim() === "") {
      flushList();
      flushNumberedList();
      continue;
    }

    // Headers
    if (line.startsWith("### ")) {
      flushList();
      flushNumberedList();
      elements.push(
        <h3 key={key++} className="text-lg font-semibold text-foreground mt-4">
          {parseInlineMarkdown(line.slice(4))}
        </h3>
      );
      continue;
    }

    if (line.startsWith("## ")) {
      flushList();
      flushNumberedList();
      elements.push(
        <h2 key={key++} className="text-xl font-bold text-foreground mt-6">
          {parseInlineMarkdown(line.slice(3))}
        </h2>
      );
      continue;
    }

    if (line.startsWith("# ")) {
      flushList();
      flushNumberedList();
      elements.push(
        <h1 key={key++} className="text-2xl font-bold text-foreground mt-6">
          {parseInlineMarkdown(line.slice(2))}
        </h1>
      );
      continue;
    }

    // Unordered list
    if (line.match(/^[-*]\s+/)) {
      flushNumberedList();
      currentList.push(line.replace(/^[-*]\s+/, ""));
      continue;
    }

    // Numbered list
    if (line.match(/^\d+\.\s+/)) {
      flushList();
      currentNumberedList.push(line.replace(/^\d+\.\s+/, ""));
      continue;
    }

    // Horizontal rule
    if (line.match(/^---+$/)) {
      flushList();
      flushNumberedList();
      elements.push(<hr key={key++} className="my-4 border-border" />);
      continue;
    }

    // Regular paragraph
    flushList();
    flushNumberedList();
    elements.push(
      <p key={key++} className="text-foreground leading-relaxed">
        {parseInlineMarkdown(line)}
      </p>
    );
  }

  // Flush any remaining lists
  flushList();
  flushNumberedList();

  return elements;
}

function parseInlineMarkdown(text: string): React.ReactNode {
  // Process inline elements
  const parts: React.ReactNode[] = [];
  let remaining = text;
  let key = 0;

  while (remaining.length > 0) {
    // Bold: **text**
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    // Italic: *text* or _text_
    const italicMatch = remaining.match(/(?<!\*)\*([^*]+)\*(?!\*)|_([^_]+)_/);
    // Inline code: `code`
    const codeMatch = remaining.match(/`([^`]+)`/);

    // Find earliest match
    const matches = [
      boldMatch ? { type: "bold", match: boldMatch, index: boldMatch.index! } : null,
      italicMatch ? { type: "italic", match: italicMatch, index: italicMatch.index! } : null,
      codeMatch ? { type: "code", match: codeMatch, index: codeMatch.index! } : null,
    ]
      .filter(Boolean)
      .sort((a, b) => a!.index - b!.index);

    if (matches.length === 0) {
      parts.push(remaining);
      break;
    }

    const firstMatch = matches[0]!;

    // Add text before match
    if (firstMatch.index > 0) {
      parts.push(remaining.slice(0, firstMatch.index));
    }

    // Add formatted element
    if (firstMatch.type === "bold") {
      parts.push(
        <strong key={key++} className="font-semibold">
          {firstMatch.match[1]}
        </strong>
      );
    } else if (firstMatch.type === "italic") {
      parts.push(
        <em key={key++} className="italic">
          {firstMatch.match[1] || firstMatch.match[2]}
        </em>
      );
    } else if (firstMatch.type === "code") {
      parts.push(
        <code key={key++} className="bg-muted px-1.5 py-0.5 rounded font-mono text-sm">
          {firstMatch.match[1]}
        </code>
      );
    }

    remaining = remaining.slice(firstMatch.index + firstMatch.match[0].length);
  }

  return parts.length === 1 ? parts[0] : parts;
}
