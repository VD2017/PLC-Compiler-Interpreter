# Python Linter

![Python Linter](https://img.shields.io/badge/python-linter-blue)

A modular Python Linter designed to enforce coding standards, detect potential runtime issues, and enhance code quality through static analysis using Python's Abstract Syntax Tree (AST).

---

## Table of Contents
- [Features](#features)
- [How to Run](#how-to-run)
- [Architecture](#architecture)
- [Design](#design)
- [Linting Rules](#linting-rules)
- [Multi-Threading](#multi-threading)


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
## How To Run
### From Main Linter Program:
1. Open up terminal and go to directory of project files.
2. Run `python Linter.py <python_file_here>`
3. Result will be non-multi-threaded and multi-threaded execution.

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

## Design

### AST Tree
The Python Linter leverages Python's native `ast` module to parse the source code into an Abstract Syntax Tree (AST). This approach allows:
- **Efficient Static Analysis**: Analyze code without executing it, ensuring safety and performance.
- **Extensibility**: The modular AST traversal supports adding custom rules easily.

### Methods
#### Self-Contained Linters
- Each linting rule is encapsulated in its own class.
- **Standardized Interfaces**:
  - Each linter extends the base class `checker_base`.
  - Violations are stored in a standardized `violations` set.
- **Independence**:
  - Each linter operates independently, enabling easier maintenance and extension.

#### Thread-Safe and Non-Thread-Safe Checks
- Demonstration purposes
- **Non-Threaded Execution**: Runs checkers sequentially.
- **Threaded Execution**: Executes multiple checkers concurrently to optimize performance.

### Consolidation
- **Centralized Main Linter**: Coordinates initialization and execution of all checkers.
- **Unified Violation Report**: Aggregates violations from all checkers into a centralized dictionary.
- **Queue System**: Uses a thread-safe queue to collect and manage violations in multi-threaded mode.

---

## Linting Rules
The Python Linter enforces the following coding standards:

### 1. Division by Zero
Detects divisions where the divisor is zero, preventing runtime errors.
- **Example Violation**:
    ```python
    result = a / 0  # Detected
    ```

### 2. Duplicate Variables
Flags variables assigned identical values.
- **Example Violation**:
    ```python
    x = 10
    y = x
    z = x  # Detected as a duplicate
    ```

### 3. Naming Conventions
Enforces Python's recommended `snake_case` for functions and variables.
- **Example Violation**:
    ```python
    def ExampleFunction():  # Detected
        pass
    ```

### 4. Unreachable Code
Identifies code that will never execute after an early exit like `return`, `break`, or `continue`.
- **Example Violation**:
    ```python
    def example():
        return
        print("This will not run")  # Detected
    ```

### 5. Unused Variables
Flags variables that are declared but never used.
- **Example Violation**:
    ```python
    x = 10  # Detected as unused
    ```

---

## Multi-Threading
The linter supports both non-threaded and multi-threaded execution modes.

### Implementation
1. **Thread Pool Execution**:
   - Python’s `concurrent.futures.ThreadPoolExecutor` is used for thread management.
   - Each checker runs in its own thread, allowing simultaneous execution.

2. **Event-Based Synchronization**:
   - Threads use event flags for communication, ensuring thread-safe operation and synchronization.

3. **Queue-Based Writing**:
   - A queue collects checker objects from finished threads.
   - Violations are written to the main results dictionary in a thread-safe manner.


