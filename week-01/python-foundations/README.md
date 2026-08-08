# Python Foundations: Enterprise Ticket Intake

## Purpose

**Python foundations: enterprise ticket intake.**

This project is a small enterprise-style customer support intake application
used to practice Python fundamentals, data modeling, validation, error
handling, logging, testing, and project structure.

## Prerequisites — WSL

The project is intended to run inside WSL.

Required:

* WSL2
* Python 3.11+
* `pip`
* Git

Verify the installation:

```bash
python3 --version
pip3 --version
git --version
```

## Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <project-directory>
```

Create and activate the project-local virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the application

From the project root:

```bash
python -m src.main
```

## Run tests

Run the complete test suite:

```bash
python -m pytest -q
```

## Architectural Choices

### Typed models

Use Python `dataclasses` and `Enum` to represent domain concepts such as
customers, support tickets, and ticket priorities.

### Validation

Business validation is kept explicit and uses application-specific
exceptions for invalid ticket data.

### Logging

Use Python's standard `logging` module with:

* Named module-level loggers.
* `INFO` for normal workflow events.
* `WARNING` for recoverable invalid input.
* `ERROR` for unexpected failures with exception context.

Logging configuration is centralized separately from business logic.

### Tests

Use `pytest` to verify domain behavior, validation rules, and application
workflows.

## Known Limitations

* Data is local and stored only in memory.
* There is no persistent database.
* Data is lost when the application stops.
* The application is intended as a learning project rather than a
  production-ready ticket management system.
