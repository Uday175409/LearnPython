# ============================================================
# sandbox.py — Safe Python Code Execution
# ============================================================
# This is the MOST SECURITY-CRITICAL part of the application.
#
# When a student taps "Run Code" on their phone, their code
# is sent to the server and executed HERE inside a restricted
# subprocess. We enforce:
#
#   1. TIME LIMIT — Code that runs too long is killed.
#   2. OUTPUT LIMIT — Huge output is truncated.
#   3. NO FILE ACCESS — Students can't read/write server files.
#   4. NO NETWORK — Students can't make web requests.
#   5. NO IMPORTS — Only safe modules are allowed.
#   6. SEPARATE PROCESS — Each run is isolated.
#
# This approach uses subprocess + RestrictedPython concepts.
# For production at scale, consider Docker-based isolation.
# ============================================================

import asyncio
import subprocess
import sys
import time
import tempfile
import os
from typing import Tuple

from django.conf import settings as django_settings


class _SandboxSettings:
    """Adapter so sandbox code doesn't change much."""
    @property
    def SANDBOX_TIMEOUT_SECONDS(self):
        return getattr(django_settings, 'SANDBOX_TIMEOUT_SECONDS', 5)

    @property
    def SANDBOX_MAX_OUTPUT_CHARS(self):
        return getattr(django_settings, 'SANDBOX_MAX_OUTPUT_CHARS', 5000)

    @property
    def SANDBOX_MAX_CODE_LENGTH(self):
        return getattr(django_settings, 'SANDBOX_MAX_CODE_LENGTH', 10000)

    @property
    def SANDBOX_MAX_MEMORY_BYTES(self):
        return getattr(django_settings, 'SANDBOX_MAX_MEMORY_BYTES', 64 * 1024 * 1024)


settings = _SandboxSettings()


# ── Blocked Patterns ─────────────────────────────────────────
# These are strings that should NEVER appear in student code.
# If any are found, we refuse to run the code immediately.
BLOCKED_PATTERNS = [
    "import os",
    "import sys",
    "import subprocess",
    "import shutil",
    "import socket",
    "import http",
    "import urllib",
    "import requests",
    "import pathlib",
    "import glob",
    "import pickle",
    "import shelve",
    "import sqlite3",
    "import ctypes",
    "import importlib",
    "import threading",
    "import multiprocessing",
    "import concurrent",
    "import signal",
    "import resource",
    "__import__",
    "eval(",
    "exec(",
    "compile(",
    "open(",
    "breakpoint(",
    "globals(",
    "locals(",
    "getattr(",
    "setattr(",
    "delattr(",
    "__builtins__",
    "__subclasses__",
    "__class__",
    "__bases__",
    "__mro__",
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.Popen",
    "exit(",
    "quit(",
    # Memory-bomb patterns
    "bytearray(",
    "memoryview(",
    "object.__",
]

# ── Allowed Imports ──────────────────────────────────────────
# Students usually only need these in beginner lessons.
ALLOWED_IMPORTS = [
    "math",
    "random",
    "string",
    "datetime",
    "collections",
    "itertools",
    "functools",
    "json",
    "re",
    "statistics",
    "decimal",
    "fractions",
    "textwrap",
]


def check_code_safety(code: str) -> Tuple[bool, str]:
    """
    Scan student code for dangerous patterns.

    Returns:
        (is_safe, message) — If not safe, message explains why.
    """
    # ── Code length guard ────────────────────────────────────
    max_len = settings.SANDBOX_MAX_CODE_LENGTH
    if len(code) > max_len:
        return False, (
            f"Your code is too long ({len(code):,} characters). "
            f"Please keep your code under {max_len:,} characters."
        )

    # ── Line count guard ─────────────────────────────────────
    lines = code.splitlines()
    if len(lines) > 500:
        return False, (
            f"Your code has too many lines ({len(lines)}). "
            f"Please keep it under 500 lines."
        )

    # Normalize the code to catch tricks like extra spaces
    normalized = " ".join(code.split())

    for pattern in BLOCKED_PATTERNS:
        if pattern in code or pattern in normalized:
            # Give a friendly explanation instead of a scary error
            return False, (
                f"Your code contains '{pattern}' which is not allowed "
                f"for security reasons. In these lessons, you don't "
                f"need to use this. Try a different approach!"
            )

    # Check that any import statements only use allowed modules
    for line in code.splitlines():
        stripped = line.strip()

        # Remove inline comments before parsing
        if "#" in stripped:
            stripped = stripped[:stripped.index("#")].strip()

        if not stripped:
            continue

        if stripped.startswith("import "):
            # Handle "import mod1, mod2, mod3" syntax
            modules_part = stripped[len("import "):].strip()
            module_names = [m.strip().split(".")[0].split(" ")[0]
                           for m in modules_part.split(",")]
            for module_name in module_names:
                if module_name and module_name not in ALLOWED_IMPORTS:
                    return False, (
                        f"The module '{module_name}' is not available "
                        f"in this learning environment. Available modules: "
                        f"{', '.join(ALLOWED_IMPORTS)}"
                    )
        elif stripped.startswith("from "):
            # Handle "from module import something"
            parts = stripped.split()
            if len(parts) >= 2:
                module_name = parts[1].split(".")[0]
                if module_name not in ALLOWED_IMPORTS:
                    return False, (
                        f"The module '{module_name}' is not available "
                        f"in this learning environment. Available modules: "
                        f"{', '.join(ALLOWED_IMPORTS)}"
                    )

    return True, ""


