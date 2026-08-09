import pytest
from src.models import Customer, SupportTicket, TicketPriority
from src.repository import load_sample_tickets
from src.validation import validate_ticket, validate_ticket_for_triage
from src.service import get_five_newest_tickets, get_high_priority_tickets, group_tickets_by_priority, count_tickets_by_customer



def test_generated_sample_tickets_are_valid_and_varied():
    tickets = load_sample_tickets()

    assert len(tickets) == 100
    assert {ticket.priority for ticket in tickets} == set(TicketPriority)
    assert all(validate_ticket(ticket) == [] for ticket in tickets)

def test_get_five_newest_tickets_does_not_mutate_input():
    tickets = load_sample_tickets()
    original_tickets = tickets.copy()

    newest_tickets = get_five_newest_tickets(tickets)

    assert tickets == original_tickets
    assert len(newest_tickets) == 5
    
def test_get_high_priority_tickets():
    tickets = load_sample_tickets()
    high_priority_tickets = get_high_priority_tickets(tickets)

    assert all(
        ticket.priority in {
            TicketPriority.HIGH, 
            TicketPriority.CRITICAL
        }
        for ticket in high_priority_tickets)
    
def test_group_tickets_by_priority():
    tickets = load_sample_tickets()
    grouped_tickets = group_tickets_by_priority(tickets)

    assert set(grouped_tickets.keys()) == set(TicketPriority)
    assert all(
        ticket.priority == priority
        for priority, tickets in grouped_tickets.items()
        for ticket in tickets
    )
    
def test_count_tickets_by_customer():
    tickets = load_sample_tickets()
    ticket_counts = count_tickets_by_customer(tickets)

    assert all(
        ticket_counts[customer_id] == sum(
            1 
            for ticket in tickets 
            if ticket.customer.customer_id == customer_id
        )
        for customer_id in {ticket.customer.customer_id for ticket in tickets}
    )