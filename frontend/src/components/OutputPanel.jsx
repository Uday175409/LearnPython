// ============================================================
// components/OutputPanel.jsx — Code Execution Output Display
// ============================================================
// Shows the result of running code — either output or error.
// Errors are shown with the friendly explanation from the backend.
// ============================================================

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./OutputPanel.css";

/**
 * OutputPanel — displays code execution results.
 *
 * Props:
 *   output       — stdout text from the code
 *   error        — raw error text
 *   friendlyError — plain-English error explanation
 *   executionTime — milliseconds the code took
 *   visible       — whether to show the panel
 */
export default function OutputPanel({
  output = "",
  error = "",
  friendlyError = "",
  executionTime = 0,
  visible = false,
}) {
  if (!visible) return null;

  const hasError = error && error.length > 0;
  const hasOutput = output && output.length > 0;

  return (
    <div className={`output-panel ${hasError ? "has-error" : "has-output"}`}>
      {/* Header with execution time */}
      <div className="output-header">
        <span className="output-label">
          {hasError ? "❌ Error" : "✅ Output"}
        </span>
        {executionTime > 0 && (
          <span className="output-time">{executionTime}ms</span>
        )}
      </div>

      {/* Successful output */}
      {hasOutput && (
        <pre className="output-text">{output}</pre>
      )}

      {/* No output, no error */}
      {!hasOutput && !hasError && (
        <p className="output-empty">
          Your code ran successfully but didn't print anything.
          Use <code>print()</code> to see output!
        </p>
      )}

      {/* Friendly error explanation */}
      {hasError && friendlyError && (
        <div className="output-friendly-error">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {friendlyError}
          </ReactMarkdown>
        </div>
      )}

      {/* Raw error (collapsed by default for beginners) */}
      {hasError && (
        <details className="output-raw-error">
          <summary>Show technical error details</summary>
          <pre className="output-error-text">{error}</pre>
        </details>
      )}
    </div>
  );
}