# ── Execution Wrapper Script ─────────────────────────────────
# We wrap the student's code inside this template before running
# it. The wrapper: limits recursion, captures output, etc.
WRAPPER_TEMPLATE = '''
import sys
import io

# Limit recursion to prevent infinite recursion crashes
sys.setrecursionlimit(200)

# Limit memory and CPU usage (Linux/Unix only — no-op on Windows)
try:
    import resource as _resource
    _MEM = {max_memory}
    _resource.setrlimit(_resource.RLIMIT_AS, (_MEM, _MEM))
    _resource.setrlimit(_resource.RLIMIT_CPU, ({timeout}, {timeout}))
except Exception:
    pass

# Capture all print output
_captured_output = io.StringIO()
sys.stdout = _captured_output
sys.stderr = _captured_output

try:
    # ── Student code begins ──
{student_code}
    # ── Student code ends ──
except MemoryError:
    print("MemoryError: Your code used too much memory and was stopped.", file=sys.stderr)
except Exception as _e:
    print(f"{{type(_e).__name__}}: {{_e}}", file=sys.stderr)

# Print captured output
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
_result = _captured_output.getvalue()
if len(_result) > {max_output}:
    _result = _result[:{max_output}] + "\\n... (output truncated — too much text)"
print(_result, end="")
'''


async def execute_code(code: str) -> dict:
    """
    Execute student Python code safely in a subprocess.

    Args:
        code: The Python code string from the student.

    Returns:
        A dict with keys: output, error, execution_time_ms
    """
    # ── Step 1: Safety check ─────────────────────────────────
    is_safe, safety_message = check_code_safety(code)
    if not is_safe:
        return {
            "output": "",
            "error": safety_message,
            "execution_time_ms": 0,
        }

    # ── Step 2: Prepare the wrapped code ─────────────────────
    # Indent student code by 4 spaces so it fits inside the
    # try block of our wrapper template.
    indented_code = "\n".join(
        "    " + line for line in code.splitlines()
    )
    wrapped_code = WRAPPER_TEMPLATE.format(
        student_code=indented_code,
        max_output=settings.SANDBOX_MAX_OUTPUT_CHARS,
        max_memory=settings.SANDBOX_MAX_MEMORY_BYTES,
        timeout=settings.SANDBOX_TIMEOUT_SECONDS,
    )

    # ── Step 3: Write to temp file and execute ───────────────
    # We use a temp file instead of passing code via stdin
    # because it produces cleaner error messages.
    start_time = time.time()

    try:
        # Create a temporary Python file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as tmp_file:
            tmp_file.write(wrapped_code)
            tmp_path = tmp_file.name

        # Run the code in a separate Python process
        # We use asyncio.to_thread to avoid blocking the event loop
        result = await asyncio.wait_for(
            asyncio.to_thread(
                _run_subprocess,
                tmp_path,
            ),
            timeout=settings.SANDBOX_TIMEOUT_SECONDS,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "output": result["output"],
            "error": result["error"],
            "execution_time_ms": elapsed_ms,
        }

    except asyncio.TimeoutError:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "output": "",
            "error": (
                "Your code took too long to run and was stopped. "
                "This usually means you have an infinite loop — "
                "a loop that never ends. Check your while loop "
                "condition or make sure your loop has a way to stop."
            ),
            "execution_time_ms": elapsed_ms,
        }

    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "output": "",
            "error": f"Something went wrong while running your code: {str(e)}",
            "execution_time_ms": elapsed_ms,
        }

    finally:
        # Always clean up the temp file
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def _run_subprocess(file_path: str) -> dict:
    """
    Run a Python file in a subprocess and capture output.
    This function runs in a thread (called via asyncio.to_thread).
    """
    try:
        result = subprocess.run(
            [sys.executable, "-u", file_path],
            capture_output=True,
            text=True,
            timeout=settings.SANDBOX_TIMEOUT_SECONDS + 1,
            # Don't inherit the parent's environment variables
            env={
                "PATH": os.environ.get("PATH", ""),
                "PYTHONPATH": "",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        return {"output": output, "error": error}

    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": (
                "Your code took too long to run and was stopped. "
                "Check for infinite loops!"
            ),
        }
    except Exception as e:
        return {
            "output": "",
            "error": f"Execution error: {str(e)}",
        }


