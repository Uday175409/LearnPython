# ============================================================
# api/management/commands/seed.py — Full Course Curriculum
# ============================================================
# Run with:   python manage.py seed
# Clears existing courses/lessons/exercises and recreates them.
#
# 10 lessons, 2-3 exercises each, with rich content blocks,
# tips, common mistakes, hints, solutions, explanations, and
# automated test cases.
# ============================================================

from django.core.management.base import BaseCommand
from api.models import Course, Lesson, Exercise


class Command(BaseCommand):
    help = "Seed the database with the full Python Basics curriculum"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding curriculum...")

        # Clear old data
        Exercise.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # ── Create the course ────────────────────────────────
        course = Course.objects.create(
            title="Python Basics",
            description=(
                "Learn Python from scratch — no experience needed! "
                "This course takes you from zero to writing your own "
                "programs, one small step at a time."
            ),
            order=1,
            icon="🐍",
        )

        # ════════════════════════════════════════════════════
        # LESSON 1 — What is Programming?
        # ════════════════════════════════════════════════════
        L1 = Lesson.objects.create(
            course=course,
            title="What is Programming?",
            subtitle="Understand what programming is and why Python is great for beginners",
            order=1,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Welcome! 🎉\n\n"
                        "Programming is simply **giving instructions to a computer**. "
                        "Imagine you're writing a recipe for a robot in your kitchen. "
                        "The robot can chop vegetables, boil water, and stir soup — but "
                        "**only if you tell it exactly what to do**, step by step.\n\n"
                        "That's what programming is! You write a list of instructions "
                        "(called **code**), and the computer follows them — one line at a time, "
                        "from top to bottom."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Why Python? 🐍\n\n"
                        "There are hundreds of programming languages, but **Python** is "
                        "the best choice for beginners because:\n\n"
                        "1. **It reads like English** — `print(\"Hello\")` literally prints \"Hello\"\n"
                        "2. **No complicated setup** — you'll run code right here in your browser\n"
                        "3. **Huge community** — millions of people use Python, so help is everywhere\n"
                        "4. **Used in real life** — Instagram, Netflix, Google, and NASA all use Python"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## How Code Runs\n\n"
                        "When you press the **Run** button, here's what happens:\n\n"
                        "1. Your code is sent to a computer (a server)\n"
                        "2. The computer reads your code **line by line, top to bottom**\n"
                        "3. It does what each line says\n"
                        "4. Any results are sent back and shown to you\n\n"
                        "Think of it like sending a text message — you type it, press send, "
                        "and the reply comes back."
                    ),
                },
                {
                    "type": "tip",
                    "body": (
                        "You don't need to memorize anything yet. Just read through this lesson "
                        "and tap \"Mark as Complete\" when you're done. The hands-on coding starts "
                        "in the next lesson!"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- Programming means **writing instructions for a computer**\n"
                        "- Python is beginner-friendly because it reads like English\n"
                        "- Code runs **top to bottom**, one line at a time\n"
                        "- You don't need any experience — we'll start from zero!\n\n"
                        "**You're off to a great start!** Let's write some real code in the next lesson. 🚀"
                    ),
                },
            ],
        )

        # ════════════════════════════════════════════════════
        # LESSON 2 — Your First Code (print)
        # ════════════════════════════════════════════════════
        L2 = Lesson.objects.create(
            course=course,
            title="Your First Code",
            subtitle="Learn to display text on the screen using print()",
            order=2,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Use `print()` to display text on the screen\n"
                        "- Understand what **strings** (text) are\n"
                        "- Know the difference between single and double quotes\n"
                        "- Print multiple lines of text"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## The `print()` Function\n\n"
                        "The very first thing most programmers learn is how to make the "
                        "computer **display a message**. In Python, we use `print()`.\n\n"
                        "Think of `print()` as a **megaphone** 📢. Whatever you put inside "
                        "the parentheses, Python will shout it out on the screen."
                    ),
                },
                {
                    "type": "code",
                    "body": 'print("Hello, World!")',
                    "caption": "This displays: Hello, World!",
                },
                {
                    "type": "text",
                    "body": (
                        "Let's break this down:\n\n"
                        "- `print` — this is the **command** (called a \"function\")\n"
                        "- `(` and `)` — parentheses wrap what you want to print\n"
                        "- `\"Hello, World!\"` — the text inside quotes is called a **string**\n\n"
                        "The quotation marks tell Python: *\"this is text, not a command.\"* "
                        "Without them, Python would think `Hello` is a variable name and get confused."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Single vs. Double Quotes\n\n"
                        "Python accepts both single quotes `'...'` and double quotes `\"...\"`. "
                        "These two lines do exactly the same thing:"
                    ),
                },
                {
                    "type": "code",
                    "body": "print('Hello!')\nprint(\"Hello!\")",
                    "caption": "Both output: Hello!",
                },
                {
                    "type": "text",
                    "body": (
                        "## Printing Multiple Lines\n\n"
                        "Each `print()` creates a new line of output:"
                    ),
                },
                {
                    "type": "code",
                    "body": "print(\"Line 1\")\nprint(\"Line 2\")\nprint(\"Line 3\")",
                    "caption": "Each print() starts on a new line",
                },
                {
                    "type": "tip",
                    "body": (
                        "Python is **case-sensitive**. `print()` works, but `Print()` or "
                        "`PRINT()` will cause an error. Always use lowercase `print`."
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": "print(Hello)",
                    "right": 'print("Hello")',
                    "explanation": (
                        "Text must be inside quotes. Without quotes, Python thinks "
                        "`Hello` is a variable name and throws a NameError."
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": 'print "Hello"',
                    "right": 'print("Hello")',
                    "explanation": (
                        "In Python 3, `print` requires parentheses. "
                        "It's `print(\"Hello\")`, not `print \"Hello\"`."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `print()` displays text on the screen\n"
                        "- Text (strings) must be wrapped in quotes: `\"...\"` or `'...'`\n"
                        "- Each `print()` call outputs on a new line\n"
                        "- Python is case-sensitive: use lowercase `print`\n\n"
                        "**Awesome! You just wrote your first Python code!** 🎉"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L2,
            title="Say Hello",
            instructions=(
                "Write a program that prints **exactly** this text:\n\n"
                "```\nHello, World!\n```\n\n"
                "Use the `print()` function."
            ),
            starter_code='# Use print() to display Hello, World!\n',
            hint="Type: print(\"Hello, World!\")",
            solution='print("Hello, World!")',
            explanation=(
                "We use `print()` with the text inside double quotes. "
                "The exact text `Hello, World!` (including the comma, space, "
                "and exclamation mark) is placed inside the quotes."
            ),
            tests=[
                {"input": "", "expected_output": "Hello, World!"},
            ],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L2,
            title="Three Lines",
            instructions=(
                "Write a program that prints these three lines **exactly**:\n\n"
                "```\nI am learning Python\nIt is fun\nLet's go!\n```\n\n"
                "You'll need three separate `print()` calls."
            ),
            starter_code=(
                "# Print three lines:\n"
                "# I am learning Python\n"
                "# It is fun\n"
                "# Let's go!\n"
            ),
            hint="Use one print() for each line. You can use double quotes for the last line since it contains an apostrophe.",
            solution=(
                'print("I am learning Python")\n'
                'print("It is fun")\n'
                'print("Let\'s go!")'
            ),
            explanation=(
                "Each `print()` displays one line. For the third line, "
                "we use double quotes on the outside because the text "
                "contains a single quote (apostrophe) in `Let's`."
            ),
            tests=[
                {"input": "", "expected_output": "I am learning Python\nIt is fun\nLet's go!"},
            ],
            order=2,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L2,
            title="Your Introduction",
            instructions=(
                "Write a program that prints a short self-introduction on two lines:\n\n"
                "```\nMy name is Python Learner\nI am a beginner\n```"
            ),
            starter_code='# Introduce yourself!\n',
            hint="Use two print() calls, one for each line.",
            solution=(
                'print("My name is Python Learner")\n'
                'print("I am a beginner")'
            ),
            explanation=(
                "Two `print()` statements, one per line. The text is inside "
                "double quotes."
            ),
            tests=[
                {"input": "", "expected_output": "My name is Python Learner\nI am a beginner"},
            ],
            order=3,
            difficulty="easy",
        )

        # ════════════════════════════════════════════════════
        # LESSON 3 — Variables
        # ════════════════════════════════════════════════════
        L3 = Lesson.objects.create(
            course=course,
            title="Variables",
            subtitle="Store and reuse information using variables",
            order=3,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Create variables and assign values to them\n"
                        "- Use variables inside `print()`\n"
                        "- Change a variable's value\n"
                        "- Follow variable naming rules"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## What is a Variable?\n\n"
                        "A variable is like a **labeled box** 📦. You put something "
                        "inside the box, and you can use the label to get it back later.\n\n"
                        "For example, if you write:\n"
                    ),
                },
                {
                    "type": "code",
                    "body": "name = \"Alice\"\nprint(name)",
                    "caption": "Output: Alice",
                },
                {
                    "type": "text",
                    "body": (
                        "Here's what happened:\n"
                        "1. `name` is the **label** on the box\n"
                        "2. `\"Alice\"` is what we **put inside** the box\n"
                        "3. `=` means **\"put this value into the variable\"** (NOT \"equals\" like in math!)\n"
                        "4. `print(name)` opens the box and shows what's inside"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Variables with Numbers\n\n"
                        "Variables can store numbers too — and you can do math with them!"
                    ),
                },
                {
                    "type": "code",
                    "body": "age = 25\nprice = 9.99\nprint(age)\nprint(price)",
                    "caption": "Output: 25 then 9.99",
                },
                {
                    "type": "text",
                    "body": (
                        "## Changing a Variable\n\n"
                        "You can change what's in the box at any time:"
                    ),
                },
                {
                    "type": "code",
                    "body": "score = 10\nprint(score)\nscore = 20\nprint(score)",
                    "caption": "Output: 10 then 20",
                },
                {
                    "type": "text",
                    "body": (
                        "## Using f-strings\n\n"
                        "To mix variables with text, use an **f-string** (put `f` before the quotes):"
                    ),
                },
                {
                    "type": "code",
                    "body": "name = \"Alice\"\nage = 25\nprint(f\"My name is {name} and I am {age} years old\")",
                    "caption": "Output: My name is Alice and I am 25 years old",
                },
                {
                    "type": "text",
                    "body": (
                        "The `{name}` and `{age}` parts get **replaced** with the actual values. "
                        "The `f` before the quote is what makes this magic work."
                    ),
                },
                {
                    "type": "tip",
                    "body": (
                        "**Variable naming rules:**\n"
                        "- Must start with a letter or underscore: `name`, `_count`\n"
                        "- Can contain letters, numbers, underscores: `player1`, `high_score`\n"
                        "- Cannot start with a number: `1name` is **invalid**\n"
                        "- Cannot contain spaces: use `my_name` not `my name`\n"
                        "- Case-sensitive: `Name` and `name` are different variables"
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": "print(\"My name is name\")",
                    "right": "name = \"Alice\"\nprint(f\"My name is {name}\")",
                    "explanation": (
                        "If you put a variable name inside quotes without using an f-string, "
                        "Python treats it as plain text. Use f\"...{variable}...\" to insert Variable values."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- Variables store values: `name = \"Alice\"`\n"
                        "- `=` means \"assign\", not \"equals\"\n"
                        "- Use `f\"...{var}...\"` to mix variables with text\n"
                        "- Variable names are case-sensitive and can't start with numbers\n\n"
                        "**You now know what variables are — the foundation of all programming!** 💪"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L3,
            title="Store and Print",
            instructions=(
                "Create a variable called `city` and set it to `\"Paris\"`.\n"
                "Then print it so the output is:\n\n```\nParis\n```"
            ),
            starter_code='# Create a variable called city\n\n# Print it\n',
            hint='Use city = "Paris" then print(city)',
            solution='city = "Paris"\nprint(city)',
            explanation=(
                "We create a variable `city` and assign the string `\"Paris\"` to it. "
                "Then `print(city)` displays the value stored in the variable."
            ),
            tests=[{"input": "", "expected_output": "Paris"}],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L3,
            title="F-String Greeting",
            instructions=(
                "Create two variables:\n"
                "- `name` set to `\"Sam\"`\n"
                "- `age` set to `20`\n\n"
                "Then print this **exactly**:\n\n"
                "```\nHello, Sam! You are 20 years old.\n```\n\n"
                "Use an f-string."
            ),
            starter_code='# Create variables\n\n# Print using f-string\n',
            hint='Use f"Hello, {name}! You are {age} years old."',
            solution=(
                'name = "Sam"\n'
                'age = 20\n'
                'print(f"Hello, {name}! You are {age} years old.")'
            ),
            explanation=(
                "We store the name and age in variables, then use an f-string "
                "with curly braces `{name}` and `{age}` to insert them into the text."
            ),
            tests=[{"input": "", "expected_output": "Hello, Sam! You are 20 years old."}],
            order=2,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L3,
            title="Update a Variable",
            instructions=(
                "Create a variable `score` set to `0`.\n"
                "Print it.\n"
                "Then change `score` to `100`.\n"
                "Print it again.\n\n"
                "Expected output:\n```\n0\n100\n```"
            ),
            starter_code="# Set score to 0 and print it\n\n# Change score to 100 and print it\n",
            hint="Assign score = 0, print, then score = 100, print again.",
            solution="score = 0\nprint(score)\nscore = 100\nprint(score)",
            explanation=(
                "Variables can be reassigned. First we set `score` to 0 and print it. "
                "Then we set `score` to 100 and print it again."
            ),
            tests=[{"input": "", "expected_output": "0\n100"}],
            order=3,
            difficulty="easy",
        )

        # ════════════════════════════════════════════════════
        # LESSON 4 — Data Types
        # ════════════════════════════════════════════════════
        L4 = Lesson.objects.create(
            course=course,
            title="Data Types",
            subtitle="Learn about integers, floats, strings, and booleans",
            order=4,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Name the 4 basic Python data types\n"
                        "- Use `type()` to check what type a value is\n"
                        "- Convert between types using `int()`, `float()`, `str()`\n"
                        "- Do basic math in Python"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## The 4 Basic Types\n\n"
                        "Every piece of data in Python has a **type**. Think of it like this:\n\n"
                        "| Type | What it stores | Example |\n"
                        "|------|---------------|--------|\n"
                        "| `int` | Whole numbers | `42`, `-5`, `0` |\n"
                        "| `float` | Decimal numbers | `3.14`, `-0.5` |\n"
                        "| `str` | Text (strings) | `\"Hello\"`, `'abc'` |\n"
                        "| `bool` | True or False | `True`, `False` |"
                    ),
                },
                {
                    "type": "code",
                    "body": "print(type(42))\nprint(type(3.14))\nprint(type(\"Hello\"))\nprint(type(True))",
                    "caption": "Check the type of any value with type()",
                },
                {
                    "type": "text",
                    "body": (
                        "## Math in Python\n\n"
                        "Python can do math with numbers:\n\n"
                        "| Operator | Meaning | Example | Result |\n"
                        "|----------|---------|---------|--------|\n"
                        "| `+` | Add | `5 + 3` | `8` |\n"
                        "| `-` | Subtract | `10 - 4` | `6` |\n"
                        "| `*` | Multiply | `3 * 7` | `21` |\n"
                        "| `/` | Divide | `10 / 3` | `3.333...` |\n"
                        "| `//` | Floor divide | `10 // 3` | `3` |\n"
                        "| `%` | Remainder | `10 % 3` | `1` |\n"
                        "| `**` | Power | `2 ** 3` | `8` |"
                    ),
                },
                {
                    "type": "code",
                    "body": "a = 10\nb = 3\nprint(a + b)\nprint(a / b)\nprint(a // b)\nprint(a % b)",
                    "caption": "Output: 13, 3.333..., 3, 1",
                },
                {
                    "type": "text",
                    "body": (
                        "## Type Conversion\n\n"
                        "You can convert between types:"
                    ),
                },
                {
                    "type": "code",
                    "body": "# String to integer\nage_text = \"25\"\nage_number = int(age_text)\nprint(age_number + 5)\n\n# Integer to string\ncount = 42\nprint(\"Count: \" + str(count))",
                    "caption": "int() converts to integer, str() converts to string",
                },
                {
                    "type": "mistake",
                    "wrong": "age = \"25\"\nprint(age + 5)",
                    "right": "age = \"25\"\nprint(int(age) + 5)",
                    "explanation": (
                        "You can't add a string and a number. Convert the string to a "
                        "number first with `int()` or `float()`."
                    ),
                },
                {
                    "type": "tip",
                    "body": (
                        "`True` and `False` must be capitalized. `true` (lowercase) is not valid in Python."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `int` = whole numbers, `float` = decimals, `str` = text, `bool` = True/False\n"
                        "- Use `type()` to check a value's type\n"
                        "- Use `int()`, `float()`, `str()` to convert between types\n"
                        "- Python follows standard math operators: `+`, `-`, `*`, `/`\n\n"
                        "**You're building a strong foundation!** 🧱"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L4,
            title="Simple Calculator",
            instructions=(
                "Create two variables `a = 15` and `b = 4`.\n"
                "Print their sum, difference, and product on three lines:\n\n"
                "```\n19\n11\n60\n```"
            ),
            starter_code="a = 15\nb = 4\n# Print sum, difference, product\n",
            hint="Use print(a + b), print(a - b), print(a * b)",
            solution="a = 15\nb = 4\nprint(a + b)\nprint(a - b)\nprint(a * b)",
            explanation=(
                "`a + b` gives 19, `a - b` gives 11, `a * b` gives 60. "
                "Each `print()` outputs one line."
            ),
            tests=[{"input": "", "expected_output": "19\n11\n60"}],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L4,
            title="Type Detective",
            instructions=(
                "Print the **type** of each value, one per line:\n"
                "- `42`\n- `3.14`\n- `\"Hello\"`\n\n"
                "Expected output:\n```\n<class 'int'>\n<class 'float'>\n<class 'str'>\n```"
            ),
            starter_code="# Print the type of 42, 3.14, and \"Hello\"\n",
            hint="Use print(type(42)), etc.",
            solution="print(type(42))\nprint(type(3.14))\nprint(type(\"Hello\"))",
            explanation="The `type()` function returns the data type of any value.",
            tests=[{"input": "", "expected_output": "<class 'int'>\n<class 'float'>\n<class 'str'>"}],
            order=2,
            difficulty="easy",
        )

        # ════════════════════════════════════════════════════
        # LESSON 5 — Getting User Input
        # ════════════════════════════════════════════════════
        L5 = Lesson.objects.create(
            course=course,
            title="Getting User Input",
            subtitle="Learn to ask the user for information using input()",
            order=5,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Use `input()` to ask the user for information\n"
                        "- Store what the user types in a variable\n"
                        "- Convert input to numbers with `int()` and `float()`\n"
                        "- Build interactive programs"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## The `input()` Function\n\n"
                        "So far, our programs have been one-way — we tell the computer what to "
                        "print. But what if we want to **ask the user a question**?\n\n"
                        "That's what `input()` does. It pauses the program, waits for the "
                        "user to type something, and stores their answer."
                    ),
                },
                {
                    "type": "code",
                    "body": "name = input(\"What is your name? \")\nprint(f\"Hello, {name}!\")",
                    "caption": "The program pauses, waits for typing, then continues",
                },
                {
                    "type": "text",
                    "body": (
                        "**Important:** `input()` **always returns text** (a string), "
                        "even if the user types a number! If you type `25`, Python sees "
                        "it as the text `\"25\"`, not the number `25`."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Converting Input to Numbers\n\n"
                        "If you need to do math with user input, convert it first:"
                    ),
                },
                {
                    "type": "code",
                    "body": "age_text = input(\"Enter your age: \")\nage = int(age_text)\nprint(f\"Next year you will be {age + 1}\")",
                    "caption": "int() converts the text to a whole number",
                },
                {
                    "type": "tip",
                    "body": (
                        "You can combine `input()` and `int()` in one line:\n"
                        "`age = int(input(\"Enter your age: \"))`"
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": "age = input(\"Enter age: \")\nprint(age + 1)",
                    "right": "age = int(input(\"Enter age: \"))\nprint(age + 1)",
                    "explanation": (
                        "`input()` always returns a string. You can't add 1 to a string. "
                        "Wrap it in `int()` to convert to a number first."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `input(\"prompt\")` asks the user to type something\n"
                        "- `input()` always returns a **string**\n"
                        "- Use `int()` or `float()` to convert input to a number\n"
                        "- Store input in a variable: `name = input(\"...\")`\n\n"
                        "**Your programs can now talk back and forth with users!** 🗣️"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L5,
            title="Greeting Machine",
            instructions=(
                "Ask the user for their name using `input()`, then print:\n\n"
                "```\nNice to meet you, [name]!\n```\n\n"
                "If the user types `Alex`, the output should be:\n"
                "`Nice to meet you, Alex!`"
            ),
            starter_code="# Ask for the user's name\n\n# Print greeting\n",
            hint='Use name = input("...") and then print(f"Nice to meet you, {name}!")',
            solution=(
                'name = input("Enter your name: ")\n'
                'print(f"Nice to meet you, {name}!")'
            ),
            explanation=(
                "We use `input()` to get the user's name and store it in a variable. "
                "Then we use an f-string to include the name in our greeting."
            ),
            tests=[
                {"input": "Alex", "expected_output": "Nice to meet you, Alex!"},
                {"input": "Maria", "expected_output": "Nice to meet you, Maria!"},
            ],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L5,
            title="Double the Number",
            instructions=(
                "Ask the user for a number, then print **double** that number.\n\n"
                "If the user types `7`, the output should be:\n`14`\n\n"
                "Remember: `input()` returns a string, so you need to convert it!"
            ),
            starter_code="# Ask for a number\n\n# Print double the number\n",
            hint="Use int(input(...)) to get a number, then multiply by 2.",
            solution=(
                'number = int(input("Enter a number: "))\n'
                'print(number * 2)'
            ),
            explanation=(
                "We use `int(input(...))` to get a number from the user. "
                "Then we multiply by 2 and print the result."
            ),
            tests=[
                {"input": "7", "expected_output": "14"},
                {"input": "0", "expected_output": "0"},
                {"input": "15", "expected_output": "30"},
            ],
            order=2,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L5,
            title="Add Two Numbers",
            instructions=(
                "Ask the user for two numbers (on separate input lines), "
                "then print their **sum**.\n\n"
                "If the user types `5` and then `3`, the output should be:\n`8`"
            ),
            starter_code="# Ask for two numbers\n\n# Print their sum\n",
            hint="Use int(input(...)) twice, then print(a + b).",
            solution=(
                'a = int(input("Enter first number: "))\n'
                'b = int(input("Enter second number: "))\n'
                'print(a + b)'
            ),
            explanation=(
                "We read two numbers from the user (converting both to `int`), "
                "then add them and print the result."
            ),
            tests=[
                {"input": "5\n3", "expected_output": "8"},
                {"input": "10\n20", "expected_output": "30"},
            ],
            order=3,
            difficulty="medium",
        )

        # ════════════════════════════════════════════════════
        # LESSON 6 — Making Decisions (if/else)
        # ════════════════════════════════════════════════════
        L6 = Lesson.objects.create(
            course=course,
            title="Making Decisions",
            subtitle="Use if, elif, and else to make your programs smart",
            order=6,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Write `if` statements to make decisions\n"
                        "- Use `elif` and `else` for multiple options\n"
                        "- Understand comparison operators (`==`, `!=`, `>`, `<`)\n"
                        "- Combine conditions with `and`, `or`, `not`"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## The `if` Statement\n\n"
                        "In real life, we make decisions constantly: *\"If it's raining, "
                        "bring an umbrella.\"* Python can make decisions too!\n\n"
                        "The `if` statement runs code **only when a condition is true**."
                    ),
                },
                {
                    "type": "code",
                    "body": "age = 18\n\nif age >= 18:\n    print(\"You can vote!\")",
                    "caption": "The indented line runs ONLY if the condition is True",
                },
                {
                    "type": "text",
                    "body": (
                        "**Key points:**\n"
                        "- The condition `age >= 18` is checked\n"
                        "- If it's `True`, the indented code runs\n"
                        "- If it's `False`, the indented code is **skipped**\n"
                        "- The colon `:` after the condition is **required**\n"
                        "- The code inside must be **indented** (4 spaces)"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## `if` / `else`\n\n"
                        "What if you want to do something different when the condition is false?"
                    ),
                },
                {
                    "type": "code",
                    "body": "temperature = 35\n\nif temperature > 30:\n    print(\"It's hot! 🥵\")\nelse:\n    print(\"It's nice outside 😊\")",
                    "caption": "One of the two blocks ALWAYS runs",
                },
                {
                    "type": "text",
                    "body": (
                        "## `if` / `elif` / `else`\n\n"
                        "For more than two options, use `elif` (short for \"else if\"):"
                    ),
                },
                {
                    "type": "code",
                    "body": "score = 75\n\nif score >= 90:\n    print(\"Grade: A\")\nelif score >= 80:\n    print(\"Grade: B\")\nelif score >= 70:\n    print(\"Grade: C\")\nelse:\n    print(\"Grade: F\")",
                    "caption": "Python checks conditions top-to-bottom",
                },
                {
                    "type": "text",
                    "body": (
                        "## Comparison Operators\n\n"
                        "| Operator | Meaning | Example |\n"
                        "|----------|---------|--------|\n"
                        "| `==` | Equals | `x == 5` |\n"
                        "| `!=` | Not equals | `x != 5` |\n"
                        "| `>` | Greater than | `x > 5` |\n"
                        "| `<` | Less than | `x < 5` |\n"
                        "| `>=` | Greater or equal | `x >= 5` |\n"
                        "| `<=` | Less or equal | `x <= 5` |\n\n"
                        "**Warning:** `=` is assignment. `==` is comparison. Don't mix them up!"
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": "if age = 18:\n    print(\"18!\")",
                    "right": "if age == 18:\n    print(\"18!\")",
                    "explanation": "Use `==` (double equals) to compare. Single `=` is for assigning values.",
                },
                {
                    "type": "mistake",
                    "wrong": "if age >= 18\n    print(\"Adult\")",
                    "right": "if age >= 18:\n    print(\"Adult\")",
                    "explanation": "Don't forget the colon `:` after the condition!",
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `if` runs code only when a condition is True\n"
                        "- `else` runs when the condition is False\n"
                        "- `elif` adds more conditions in between\n"
                        "- Always end conditions with a colon `:` and indent the body\n"
                        "- Use `==` to compare, not `=`\n\n"
                        "**Your programs can now think and make choices!** 🧠"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L6,
            title="Even or Odd",
            instructions=(
                "Ask the user for a number. Print `Even` if the number is even, "
                "or `Odd` if it's odd.\n\n"
                "Input: `4` → Output: `Even`\n"
                "Input: `7` → Output: `Odd`\n\n"
                "**Hint:** A number is even if `number % 2 == 0`"
            ),
            starter_code="number = int(input(\"Enter a number: \"))\n# Check if even or odd\n",
            hint="Use if number % 2 == 0 to check if even.",
            solution=(
                'number = int(input("Enter a number: "))\n'
                'if number % 2 == 0:\n'
                '    print("Even")\n'
                'else:\n'
                '    print("Odd")'
            ),
            explanation=(
                "The modulo operator `%` gives the remainder of division. "
                "If dividing by 2 has no remainder (0), the number is even."
            ),
            tests=[
                {"input": "4", "expected_output": "Even"},
                {"input": "7", "expected_output": "Odd"},
                {"input": "0", "expected_output": "Even"},
            ],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L6,
            title="Grade Calculator",
            instructions=(
                "Ask the user for a score (0-100). Print the grade:\n\n"
                "- 90 and above: `A`\n"
                "- 80-89: `B`\n"
                "- 70-79: `C`\n"
                "- Below 70: `F`\n\n"
                "Input: `85` → Output: `B`"
            ),
            starter_code="score = int(input(\"Enter your score: \"))\n# Print the grade\n",
            hint="Use if/elif/else chain starting from the highest grade.",
            solution=(
                'score = int(input("Enter your score: "))\n'
                'if score >= 90:\n'
                '    print("A")\n'
                'elif score >= 80:\n'
                '    print("B")\n'
                'elif score >= 70:\n'
                '    print("C")\n'
                'else:\n'
                '    print("F")'
            ),
            explanation=(
                "We check from highest to lowest. If score >= 90, it's an A. "
                "If that's false but >= 80, it's B. And so on."
            ),
            tests=[
                {"input": "95", "expected_output": "A"},
                {"input": "85", "expected_output": "B"},
                {"input": "75", "expected_output": "C"},
                {"input": "60", "expected_output": "F"},
            ],
            order=2,
            difficulty="medium",
        )

        # ════════════════════════════════════════════════════
        # LESSON 7 — Loops
        # ════════════════════════════════════════════════════
        L7 = Lesson.objects.create(
            course=course,
            title="Loops",
            subtitle="Repeat actions with for and while loops",
            order=7,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Use `for` loops to repeat code a specific number of times\n"
                        "- Use `while` loops to repeat code until a condition is met\n"
                        "- Use `range()` to generate numbers\n"
                        "- Avoid infinite loops"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Why Loops?\n\n"
                        "Imagine you want to print \"Hello\" 5 times. Without a loop:\n\n"
                        "```python\nprint(\"Hello\")\nprint(\"Hello\")\nprint(\"Hello\")\nprint(\"Hello\")\nprint(\"Hello\")\n```\n\n"
                        "That's tedious! A loop does it in 2 lines."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## The `for` Loop\n\n"
                        "A `for` loop repeats code a **specific number of times**. "
                        "Think of it as going through a list of items:"
                    ),
                },
                {
                    "type": "code",
                    "body": "for i in range(5):\n    print(\"Hello\")",
                    "caption": "Prints 'Hello' five times",
                },
                {
                    "type": "text",
                    "body": (
                        "`range(5)` generates the numbers 0, 1, 2, 3, 4 (five numbers). "
                        "The loop runs once for each number.\n\n"
                        "You can also use the loop variable `i`:"
                    ),
                },
                {
                    "type": "code",
                    "body": "for i in range(1, 6):\n    print(f\"Step {i}\")",
                    "caption": "Output: Step 1, Step 2, ... Step 5",
                },
                {
                    "type": "text",
                    "body": (
                        "## The `while` Loop\n\n"
                        "A `while` loop keeps going **as long as a condition is True**:"
                    ),
                },
                {
                    "type": "code",
                    "body": "count = 1\nwhile count <= 3:\n    print(f\"Count: {count}\")\n    count = count + 1",
                    "caption": "Output: Count: 1, Count: 2, Count: 3",
                },
                {
                    "type": "tip",
                    "body": (
                        "Always make sure your `while` loop will eventually stop! "
                        "If the condition is always True, you get an **infinite loop** "
                        "and the program runs forever."
                    ),
                },
                {
                    "type": "mistake",
                    "wrong": "count = 1\nwhile count <= 5:\n    print(count)\n    # Forgot count = count + 1",
                    "right": "count = 1\nwhile count <= 5:\n    print(count)\n    count = count + 1",
                    "explanation": (
                        "Without incrementing `count`, the condition `count <= 5` is "
                        "always True and the loop never stops."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `for i in range(n):` repeats code `n` times\n"
                        "- `while condition:` repeats as long as condition is True\n"
                        "- `range(start, stop)` generates numbers from start to stop-1\n"
                        "- Always make sure while loops can stop!\n\n"
                        "**Loops are one of the most powerful tools in programming!** ⚡"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L7,
            title="Count to Five",
            instructions=(
                "Use a `for` loop with `range()` to print the numbers 1 through 5, "
                "each on a new line:\n\n```\n1\n2\n3\n4\n5\n```"
            ),
            starter_code="# Use a for loop to count from 1 to 5\n",
            hint="Use for i in range(1, 6): and print(i)",
            solution="for i in range(1, 6):\n    print(i)",
            explanation=(
                "`range(1, 6)` generates 1, 2, 3, 4, 5. "
                "The loop variable `i` takes each value and we print it."
            ),
            tests=[{"input": "", "expected_output": "1\n2\n3\n4\n5"}],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L7,
            title="Sum of Numbers",
            instructions=(
                "Ask the user for a number `n`. Then calculate and print "
                "the **sum of all numbers from 1 to n**.\n\n"
                "Input: `5` → Output: `15` (because 1+2+3+4+5 = 15)\n"
                "Input: `3` → Output: `6`"
            ),
            starter_code="n = int(input(\"Enter a number: \"))\ntotal = 0\n# Use a loop to add up 1 to n\n\nprint(total)",
            hint="Use a for loop with range(1, n+1) and add each number to total.",
            solution=(
                'n = int(input("Enter a number: "))\n'
                'total = 0\n'
                'for i in range(1, n + 1):\n'
                '    total = total + i\n'
                'print(total)'
            ),
            explanation=(
                "We start with `total = 0`, then loop through 1 to n. "
                "Each iteration, we add the current number `i` to `total`."
            ),
            tests=[
                {"input": "5", "expected_output": "15"},
                {"input": "3", "expected_output": "6"},
                {"input": "1", "expected_output": "1"},
            ],
            order=2,
            difficulty="medium",
        )

        Exercise.objects.create(
            lesson=L7,
            title="Multiplication Table",
            instructions=(
                "Ask the user for a number and print its multiplication table "
                "from 1 to 5.\n\n"
                "If the user types `3`, print:\n```\n3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15\n```"
            ),
            starter_code='n = int(input("Enter a number: "))\n# Print multiplication table\n',
            hint='Use a for loop and print(f"{n} x {i} = {n * i}")',
            solution=(
                'n = int(input("Enter a number: "))\n'
                'for i in range(1, 6):\n'
                '    print(f"{n} x {i} = {n * i}")'
            ),
            explanation=(
                "We loop i from 1 to 5. For each, we print the number, the multiplier, "
                "and the product using an f-string."
            ),
            tests=[
                {"input": "3", "expected_output": "3 x 1 = 3\n3 x 2 = 6\n3 x 3 = 9\n3 x 4 = 12\n3 x 5 = 15"},
                {"input": "5", "expected_output": "5 x 1 = 5\n5 x 2 = 10\n5 x 3 = 15\n5 x 4 = 20\n5 x 5 = 25"},
            ],
            order=3,
            difficulty="medium",
        )

        # ════════════════════════════════════════════════════
        # LESSON 8 — Lists
        # ════════════════════════════════════════════════════
        L8 = Lesson.objects.create(
            course=course,
            title="Lists",
            subtitle="Store multiple items in one place",
            order=8,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Create a list and access items by position\n"
                        "- Add and remove items\n"
                        "- Loop through a list\n"
                        "- Use `len()` to find the number of items"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## What is a List?\n\n"
                        "A list is like a **shopping list** 🛒 — it holds multiple items "
                        "in order. In Python, you create a list with square brackets `[]`:"
                    ),
                },
                {
                    "type": "code",
                    "body": "fruits = [\"apple\", \"banana\", \"cherry\"]\nprint(fruits)",
                    "caption": "A list of three strings",
                },
                {
                    "type": "text",
                    "body": (
                        "## Accessing Items (Indexing)\n\n"
                        "Each item has a position number called an **index**. "
                        "**Important: Python starts counting from 0!**\n\n"
                        "```\n[\"apple\", \"banana\", \"cherry\"]\n   0         1         2\n```"
                    ),
                },
                {
                    "type": "code",
                    "body": "fruits = [\"apple\", \"banana\", \"cherry\"]\nprint(fruits[0])\nprint(fruits[1])\nprint(fruits[2])",
                    "caption": "Output: apple, banana, cherry",
                },
                {
                    "type": "text",
                    "body": (
                        "## Adding and Removing Items\n\n"
                        "- `list.append(item)` — adds to the **end**\n"
                        "- `list.remove(item)` — removes the **first match**\n"
                        "- `len(list)` — tells you how many items"
                    ),
                },
                {
                    "type": "code",
                    "body": "colors = [\"red\", \"blue\"]\ncolors.append(\"green\")\nprint(colors)\nprint(len(colors))",
                    "caption": "Output: ['red', 'blue', 'green'] and 3",
                },
                {
                    "type": "text",
                    "body": "## Looping Through a List\n\nYou can use a `for` loop to visit each item:",
                },
                {
                    "type": "code",
                    "body": "animals = [\"cat\", \"dog\", \"fish\"]\nfor animal in animals:\n    print(f\"I have a {animal}\")",
                    "caption": "Prints one line per animal",
                },
                {
                    "type": "mistake",
                    "wrong": "fruits = [\"apple\", \"banana\"]\nprint(fruits[2])",
                    "right": "fruits = [\"apple\", \"banana\"]\nprint(fruits[1])",
                    "explanation": (
                        "A list with 2 items has indexes 0 and 1. "
                        "Index 2 doesn't exist — you'll get an IndexError."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- Lists store multiple items: `[item1, item2, item3]`\n"
                        "- Index starts at 0: `my_list[0]` is the first item\n"
                        "- `.append()` adds, `.remove()` removes, `len()` counts\n"
                        "- `for item in my_list:` loops through each item\n\n"
                        "**Lists are incredibly useful — you'll use them everywhere!** 📋"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L8,
            title="Fruit Basket",
            instructions=(
                "Create a list called `fruits` with: `\"apple\"`, `\"banana\"`, `\"mango\"`.\n"
                "Then print each fruit on a new line using a loop:\n\n"
                "```\napple\nbanana\nmango\n```"
            ),
            starter_code='# Create the fruits list\n\n# Loop and print each fruit\n',
            hint="Create the list with [...], then use for fruit in fruits: print(fruit)",
            solution=(
                'fruits = ["apple", "banana", "mango"]\n'
                'for fruit in fruits:\n'
                '    print(fruit)'
            ),
            explanation="We create a list with 3 items, then loop through and print each one.",
            tests=[{"input": "", "expected_output": "apple\nbanana\nmango"}],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L8,
            title="List Length",
            instructions=(
                "Ask the user for 3 names (3 separate inputs). "
                "Store them in a list, then print the **number of names** in the list.\n\n"
                "Input: `Alice`, `Bob`, `Charlie` → Output: `3`"
            ),
            starter_code="names = []\n# Ask for 3 names and add them to the list\n\n# Print the length\n",
            hint="Use names.append(input(...)) three times, then print(len(names)).",
            solution=(
                'names = []\n'
                'names.append(input("Name 1: "))\n'
                'names.append(input("Name 2: "))\n'
                'names.append(input("Name 3: "))\n'
                'print(len(names))'
            ),
            explanation=(
                "We start with an empty list, append three names from the user, "
                "then use `len()` to count the items."
            ),
            tests=[
                {"input": "Alice\nBob\nCharlie", "expected_output": "3"},
            ],
            order=2,
            difficulty="medium",
        )

        Exercise.objects.create(
            lesson=L8,
            title="Find the Maximum",
            instructions=(
                "Given the list `numbers = [4, 9, 2, 7, 1]`, find and print "
                "the **largest** number.\n\n"
                "Expected output: `9`\n\n"
                "Hint: Python has a built-in `max()` function!"
            ),
            starter_code="numbers = [4, 9, 2, 7, 1]\n# Print the largest number\n",
            hint="Use max(numbers) to find the biggest value.",
            solution="numbers = [4, 9, 2, 7, 1]\nprint(max(numbers))",
            explanation="`max()` returns the largest value in a list.",
            tests=[{"input": "", "expected_output": "9"}],
            order=3,
            difficulty="easy",
        )

        # ════════════════════════════════════════════════════
        # LESSON 9 — Functions
        # ════════════════════════════════════════════════════
        L9 = Lesson.objects.create(
            course=course,
            title="Functions",
            subtitle="Create reusable blocks of code",
            order=9,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## Learning Goals 🎯\n\n"
                        "By the end of this lesson, you will be able to:\n"
                        "- Define your own functions using `def`\n"
                        "- Pass information to functions (parameters)\n"
                        "- Get results back from functions (return values)\n"
                        "- Understand why functions make code better"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## What is a Function?\n\n"
                        "A function is like a **recipe** 🧑‍🍳. You write it once, "
                        "and then you can use it over and over.\n\n"
                        "You've already used built-in functions: `print()`, `input()`, "
                        "`int()`, `len()`. Now you'll learn to **create your own**."
                    ),
                },
                {
                    "type": "code",
                    "body": "def greet(name):\n    print(f\"Hello, {name}!\")\n\ngreet(\"Alice\")\ngreet(\"Bob\")",
                    "caption": "Output: Hello, Alice! then Hello, Bob!",
                },
                {
                    "type": "text",
                    "body": (
                        "Let's break this down:\n"
                        "- `def` is the keyword to **define** a function\n"
                        "- `greet` is the name we give our function\n"
                        "- `(name)` is a **parameter** — a placeholder for information\n"
                        "- The indented code is the **body** — what the function does\n"
                        "- `greet(\"Alice\")` **calls** the function, passing in `\"Alice\"`"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Return Values\n\n"
                        "Functions can also **send a result back** using `return`:"
                    ),
                },
                {
                    "type": "code",
                    "body": "def add(a, b):\n    return a + b\n\nresult = add(3, 5)\nprint(result)",
                    "caption": "Output: 8",
                },
                {
                    "type": "text",
                    "body": (
                        "`return` sends the value back to where the function was called. "
                        "You can store it in a variable or use it directly."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Functions with Multiple Parameters\n\n"
                        "Functions can take any number of parameters:"
                    ),
                },
                {
                    "type": "code",
                    "body": "def introduce(name, age, hobby):\n    print(f\"{name} is {age} and likes {hobby}\")\n\nintroduce(\"Sam\", 20, \"painting\")",
                    "caption": "Output: Sam is 20 and likes painting",
                },
                {
                    "type": "mistake",
                    "wrong": "def greet(name):\nprint(f\"Hello, {name}!\")",
                    "right": "def greet(name):\n    print(f\"Hello, {name}!\")",
                    "explanation": "The function body must be indented (4 spaces).",
                },
                {
                    "type": "tip",
                    "body": (
                        "A function must be **defined before it's called**. If you call "
                        "`greet(\"Alice\")` before `def greet(name):`, Python will crash."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 📝 Summary\n\n"
                        "- `def function_name(params):` creates a function\n"
                        "- `return value` sends a result back\n"
                        "- Functions help you avoid repeating code\n"
                        "- Define first, then call\n\n"
                        "**Functions are like superpowers for your code!** 🦸"
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L9,
            title="Square Function",
            instructions=(
                "Write a function called `square` that takes a number and "
                "**returns** that number squared (multiplied by itself).\n\n"
                "Then read a number from input and print the result of calling `square()`.\n\n"
                "Input: `4` → Output: `16`\n"
                "Input: `7` → Output: `49`"
            ),
            starter_code=(
                "def square(n):\n"
                "    # Return n squared\n"
                "    pass\n\n"
                "number = int(input(\"Enter a number: \"))\n"
                "print(square(number))"
            ),
            hint="Replace pass with: return n * n",
            solution=(
                'def square(n):\n'
                '    return n * n\n\n'
                'number = int(input("Enter a number: "))\n'
                'print(square(number))'
            ),
            explanation=(
                "The function takes one parameter `n` and returns `n * n`. "
                "We call it with the user's input and print the result."
            ),
            tests=[
                {"input": "4", "expected_output": "16"},
                {"input": "7", "expected_output": "49"},
                {"input": "0", "expected_output": "0"},
            ],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L9,
            title="Max of Three",
            instructions=(
                "Write a function called `max_of_three` that takes three numbers "
                "and **returns** the largest one.\n\n"
                "Read three numbers from input and print the result.\n\n"
                "Input: `3`, `9`, `5` → Output: `9`\n\n"
                "**Don't use Python's built-in `max()` function.** Use `if/elif/else`."
            ),
            starter_code=(
                "def max_of_three(a, b, c):\n"
                "    # Return the largest of a, b, c\n"
                "    pass\n\n"
                "x = int(input())\ny = int(input())\nz = int(input())\n"
                "print(max_of_three(x, y, z))"
            ),
            hint="Compare a >= b and a >= c for the first condition, then check b.",
            solution=(
                'def max_of_three(a, b, c):\n'
                '    if a >= b and a >= c:\n'
                '        return a\n'
                '    elif b >= a and b >= c:\n'
                '        return b\n'
                '    else:\n'
                '        return c\n\n'
                'x = int(input())\ny = int(input())\nz = int(input())\n'
                'print(max_of_three(x, y, z))'
            ),
            explanation=(
                "We compare each number against the other two. The one that is "
                ">= both others is the largest."
            ),
            tests=[
                {"input": "3\n9\n5", "expected_output": "9"},
                {"input": "10\n4\n7", "expected_output": "10"},
                {"input": "1\n1\n1", "expected_output": "1"},
            ],
            order=2,
            difficulty="medium",
        )

        # ════════════════════════════════════════════════════
        # LESSON 10 — Mini Project
        # ════════════════════════════════════════════════════
        L10 = Lesson.objects.create(
            course=course,
            title="Mini Project: Number Guessing Game",
            subtitle="Put everything together in a fun project!",
            order=10,
            content_blocks=[
                {
                    "type": "text",
                    "body": (
                        "## 🎯 Project Goal\n\n"
                        "You'll build a **Number Guessing Game** that:\n"
                        "1. Picks a random secret number\n"
                        "2. Asks the player to guess\n"
                        "3. Tells them if the guess is too high, too low, or correct\n"
                        "4. Counts how many tries it took\n\n"
                        "This project uses **everything you've learned**: variables, "
                        "input, if/else, loops, and functions!"
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## Step 1: Pick a Random Number\n\n"
                        "Python's `random` module can generate random numbers:"
                    ),
                },
                {
                    "type": "code",
                    "body": "import random\n\nsecret = random.randint(1, 20)\nprint(f\"(Debug) Secret number is: {secret}\")",
                    "caption": "random.randint(1, 20) picks a number from 1 to 20",
                },
                {
                    "type": "text",
                    "body": (
                        "## Step 2: Get User Input in a Loop\n\n"
                        "We need a `while` loop that keeps asking until the guess is correct:"
                    ),
                },
                {
                    "type": "code",
                    "body": "guess = 0\nattempts = 0\n\nwhile guess != secret:\n    guess = int(input(\"Your guess: \"))\n    attempts = attempts + 1\n    \n    if guess < secret:\n        print(\"Too low!\")\n    elif guess > secret:\n        print(\"Too high!\")\n    else:\n        print(f\"Correct! You got it in {attempts} tries!\")",
                    "caption": "The loop stops when guess equals secret",
                },
                {
                    "type": "text",
                    "body": (
                        "## Step 3: Make it a Function\n\n"
                        "Let's wrap everything in a clean function:"
                    ),
                },
                {
                    "type": "code",
                    "body": (
                        "import random\n\n"
                        "def play_game():\n"
                        "    secret = random.randint(1, 20)\n"
                        "    attempts = 0\n"
                        "    print(\"I'm thinking of a number between 1 and 20.\")\n\n"
                        "    while True:\n"
                        "        guess = int(input(\"Your guess: \"))\n"
                        "        attempts = attempts + 1\n\n"
                        "        if guess < secret:\n"
                        "            print(\"Too low! Try again.\")\n"
                        "        elif guess > secret:\n"
                        "            print(\"Too high! Try again.\")\n"
                        "        else:\n"
                        "            print(f\"🎉 Correct! You guessed it in {attempts} tries!\")\n"
                        "            return\n\n"
                        "play_game()"
                    ),
                    "caption": "The complete Number Guessing Game!",
                },
                {
                    "type": "text",
                    "body": (
                        "## Line-by-Line Explanation\n\n"
                        "- **`import random`** — loads the random number module\n"
                        "- **`def play_game():`** — wraps everything in a function\n"
                        "- **`random.randint(1, 20)`** — picks a random number 1-20\n"
                        "- **`attempts = 0`** — counter for guesses (variable)\n"
                        "- **`while True:`** — infinite loop (we `return` to break out)\n"
                        "- **`int(input(...))`** — get user input converted to number\n"
                        "- **`if/elif/else`** — compare guess to secret, give feedback\n"
                        "- **`return`** — exits the function when they guess correctly\n"
                        "- **`play_game()`** — calls the function to start"
                    ),
                },
                {
                    "type": "tip",
                    "body": (
                        "For the exercises below, the game won't use `random` since "
                        "we need to test with predictable inputs. You'll hardcode the secret number."
                    ),
                },
                {
                    "type": "text",
                    "body": (
                        "## 🎓 Course Complete!\n\n"
                        "Congratulations! You've learned:\n"
                        "- ✅ `print()` to display text\n"
                        "- ✅ Variables to store information\n"
                        "- ✅ Data types: int, float, str, bool\n"
                        "- ✅ `input()` to get user input\n"
                        "- ✅ `if/elif/else` to make decisions\n"
                        "- ✅ `for` and `while` loops to repeat code\n"
                        "- ✅ Lists to store collections\n"
                        "- ✅ Functions to create reusable code\n\n"
                        "**You're a programmer now!** 🎉🐍\n\n"
                        "Keep practicing in the **Playground** — try building a calculator, "
                        "a quiz game, or a to-do list! The best way to learn is by doing."
                    ),
                },
            ],
        )

        Exercise.objects.create(
            lesson=L10,
            title="Simple Guessing Game",
            instructions=(
                "The secret number is **7**.\n\n"
                "Ask the user for a guess. If the guess equals 7, print `Correct!`. "
                "If the guess is less than 7, print `Too low!`. "
                "If the guess is greater than 7, print `Too high!`.\n\n"
                "(Just one guess — no loop needed)"
            ),
            starter_code=(
                "secret = 7\n"
                "guess = int(input(\"Your guess: \"))\n"
                "# Check if correct, too low, or too high\n"
            ),
            hint="Use if guess == secret, elif guess < secret, else.",
            solution=(
                'secret = 7\n'
                'guess = int(input("Your guess: "))\n'
                'if guess == secret:\n'
                '    print("Correct!")\n'
                'elif guess < secret:\n'
                '    print("Too low!")\n'
                'else:\n'
                '    print("Too high!")'
            ),
            explanation=(
                "We compare the guess to the secret number using if/elif/else. "
                "Each branch prints the appropriate feedback."
            ),
            tests=[
                {"input": "7", "expected_output": "Correct!"},
                {"input": "3", "expected_output": "Too low!"},
                {"input": "10", "expected_output": "Too high!"},
            ],
            order=1,
            difficulty="easy",
        )

        Exercise.objects.create(
            lesson=L10,
            title="Average Calculator",
            instructions=(
                "Ask the user for 3 numbers (3 separate inputs). "
                "Calculate and print the **average** (sum divided by count).\n\n"
                "Use a `float` result. For example:\n"
                "Input: `10`, `20`, `30` → Output: `20.0`\n"
                "Input: `5`, `8`, `2` → Output: `5.0`"
            ),
            starter_code=(
                "# Ask for 3 numbers\n\n"
                "# Calculate and print the average\n"
            ),
            hint="Add all three numbers together and divide by 3. Use float division /.",
            solution=(
                'a = int(input())\n'
                'b = int(input())\n'
                'c = int(input())\n'
                'average = (a + b + c) / 3\n'
                'print(average)'
            ),
            explanation=(
                "We read 3 numbers, add them, and divide by 3. "
                "The `/` operator gives a float result."
            ),
            tests=[
                {"input": "10\n20\n30", "expected_output": "20.0"},
                {"input": "5\n8\n2", "expected_output": "5.0"},
            ],
            order=2,
            difficulty="medium",
        )

        Exercise.objects.create(
            lesson=L10,
            title="FizzBuzz (Classic!)",
            instructions=(
                "Print numbers from 1 to 20, but:\n"
                "- If the number is divisible by 3, print `Fizz`\n"
                "- If divisible by 5, print `Buzz`\n"
                "- If divisible by **both** 3 and 5, print `FizzBuzz`\n"
                "- Otherwise, print the number\n\n"
                "First few lines:\n```\n1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n16\n17\nFizz\n19\nBuzz\n```"
            ),
            starter_code=(
                "# Loop 1 to 20 and print Fizz, Buzz, or FizzBuzz\n"
                "for i in range(1, 21):\n"
                "    pass  # Replace this\n"
            ),
            hint="Check divisible by both first (i % 3 == 0 and i % 5 == 0), then by 3, then by 5, then else.",
            solution=(
                'for i in range(1, 21):\n'
                '    if i % 3 == 0 and i % 5 == 0:\n'
                '        print("FizzBuzz")\n'
                '    elif i % 3 == 0:\n'
                '        print("Fizz")\n'
                '    elif i % 5 == 0:\n'
                '        print("Buzz")\n'
                '    else:\n'
                '        print(i)'
            ),
            explanation=(
                "We check the 'both' condition first (divisible by 3 AND 5), "
                "then divisible by 3 only, then 5 only, then default to the number. "
                "Order matters — if we check 3 first, we'd never reach the 'both' case."
            ),
            tests=[
                {"input": "", "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz\n16\n17\nFizz\n19\nBuzz"},
            ],
            order=3,
            difficulty="challenge",
        )

        # ── Print summary ────────────────────────────────────
        lesson_count = Lesson.objects.count()
        exercise_count = Exercise.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Done! Created 1 course, {lesson_count} lessons, "
                f"{exercise_count} exercises."
            )
        )
