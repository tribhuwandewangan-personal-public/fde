import json
import logging

from .exceptions import TicketValidationError
from .repository import load_sample_tickets
from .service import get_high_priority_tickets
from .validation import validate_ticket

# Import the named application logger you created in Block 4.
# Adjust this import if your logger lives in a different module.
from .logging_config import configure_logging


def main() -> None:
    """Run the customer-support ticket intake workflow."""
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting support ticket intake workflow")

    tickets = load_sample_tickets()
    ticket = get_high_priority_tickets(tickets)[0]

    try:
        # 2. Validate the ticket.
        validate_ticket(ticket)

        logger.info(
            "Ticket validated successfully",
            extra={"ticket_id": ticket.ticket_id},
        )

        # 3. Create a compact JSON-like summary.
        summary = {
            "ticket_id": ticket.ticket_id,
            "customer_id": ticket.customer.customer_id,
            "subject": ticket.subject,
            "priority": ticket.priority.value,
            "status": "valid",
        }

        print(json.dumps(summary, indent=2))

        logger.info(
            "Support ticket intake workflow completed",
            extra={"ticket_id": ticket.ticket_id},
        )

    # 4. Handle known validation failures cleanly.
    except TicketValidationError as exc:
        logger.warning(
            "Ticket validation failed: %s",
            exc,
            extra={"ticket_id": ticket.ticket_id},
        )

        print(
            json.dumps(
                {
                    "ticket_id": ticket.ticket_id,
                    "status": "invalid",
                    "error": str(exc),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
