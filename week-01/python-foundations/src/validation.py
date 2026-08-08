from .models import SupportTicket, TicketPriority
from .exceptions import TicketValidationError

def validate_ticket_for_triage(ticket: SupportTicket) -> list[str]:
    errors = []
    if not ticket.customer.customer_id.strip():
        errors.append("Customer ID is required")
    if not ticket.subject.strip():
        errors.append("Subject is required")
    if not ticket.description.strip():
        errors.append("Description is required")
    if not len(ticket.description) > 20:
        errors.append("Description must be at least 20 characters long")
    if not isinstance(ticket.priority, TicketPriority):
        errors.append("Invalid ticket priority")
    return errors

def validate_ticket(ticket: SupportTicket) -> None:
    errors = validate_ticket_for_triage(ticket)

    if errors:
        raise TicketValidationError(errors)
    return errors