async def run_exercise_tests(
    code: str, tests: list
) -> dict:
    """
    Run student code against a list of test cases.

    Each test case has:
        - input: text to feed via stdin (simulated)
        - expected_output: what print() should produce

    Returns:
        {
            "is_correct": True/False,
            "test_results": [{"passed": True, ...}, ...],
            "output": "last run output",
            "error": "..."
        }
    """
    # ── Safety check on student code BEFORE adding test harness ──
    is_safe, safety_message = check_code_safety(code)
    if not is_safe:
        return {
            "is_correct": False,
            "test_results": [],
            "output": "",
            "error": safety_message,
        }

    if not tests:
        # No tests defined — just run the code
        result = await execute_code(code)
        return {
            "is_correct": True if not result["error"] else False,
            "test_results": [],
            "output": result["output"],
            "error": result["error"],
        }

    test_results = []
    all_passed = True
    last_output = ""
    last_error = ""

    for i, test in enumerate(tests):
        test_input = test.get("input", "")
        expected = test.get("expected_output", "").strip()

        # Build the test code — stdin simulation is added to the
        # wrapper template, not to the student code, so it doesn't
        # trip the safety check.
        result = await _execute_with_stdin(code, test_input)
        actual_output = result["output"].strip()
        last_output = actual_output
        last_error = result["error"]

        passed = actual_output == expected

        if not passed:
            all_passed = False

        test_results.append({
            "test_number": i + 1,
            "passed": passed,
            "input": test_input,
            "expected": expected,
            "actual": actual_output,
            "error": result["error"],
        })

    return {
        "is_correct": all_passed,
        "test_results": test_results,
        "output": last_output,
        "error": last_error,
    }


# ── Wrapper Template for Exercise Tests with stdin ───────────
WRAPPER_TEMPLATE_STDIN = '''
import sys
import io

# Limit recursion to prevent infinite recursion crashes
sys.setrecursionlimit(200)

# Limit memory and CPU usage (Linux/Unix only — no-op on Windows)
try:
    import resource as _resource
    _MEM = {max_memory}
    _resource.setrlimit(_resource.RLIMIT_AS, (_MEM, _MEM))
    _resource.setrlimit(_resource.RLIMIT_CPU, ({timeout}, {timeout}))
except Exception:
    pass

# Simulate stdin for test input
sys.stdin = io.StringIO({stdin_data})

# Capture all print output
_captured_output = io.StringIO()
sys.stdout = _captured_output
sys.stderr = _captured_output

try:
    # ── Student code begins ──
{student_code}
    # ── Student code ends ──
except MemoryError:
    print("MemoryError: Your code used too much memory and was stopped.", file=sys.stderr)
except Exception as _e:
    print(f"{{type(_e).__name__}}: {{_e}}", file=sys.stderr)

# Print captured output
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
_result = _captured_output.getvalue()
if len(_result) > {max_output}:
    _result = _result[:{max_output}] + "\\n... (output truncated — too much text)"
print(_result, end="")
'''


async def _execute_with_stdin(code: str, stdin_input: str = "") -> dict:
    """
    Execute student code with optional stdin input.
    Safety check must be done by the caller before using this.
    """
    if not stdin_input:
        return await execute_code(code)

    indented_code = "\n".join(
        "    " + line for line in code.splitlines()
    )
    wrapped_code = WRAPPER_TEMPLATE_STDIN.format(
        student_code=indented_code,
        stdin_data=repr(stdin_input),
        max_output=settings.SANDBOX_MAX_OUTPUT_CHARS,
        max_memory=settings.SANDBOX_MAX_MEMORY_BYTES,
        timeout=settings.SANDBOX_TIMEOUT_SECONDS,
    )

    start_time = time.time()

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as tmp_file:
            tmp_file.write(wrapped_code)
            tmp_path = tmp_file.name

        result = await asyncio.wait_for(
            asyncio.to_thread(_run_subprocess, tmp_path),
            timeout=settings.SANDBOX_TIMEOUT_SECONDS,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "output": result["output"],
            "error": result["error"],
            "execution_time_ms": elapsed_ms,
        }

    except asyncio.TimeoutError:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "output": "",
            "error": (
                "Your code took too long to run and was stopped. "
                "Check for infinite loops!"
            ),
            "execution_time_ms": elapsed_ms,
        }
    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return {
            "output": "",
            "error": f"Something went wrong while running your code: {str(e)}",
            "execution_time_ms": elapsed_ms,
        }
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
