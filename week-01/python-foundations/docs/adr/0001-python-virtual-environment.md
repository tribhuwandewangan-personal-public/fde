# ADR 0001: Use structured application exceptions and module-level logging

* Status: Accepted
* Date: 2026-08-08
* Deciders:

## Context

The Forward Deployed Engineer learning project needs production-minded
error handling and logging.

The application performs ticket validation and business workflow operations
where expected validation failures should be distinguishable from unexpected
application failures.

The project also needs consistent logging that can be used to understand
normal workflow events, recoverable input problems, and unexpected failures.

Without a defined approach, application code may:

* Raise generic built-in exceptions for business errors.
* Log errors inconsistently across modules.
* Mix logging configuration with business logic.
* Lose useful exception context when unexpected failures occur.
* Make it difficult for callers or tests to distinguish validation failures
  from unexpected application failures.

## Decision

Use a small application-specific exception hierarchy and Python's standard
`logging` module.

### Exception hierarchy

Define a base application exception:

```python
class ApplicationError(Exception):
    """Base exception for application-specific errors."""
```

Business-specific exceptions inherit from this base class.

For example:

```python
class TicketValidationError(ApplicationError):
    """Exception raised for errors in ticket validation."""
```

These exceptions do not require additional implementation when their purpose
is only to provide a distinct exception type.

### Logging

Each application module that needs logging creates a named module logger:

```python
logger = logging.getLogger(__name__)
```

Logging configuration is kept separate from business logic.

The application logging configuration is initialized explicitly by the
application entry point.

Use the following logging levels:

* `INFO` — normal application workflow events.
* `WARNING` — recoverable invalid input or expected abnormal conditions.
* `ERROR` — unexpected failures, including exception context.

Unexpected exceptions should preserve the original exception context:

```python
logger.error("Unexpected error while processing ticket", exc_info=True)
```

### Logging configuration

Logging configuration is centralized in a dedicated module rather than being
configured independently by every application module.

Application modules are responsible only for creating loggers and emitting
log records.

## Consequences

### Positive

* Business errors have meaningful, testable exception types.
* Callers can distinguish application errors from unexpected failures.
* Logging behavior is consistent across modules.
* Exception context is preserved for unexpected failures.
* Logging configuration remains separate from application logic.
* The approach uses Python's standard library without introducing a logging
  framework dependency.
* The design provides a foundation for production observability as the
  application grows.

### Negative

* Developers must choose appropriate exception types and logging levels.
* Logging configuration requires an explicit initialization step.
* Poorly chosen log messages can still produce noisy or insufficient logs.
* Application-specific exceptions add a small amount of project structure.

## Alternatives considered

### Generic built-in exceptions

Use exceptions such as `ValueError` and `RuntimeError` throughout the
application.

**Rejected** because callers cannot clearly distinguish domain/application
failures from unrelated programming errors.

### Return error values instead of exceptions

Return validation results or error objects from every operation.

**Rejected** for this project because exceptions provide a cleaner boundary
for unexpected or invalid workflow conditions while allowing validation
logic to remain explicit.

### Configure logging inside every module

Each module configures its own logger and handlers.

**Rejected** because it can result in duplicated handlers, inconsistent
formats, and difficult-to-control logging behavior.

### Third-party logging framework

Use a structured logging library instead of Python's standard `logging`
module.

**Rejected for the current stage** because the project does not yet require
the additional capabilities of a third-party framework.

## Validation

The implementation is validated by:

* Creating application-specific exception classes.
* Creating a named logger in application modules.
* Configuring logging through a dedicated logging configuration module.
* Emitting `INFO` messages for normal workflow events.
* Emitting `WARNING` messages for recoverable validation problems.
* Emitting `ERROR` messages with exception context for unexpected failures.
* Running the project's test suite successfully.

```bash
python -m pytest -q
```

The application should be executed using the project's package structure so
that relative imports between application modules work correctly.
