// ============================================================
// pages/PlaygroundPage.jsx — Free Code Playground
// ============================================================
// A sandbox where students can write and run Python code
// freely, outside of any lesson or exercise.
// ============================================================

import React, { useState } from "react";
import CodeEditor from "../components/CodeEditor";
import OutputPanel from "../components/OutputPanel";
import { runCode } from "../api";
import "./PlaygroundPage.css";

const DEFAULT_CODE = `# Welcome to the Python Playground! 🐍
# Write any Python code here and tap "Run Code" to see the result.

# Try this:
name = "World"
print(f"Hello, {name}!")

# Or try some math:
print(2 + 2)
print(10 * 5)
`;

export default function PlaygroundPage() {
  const [output, setOutput] = useState(null);
  const [running, setRunning] = useState(false);

  async function handleRun(code) {
    setRunning(true);
    setOutput(null);
    try {
      const result = await runCode(code);
      setOutput(result);
    } catch (err) {
      setOutput({
        output: "",
        error: err.message,
        friendly_error: "Unable to run code. Check your internet connection.",
        execution_time_ms: 0,
      });
    }
    setRunning(false);
  }

  return (
    <div className="playground-page">
      <h1 className="page-title">🎮 Python Playground</h1>
      <p className="page-subtitle">
        Write any Python code and run it! This is your safe space to
        experiment. You can't break anything.
      </p>

      <CodeEditor
        initialCode={DEFAULT_CODE}
        onRun={handleRun}
        running={running}
        buttonLabel="▶ Run Code"
      />

      <OutputPanel
        output={output?.output || ""}
        error={output?.error || ""}
        friendlyError={output?.friendly_error || ""}
        executionTime={output?.execution_time_ms || 0}
        visible={output !== null}
      />

      {/* Quick Examples */}
      <div className="playground-examples">
        <h3>💡 Quick Examples to Try</h3>
        <div className="example-chips">
          <button
            className="example-chip"
            onClick={() => {
              // Cannot set code directly via state from outside
              // So we provide a hint
            }}
          >
            print("Hello!")
          </button>
          <button className="example-chip">
            for i in range(5): print(i)
          </button>
          <button className="example-chip">
            import math; print(math.pi)
          </button>
        </div>
      </div>
    </div>
  );
}
