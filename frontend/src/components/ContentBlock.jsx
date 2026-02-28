// ============================================================
// components/ContentBlock.jsx — Lesson Content Renderer
// ============================================================
// Renders the different types of content blocks that make up
// a lesson: text, code samples, tips, common mistakes.
// ============================================================

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import "./ContentBlock.css";

/**
 * ContentBlock renders one content block from a lesson.
 *
 * Block types:
 *   - text:    Markdown text explanation
 *   - code:    Python code snippet with optional caption
 *   - tip:     A helpful tip in a highlight box
 *   - mistake: Common beginner mistake with wrong/right code
 */
export default function ContentBlock({ block }) {
  if (!block) return null;

  switch (block.type) {
    case "text":
      return (
        <div className="content-block content-text">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {block.body}
          </ReactMarkdown>
        </div>
      );

    case "code":
      return (
        <div className="content-block content-code">
          <pre className="code-sample">
            <code
              dangerouslySetInnerHTML={{
                __html: Prism.highlight(
                  block.body || "",
                  Prism.languages.python,
                  "python"
                ),
              }}
            />
          </pre>
          {block.caption && (
            <p className="code-caption">{block.caption}</p>
          )}
        </div>
      );

    case "tip":
      return (
        <div className="content-block content-tip">
          <div className="tip-icon">💡</div>
          <div className="tip-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {block.body}
            </ReactMarkdown>
          </div>
        </div>
      );

    case "mistake":
      return (
        <div className="content-block content-mistake">
          <h4 className="mistake-header">⚠️ Common Mistake</h4>
          <div className="mistake-comparison">
            <div className="mistake-wrong">
              <span className="mistake-label">❌ Wrong</span>
              <pre className="code-sample small">
                <code
                  dangerouslySetInnerHTML={{
                    __html: Prism.highlight(
                      block.wrong || "",
                      Prism.languages.python,
                      "python"
                    ),
                  }}
                />
              </pre>
            </div>
            <div className="mistake-right">
              <span className="mistake-label">✅ Right</span>
              <pre className="code-sample small">
                <code
                  dangerouslySetInnerHTML={{
                    __html: Prism.highlight(
                      block.right || "",
                      Prism.languages.python,
                      "python"
                    ),
                  }}
                />
              </pre>
            </div>
          </div>
          <p className="mistake-explanation">{block.explanation}</p>
        </div>
      );

    default:
      return null;
  }
}
