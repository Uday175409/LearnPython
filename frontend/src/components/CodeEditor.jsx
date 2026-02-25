// ============================================================
// components/CodeEditor.jsx — Touch-Friendly Code Editor
// ============================================================
// A mobile-optimized code editor built on react-simple-code-editor.
// Features:
//   - Syntax highlighting via PrismJS
//   - Large touch targets
//   - Sticky "Run Code" button
//   - No hover interactions
// ============================================================

import React, { useState, useCallback } from "react";
import Editor from "react-simple-code-editor";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import "prismjs/themes/prism-tomorrow.css";
import "./CodeEditor.css";

/**
 * CodeEditor — a touch-friendly Python code editor.
 *
 * Props:
 *   initialCode  — the starting code (string)
 *   onRun        — called with the code string when "Run" is tapped
 *   running      — boolean, true when code is being executed
 *   buttonLabel  — text for the run button (default: "▶ Run Code")
 *   onCodeChange — optional callback when code changes
 */
export default function CodeEditor({
  initialCode = "",
  onRun,
  running = false,
  buttonLabel = "▶ Run Code",
  onCodeChange,
}) {
  const [code, setCode] = useState(initialCode);

  // Highlight Python code using PrismJS
  const highlight = useCallback((code) => {
    return Prism.highlight(code, Prism.languages.python, "python");
  }, []);

  function handleCodeChange(newCode) {
    setCode(newCode);
    if (onCodeChange) {
      onCodeChange(newCode);
    }
  }

  function handleRun() {
    if (onRun && !running) {
      onRun(code);
    }
  }

  return (
    <div className="code-editor-wrapper">
      {/* The editable code area */}
      <div className="code-editor-container">
        <Editor
          value={code}
          onValueChange={handleCodeChange}
          highlight={highlight}
          padding={16}
          className="code-editor"
          textareaClassName="code-editor-textarea"
          style={{
            fontFamily: '"Fira Code", "Courier New", monospace',
            fontSize: "15px",
            lineHeight: "1.6",
            minHeight: "120px",
          }}
          placeholder="# Type your Python code here..."
        />
      </div>

      {/* Sticky Run Button — always visible on mobile */}
      <div className="code-editor-actions">
        <button
          className={`run-button ${running ? "running" : ""}`}
          onClick={handleRun}
          disabled={running}
        >
          {running ? "⏳ Running..." : buttonLabel}
        </button>
      </div>
    </div>
  );
}
