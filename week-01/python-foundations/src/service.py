from collections import defaultdict
from collections.abc import Sequence

from .models import SupportTicket, TicketPriority


def get_high_priority_tickets(
    tickets: Sequence[SupportTicket],
) -> list[SupportTicket]:
    """Return tickets with HIGH or CRITICAL priority."""
    return [
        ticket
        for ticket in tickets
        if ticket.priority in {TicketPriority.HIGH, TicketPriority.CRITICAL}
    ]


def group_tickets_by_priority(
    tickets: Sequence[SupportTicket],
) -> dict[TicketPriority, list[SupportTicket]]:
    """Group tickets by their priority."""
    grouped_tickets: dict[TicketPriority, list[SupportTicket]] = defaultdict(list)
    for ticket in tickets:
        grouped_tickets[ticket.priority].append(ticket)
    return dict(grouped_tickets)


def count_tickets_by_customer(
    tickets: Sequence[SupportTicket],
) -> dict[str, int]:
    """Count tickets for each customer."""
    ticket_count: dict[str, int] = defaultdict(int)
    for ticket in tickets:
        ticket_count[ticket.customer.customer_id] += 1
    return dict(ticket_count)


def get_five_newest_tickets(
    tickets: Sequence[SupportTicket],
) -> list[SupportTicket]:
    """Return the five most recently created tickets."""
    return sorted(tickets, key=lambda ticket: ticket.created_at, reverse=True)[:5]