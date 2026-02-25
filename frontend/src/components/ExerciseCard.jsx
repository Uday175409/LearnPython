// ============================================================
// components/ExerciseCard.jsx — Interactive Exercise Widget
// ============================================================
// A self-contained exercise component with:
//   - Instructions
//   - Code editor with starter code
//   - Run and Submit buttons
//   - Hint toggle
//   - Solution reveal
//   - Test results display
// ============================================================

import React, { useState } from "react";
import CodeEditor from "./CodeEditor";
import OutputPanel from "./OutputPanel";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { runCode, submitExercise, getExerciseSolution } from "../api";
import "./ExerciseCard.css";

export default function ExerciseCard({ exercise }) {
  // ── State ─────────────────────────────────────────────────
  const [output, setOutput] = useState(null);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [solution, setSolution] = useState(null);
  const [submitResult, setSubmitResult] = useState(null);
  const [currentCode, setCurrentCode] = useState(exercise.starter_code || "");

  // ── Run Code (just execute, no grading) ───────────────────
  async function handleRun(code) {
    setRunning(true);
    setOutput(null);
    setSubmitResult(null);
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

  // ── Submit Code (run tests and grade) ─────────────────────
  async function handleSubmit() {
    setSubmitting(true);
    setOutput(null);
    setSubmitResult(null);
    try {
      const result = await submitExercise(exercise.id, currentCode);
      setSubmitResult(result);
    } catch (err) {
      setSubmitResult({
        is_correct: false,
        message: "Unable to submit. Check your internet connection.",
        output: "",
        error: err.message,
        friendly_error: "",
        test_results: [],
      });
    }
    setSubmitting(false);
  }

  // ── Reveal Solution ───────────────────────────────────────
  async function handleShowSolution() {
    if (solution) {
      setShowSolution(!showSolution);
      return;
    }
    try {
      const data = await getExerciseSolution(exercise.id);
      setSolution(data);
      setShowSolution(true);
    } catch {
      setSolution({ solution: "Unable to load solution.", explanation: "" });
      setShowSolution(true);
    }
  }

  return (
    <div className="exercise-card" id={`exercise-${exercise.id}`}>
      {/* Exercise Header */}
      <div className="exercise-header">
        <h3 className="exercise-title">
          ✏️ Exercise: {exercise.title}
        </h3>
        <span className={`difficulty-badge ${exercise.difficulty}`}>
          {exercise.difficulty}
        </span>
      </div>

      {/* Instructions */}
      <div className="exercise-instructions">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {exercise.instructions}
        </ReactMarkdown>
      </div>

      {/* Code Editor */}
      <CodeEditor
        initialCode={exercise.starter_code || ""}
        onRun={handleRun}
        running={running}
        buttonLabel="▶ Run Code"
        onCodeChange={setCurrentCode}
      />

      {/* Submit Button (separate from Run) */}
      <button
        className={`submit-button ${submitResult?.is_correct ? "correct" : ""}`}
        onClick={handleSubmit}
        disabled={submitting}
      >
        {submitting
          ? "⏳ Checking..."
          : submitResult?.is_correct
          ? "🎉 Passed!"
          : "📤 Submit Answer"}
      </button>

      {/* Output Panel (from Run) */}
      {output && (
        <OutputPanel
          output={output.output}
          error={output.error}
          friendlyError={output.friendly_error}
          executionTime={output.execution_time_ms}
          visible={true}
        />
      )}

      {/* Submit Result */}
      {submitResult && (
        <div
          className={`submit-result ${
            submitResult.is_correct ? "correct" : "incorrect"
          }`}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {submitResult.message}
          </ReactMarkdown>
          {submitResult.friendly_error && (
            <div className="submit-error-explanation">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {submitResult.friendly_error}
              </ReactMarkdown>
            </div>
          )}
        </div>
      )}

      {/* Help Buttons */}
      <div className="exercise-help">
        {/* Hint Toggle */}
        {exercise.hint && (
          <button
            className="help-button"
            onClick={() => setShowHint(!showHint)}
          >
            {showHint ? "🙈 Hide Hint" : "💡 Show Hint"}
          </button>
        )}

        {/* Solution Toggle */}
        <button className="help-button solution-btn" onClick={handleShowSolution}>
          {showSolution ? "🙈 Hide Solution" : "🔑 Show Solution"}
        </button>
      </div>

      {/* Hint Content */}
      {showHint && exercise.hint && (
        <div className="hint-box">
          <p>{exercise.hint}</p>
        </div>
      )}

      {/* Solution Content */}
      {showSolution && solution && (
        <div className="solution-box">
          <h4>Solution:</h4>
          <pre className="solution-code">{solution.solution}</pre>
          {solution.explanation && (
            <>
              <h4>Why this works:</h4>
              <p className="solution-explanation">{solution.explanation}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}
