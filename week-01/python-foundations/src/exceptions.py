class ApplicationError(Exception):
    """Base class for application-specific exceptions."""
    pass

class TicketValidationError(ApplicationError):
    """Exception raised for errors in the ticket validation."""
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Ticket validation failed.")
    pass

class TicketProcessingError(ApplicationError):
    """Exception raised for errors during ticket processing."""
    pass