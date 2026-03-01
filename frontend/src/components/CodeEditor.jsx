// ============================================================
// components/CodeEditor.jsx — Smart Mobile Code Editor
// ============================================================
// Features:
//   - Syntax highlighting via PrismJS
//   - Auto-indent after colon (Python-aware)
//   - Auto-close brackets/quotes  ()  []  {}  ""  ''
//   - Smart backspace (removes pair)
//   - Closing bracket skip (jump over instead of doubling)
//   - Tab → 4 spaces, Shift+Tab → dedent
//   - Mobile toolbar: quick-insert common Python symbols
// ============================================================

import React, { useState, useCallback, useEffect, useRef, useLayoutEffect } from "react";
import Editor from "react-simple-code-editor";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import "prismjs/themes/prism-tomorrow.css";
import "./CodeEditor.css";

// Pairs that auto-close
const OPEN_PAIRS = { "(": ")", "[": "]", "{": "}", '"': '"', "'": "'" };
// Characters that should be skipped over when already present
const CLOSE_SET  = new Set([")", "]", "}"]);

export default function CodeEditor({
  initialCode = "",
  onRun,
  running = false,
  buttonLabel = "▶ Run Code",
  onCodeChange,
}) {
  const [code, setCode]       = useState(initialCode);
  const containerRef          = useRef(null);
  const pendingCursor         = useRef(null); // { start, end } to apply after next render

  // Reset when exercise/lesson changes
  useEffect(() => { setCode(initialCode); }, [initialCode]);

  // After every render, restore any pending cursor position
  useLayoutEffect(() => {
    if (pendingCursor.current === null) return;
    const ta = containerRef.current?.querySelector("textarea");
    if (ta) {
      const { start, end } = pendingCursor.current;
      ta.selectionStart = start;
      ta.selectionEnd   = end;
    }
    pendingCursor.current = null;
  });

  const highlight = useCallback(
    (src) => Prism.highlight(src, Prism.languages.python, "python"),
    []
  );

  // ── helpers ────────────────────────────────────────────────
  function applyEdit(newCode, cursorStart, cursorEnd = cursorStart) {
    pendingCursor.current = { start: cursorStart, end: cursorEnd };
    setCode(newCode);
    if (onCodeChange) onCodeChange(newCode);
  }

  function moveCursor(pos) {
    // Move cursor without changing code (for skip-over logic)
    requestAnimationFrame(() => {
      const ta = containerRef.current?.querySelector("textarea");
      if (ta) { ta.selectionStart = ta.selectionEnd = pos; }
    });
  }

  // ── keyboard handler ───────────────────────────────────────
  function handleKeyDown(e) {
    const ta  = e.target;
    const val = ta.value;
    const ss  = ta.selectionStart;
    const se  = ta.selectionEnd;

    // ── Tab / Shift+Tab ──────────────────────────────────────
    if (e.key === "Tab") {
      e.preventDefault();
      if (e.shiftKey) {
        // Dedent: strip up to 4 leading spaces from current line
        const lineStart = val.lastIndexOf("\n", ss - 1) + 1;
        const spaces    = val.substring(lineStart).match(/^( {1,4})/)?.[1]?.length ?? 0;
        if (spaces > 0) {
          applyEdit(
            val.substring(0, lineStart) + val.substring(lineStart + spaces),
            Math.max(lineStart, ss - spaces)
          );
        }
      } else {
        applyEdit(val.substring(0, ss) + "    " + val.substring(se), ss + 4);
      }
      return;
    }

    // ── Enter → smart indent ─────────────────────────────────
    if (e.key === "Enter") {
      e.preventDefault();
      const lineStart   = val.lastIndexOf("\n", ss - 1) + 1;
      const currentLine = val.substring(lineStart, ss);
      const baseIndent  = currentLine.match(/^(\s*)/)[1];
      const extraIndent = currentLine.trimEnd().endsWith(":") ? "    " : "";
      const insertion   = "\n" + baseIndent + extraIndent;
      applyEdit(val.substring(0, ss) + insertion + val.substring(se), ss + insertion.length);
      return;
    }

    // ── Backspace → delete matching pair ────────────────────
    if (e.key === "Backspace" && ss === se && ss > 0) {
      const prev  = val[ss - 1];
      const next  = val[ss];
      if (OPEN_PAIRS[prev] && next === OPEN_PAIRS[prev]) {
        e.preventDefault();
        applyEdit(val.substring(0, ss - 1) + val.substring(ss + 1), ss - 1);
        return;
      }
    }

    // ── Closing bracket skip ─────────────────────────────────
    if (CLOSE_SET.has(e.key) && ss === se && val[ss] === e.key) {
      e.preventDefault();
      moveCursor(ss + 1);
      return;
    }

    // ── Auto-close opening bracket / quote ──────────────────
    if (OPEN_PAIRS[e.key]) {
      e.preventDefault();
      const close = OPEN_PAIRS[e.key];
      // Quote skip: if cursor is already before the same quote, jump over
      if ((e.key === '"' || e.key === "'") && ss === se && val[ss] === e.key) {
        moveCursor(ss + 1);
        return;
      }
      if (ss !== se) {
        // Wrap selected text
        const selected = val.substring(ss, se);
        applyEdit(
          val.substring(0, ss) + e.key + selected + close + val.substring(se),
          ss + 1, se + 1
        );
      } else {
        applyEdit(val.substring(0, ss) + e.key + close + val.substring(ss), ss + 1);
      }
      return;
    }
  }

  // ── code change ────────────────────────────────────────────
  function handleCodeChange(newCode) {
    setCode(newCode);
    if (onCodeChange) onCodeChange(newCode);
  }

  // ── mobile toolbar insert ──────────────────────────────────
  function insertAtCursor(text, cursorOffset = 0) {
    const ta = containerRef.current?.querySelector("textarea");
    if (!ta) return;
    const ss = ta.selectionStart;
    const se = ta.selectionEnd;
    const newCode = code.substring(0, ss) + text + code.substring(se);
    applyEdit(newCode, ss + text.length - cursorOffset);
    // Re-focus the editor after toolbar tap
    requestAnimationFrame(() => ta.focus());
  }

  // ── toolbar definition ─────────────────────────────────────
  const TOOLBAR = [
    { label: "⇥",   title: "Indent (4 spaces)",   text: "    ",   off: 0 },
    { label: ":",   title: "Colon",                text: ":",      off: 0 },
    { label: "()",  title: "Parentheses",          text: "()",     off: 1 },
    { label: "[]",  title: "Square brackets",      text: "[]",     off: 1 },
    { label: "{}",  title: "Curly braces",         text: "{}",     off: 1 },
    { label: "\"\"", title: "Double quotes",       text: '""',     off: 1 },
    { label: "''",  title: "Single quotes",        text: "''",     off: 1 },
    { label: "#",   title: "Comment",              text: "# ",     off: 0 },
    { label: "=",   title: "Assign",               text: " = ",    off: 0 },
    { label: "==",  title: "Equal",                text: " == ",   off: 0 },
    { label: "!=",  title: "Not equal",            text: " != ",   off: 0 },
    { label: "+=",  title: "Increment",            text: " += ",   off: 0 },
    { label: "not", title: "not",                  text: "not ",   off: 0 },
    { label: "and", title: "and",                  text: " and ",  off: 0 },
    { label: "or",  title: "or",                   text: " or ",   off: 0 },
  ];

  function handleRun() {
    if (onRun && !running) onRun(code);
  }

  return (
    <div className="code-editor-wrapper">

      {/* ── Mobile symbol toolbar ─────────────────────────── */}
      <div className="code-toolbar" role="toolbar" aria-label="Python symbols">
        {TOOLBAR.map(({ label, title, text, off }) => (
          <button
            key={title}
            className="toolbar-btn"
            title={title}
            // onMouseDown / onTouchEnd both prevent focus leaving the textarea
            onMouseDown={(e) => { e.preventDefault(); insertAtCursor(text, off); }}
            onTouchEnd={(e)  => { e.preventDefault(); insertAtCursor(text, off); }}
            tabIndex={-1}
            type="button"
          >
            {label}
          </button>
        ))}
      </div>

      {/* ── Editable code area ───────────────────────────── */}
      <div className="code-editor-container" ref={containerRef}>
        <Editor
          value={code}
          onValueChange={handleCodeChange}
          highlight={highlight}
          onKeyDown={handleKeyDown}
          padding={16}
          className="code-editor"
          textareaClassName="code-editor-textarea"
          style={{
            fontFamily: '"Fira Code", "Courier New", Courier, monospace',
            fontSize: "15px",
            lineHeight: "1.6",
            letterSpacing: "normal",
            minHeight: "120px",
          }}
          placeholder="# Type your Python code here..."
        />
      </div>

      {/* ── Sticky Run Button ─────────────────────────────── */}
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

