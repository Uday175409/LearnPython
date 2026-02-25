# ============================================================
# error_explainer.py — Friendly Error Messages
# ============================================================
# Python's default error messages are written for experienced
# programmers. Beginners find them confusing and scary.
#
# This module translates raw Python errors into plain-English
# explanations that help students understand WHAT went wrong
# and HOW to fix it.
# ============================================================

import re
from typing import Optional


# ── Pattern-based Error Explanations ─────────────────────────
# Each entry is: (regex_pattern, friendly_template)
# We try each pattern against the raw error. The first match
# wins. Templates can use {0}, {1}, etc. for regex groups.

ERROR_PATTERNS = [
    # ── SyntaxError ──────────────────────────────────────────
    (
        r"SyntaxError: invalid syntax",
        "🔴 **Syntax Error** — Python found something it doesn't understand.\n\n"
        "This usually means:\n"
        "• You're missing a colon `:` at the end of an `if`, `for`, `while`, or `def` line\n"
        "• You have mismatched parentheses `()` or brackets `[]`\n"
        "• There's a typo in a keyword like `prnit` instead of `print`\n\n"
        "**Tip:** Look at the line number mentioned in the error and check the line *above* it too."
    ),
    (
        r"SyntaxError: EOL while scanning string literal",
        "🔴 **String Not Closed** — You started a text string with a quote mark "
        "but forgot to close it.\n\n"
        "**Fix:** Make sure every opening quote `\"` or `'` has a matching closing quote.\n\n"
        "Example:\n"
        "```python\n"
        "# ❌ Wrong\n"
        "name = \"Alice\n\n"
        "# ✅ Right\n"
        "name = \"Alice\"\n"
        "```"
    ),
    (
        r"SyntaxError: unexpected EOF while parsing",
        "🔴 **Incomplete Code** — Python reached the end of your code but was "
        "expecting more.\n\n"
        "This usually means:\n"
        "• You're missing a closing parenthesis `)` or bracket `]`\n"
        "• An `if`, `for`, or `def` block is empty (needs at least one line inside)\n\n"
        "**Tip:** If you want an empty block, use `pass` as a placeholder."
    ),
    (
        r"IndentationError: expected an indented block",
        "🔴 **Indentation Missing** — Python expects the lines *inside* an `if`, `for`, "
        "`while`, or `def` to be indented (moved to the right).\n\n"
        "**Fix:** Add 4 spaces at the beginning of the lines inside your block.\n\n"
        "Example:\n"
        "```python\n"
        "# ❌ Wrong\n"
        "if age > 18:\n"
        "print(\"Adult\")\n\n"
        "# ✅ Right\n"
        "if age > 18:\n"
        "    print(\"Adult\")\n"
        "```"
    ),
    (
        r"IndentationError: unexpected indent",
        "🔴 **Extra Indentation** — A line has more spaces at the beginning than "
        "Python expected.\n\n"
        "**Fix:** Make sure the spacing is consistent. Lines at the same level "
        "should have the same number of spaces.\n\n"
        "**Tip:** Use exactly 4 spaces for each level of indentation."
    ),
    (
        r"SyntaxError: invalid character",
        "🔴 **Invalid Character** — Your code contains a character that Python "
        "doesn't recognize. This often happens when:\n\n"
        "• You copied code from a website that used 'fancy quotes' instead of \"straight quotes\"\n"
        "• There's an invisible special character in your code\n\n"
        "**Fix:** Delete the line and retype it manually."
    ),

    # ── NameError ────────────────────────────────────────────
    (
        r"NameError: name '(\w+)' is not defined",
        "🔴 **Name Not Found** — Python doesn't know what `{0}` means.\n\n"
        "This usually means:\n"
        "• You haven't created a variable called `{0}` yet\n"
        "• You misspelled the name (Python is case-sensitive: `Name` ≠ `name`)\n"
        "• You forgot to put quotes around a text string\n\n"
        "**Fix:** Check spelling, or make sure you assigned a value to `{0}` "
        "before using it.\n\n"
        "Example:\n"
        "```python\n"
        "# ❌ This causes the error\n"
        "print(hello)\n\n"
        "# ✅ If hello is text, add quotes\n"
        "print(\"hello\")\n\n"
        "# ✅ If hello is a variable, define it first\n"
        "hello = \"Hi there!\"\n"
        "print(hello)\n"
        "```"
    ),

    # ── TypeError ────────────────────────────────────────────
    (
        r"TypeError: can only concatenate str.*to str",
        "🔴 **Mixing Text and Numbers** — You tried to combine text (a string) "
        "with a number using `+`, but Python doesn't allow that directly.\n\n"
        "**Fix:** Convert the number to text using `str()`.\n\n"
        "Example:\n"
        "```python\n"
        "# ❌ Wrong\n"
        "age = 25\n"
        "print(\"I am \" + age + \" years old\")\n\n"
        "# ✅ Right — convert number to text\n"
        "print(\"I am \" + str(age) + \" years old\")\n\n"
        "# ✅ Even better — use f-string\n"
        "print(f\"I am {age} years old\")\n"
        "```"
    ),
    (
        r"TypeError: unsupported operand type\(s\) for (.+): '(\w+)' and '(\w+)'",
        "🔴 **Wrong Types for `{0}`** — You tried to use `{0}` with a `{1}` and "
        "a `{2}`, but Python doesn't know how to do that.\n\n"
        "**Fix:** Make sure both values are the same type. Use `int()` to convert "
        "to a number or `str()` to convert to text."
    ),
    (
        r"TypeError: '(\w+)' object is not callable",
        "🔴 **Not a Function** — You're trying to call `{0}` like a function "
        "(with parentheses), but it's not a function.\n\n"
        "**Common cause:** You might have a variable with the same name as a "
        "built-in function. For example, if you wrote `print = 5`, then `print()` "
        "stops working."
    ),
    (
        r"TypeError: (.+) takes (\d+) positional argument.* (\d+) .* given",
        "🔴 **Wrong Number of Arguments** — The function `{0}` expects {1} "
        "value(s), but you gave it {2}.\n\n"
        "**Fix:** Check the function definition to see how many values it needs."
    ),

    # ── ValueError ───────────────────────────────────────────
    (
        r"ValueError: invalid literal for int\(\) with base 10: '(.+)'",
        "🔴 **Can't Convert to Number** — You tried to turn `\"{0}\"` into a "
        "whole number using `int()`, but it's not a valid number.\n\n"
        "**Fix:** Make sure the text contains only digits (like `\"42\"`, not `\"hello\"`).\n\n"
        "If the text has a decimal point (like `\"3.14\"`), use `float()` instead of `int()`."
    ),
    (
        r"ValueError: could not convert string to float: '(.+)'",
        "🔴 **Can't Convert to Decimal** — You tried to turn `\"{0}\"` into a "
        "decimal number using `float()`, but it's not a valid number.\n\n"
        "**Fix:** Make sure the text looks like a number (e.g., `\"3.14\"` or `\"42\"`)."
    ),

    # ── IndexError ───────────────────────────────────────────
    (
        r"IndexError: list index out of range",
        "🔴 **List Position Doesn't Exist** — You tried to access a position in "
        "a list that doesn't exist.\n\n"
        "**Remember:** Python counts positions starting from 0!\n"
        "A list with 3 items has positions 0, 1, and 2. There is no position 3.\n\n"
        "Example:\n"
        "```python\n"
        "fruits = [\"apple\", \"banana\", \"cherry\"]\n"
        "#          ^0        ^1         ^2\n\n"
        "print(fruits[0])  # ✅ \"apple\"\n"
        "print(fruits[2])  # ✅ \"cherry\"\n"
        "print(fruits[3])  # ❌ Error! Only 0, 1, 2 exist\n"
        "```\n\n"
        "**Tip:** Use `len(my_list)` to check how many items are in a list."
    ),
    (
        r"IndexError: string index out of range",
        "🔴 **Character Position Doesn't Exist** — You tried to access a character "
        "position in a string that doesn't exist.\n\n"
        "**Remember:** Positions start at 0, and the last position is `len(text) - 1`."
    ),

    # ── KeyError ─────────────────────────────────────────────
    (
        r"KeyError: (.+)",
        "🔴 **Key Not Found** — You tried to look up `{0}` in a dictionary, "
        "but that key doesn't exist.\n\n"
        "**Fix:** Check the spelling of your key, or use `.get()` which returns "
        "`None` instead of crashing.\n\n"
        "Example:\n"
        "```python\n"
        "person = {{\"name\": \"Alice\", \"age\": 25}}\n\n"
        "# ❌ Crashes if key is wrong\n"
        "print(person[\"naem\"])  # Typo!\n\n"
        "# ✅ Safer — returns None if key is missing\n"
        "print(person.get(\"name\"))\n"
        "```"
    ),

    # ── ZeroDivisionError ────────────────────────────────────
    (
        r"ZeroDivisionError",
        "🔴 **Division by Zero** — You tried to divide a number by 0, which is "
        "mathematically impossible.\n\n"
        "**Fix:** Before dividing, check that the number isn't zero.\n\n"
        "```python\n"
        "# ✅ Safe division\n"
        "if divisor != 0:\n"
        "    result = number / divisor\n"
        "else:\n"
        "    print(\"Cannot divide by zero!\")\n"
        "```"
    ),

    # ── AttributeError ──────────────────────────────────────
    (
        r"AttributeError: '(\w+)' object has no attribute '(\w+)'",
        "🔴 **No Such Method/Property** — A `{0}` doesn't have something "
        "called `.{1}`.\n\n"
        "**Fix:** Check the spelling, or look up what methods are available "
        "for `{0}` type objects."
    ),

    # ── RecursionError ───────────────────────────────────────
    (
        r"RecursionError",
        "🔴 **Infinite Loop (Recursion)** — A function is calling itself "
        "over and over without stopping.\n\n"
        "**Fix:** Make sure your function has a clear *base case* — a condition "
        "where it stops calling itself."
    ),

    # ── ModuleNotFoundError ──────────────────────────────────
    (
        r"ModuleNotFoundError: No module named '(\w+)'",
        "🔴 **Module Not Found** — Python can't find a module called `{0}`.\n\n"
        "In this learning environment, only basic modules are available: "
        "math, random, string, datetime, collections, json, re, and statistics."
    ),

    # ── FileNotFoundError ────────────────────────────────────
    (
        r"FileNotFoundError",
        "🔴 **File Not Found** — Your code tried to open a file that doesn't exist.\n\n"
        "In this learning environment, you cannot read or write files. "
        "Focus on using `print()` to show your results!"
    ),
]


def explain_error(raw_error: str) -> str:
    """
    Convert a raw Python error message into a friendly,
    beginner-understandable explanation.

    Args:
        raw_error: The raw error text from Python.

    Returns:
        A friendly explanation string, or the original error
        if no pattern matches.
    """
    if not raw_error:
        return ""

    # Try each pattern until we find a match
    for pattern, template in ERROR_PATTERNS:
        match = re.search(pattern, raw_error)
        if match:
            # Fill in the template with captured groups
            try:
                groups = match.groups()
                explanation = template.format(*groups)
            except (IndexError, KeyError):
                explanation = template
            return explanation

    # ── Fallback: No pattern matched ─────────────────────────
    # Still try to make it slightly friendlier
    return (
        f"🔴 **Error in your code:**\n\n"
        f"```\n{raw_error}\n```\n\n"
        f"**Don't worry!** Errors are a normal part of programming. "
        f"Read the message above carefully — it usually tells you "
        f"which line the problem is on. Try fixing that line and "
        f"running your code again."
    )
