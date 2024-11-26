# Python Linter

![Python Linter](https://img.shields.io/badge/python-linter-blue)

A modular Python Linter designed to enforce coding standards, detect potential runtime issues, and enhance code quality through static analysis using Python's Abstract Syntax Tree (AST).

---

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Usage](#usage)
- [Installation](#installation)
- [Linting Rules](#linting-rules)
- [Multi-Threading](#multi-threading)
- [Code Examples](#code-examples)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- **Unused Variable Detection**: Identifies variables that are declared but not used.
- **Unreachable Code Detection**: Flags unreachable code segments.
- **Naming Convention Enforcement**: Ensures variables and functions follow Python's snake_case.
- **Duplicate Variable Detection**: Highlights duplicate variable assignments.
- **Division by Zero Checks**: Detects division by zero errors to prevent runtime exceptions.
- **Modular and Extensible**: Easily add new checkers for custom linting rules.
- **Threaded Execution**: Supports multi-threaded linting for faster analysis of large codebases.

---

## Architecture
The Python Linter is designed around modular checkers. Each checker class inherits from a base class `checker_base`, ensuring consistent interfaces and ease of extensibility.

### Key Components
1. **AST Parsing**: Parses Python code into an Abstract Syntax Tree (AST) using the built-in `ast` module.
2. **Checker Classes**:
   - `DivisionByZeroChecker`: Flags division by zero violations.
   - `DuplicateVarChecker`: Detects duplicate variable assignments.
   - `NameConventionChecker`: Enforces naming conventions.
   - `UnreachableCodeChecker`: Identifies unreachable code.
   - `VariableNameChecker`: Detects unused variables.
3. **Thread Pooling**: Utilizes Python’s `concurrent.futures.ThreadPoolExecutor` for concurrent rule checking.
4. **Violation Reporting**: Aggregates all violations into a structured and human-readable report.

---

## Usage

### Running the Linter
Run the linter on a Python file:
```bash
python linter.py <file_to_lint.py>
