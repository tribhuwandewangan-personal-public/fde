import pytest
from src.models import Customer, SupportTicket, TicketPriority
from src.validation import validate_ticket, validate_ticket_for_triage
from src.exceptions import TicketValidationError

def test_valid_customer_name():
    customer = Customer(name="  Alice   Johnson  ", customer_id="C1001", email="john@gmail.com")

    assert customer.name == "Alice Johnson"

def test_blank_customer_name_is_rejected():
    with pytest.raises(TicketValidationError):
        Customer(
            name="   ",
            customer_id="C1001",
            email="john@gmail.com",
        )
        
def test_customer_name_whitespace_is_normalized():
    customer = Customer(name="  Alice   Johnson  ", customer_id="C1001", email="john@gmail.com")

    assert customer.name == "Alice Johnson"
    
def test_valid_ticket_can_be_triaged():
    customer = Customer(name="  Alice   Johnson  ", customer_id="C1001", email="john@gmail.com")

    ticket = SupportTicket(
        ticket_id="T1001",
        customer=customer,
        subject="Unable to login",
        description="Customer cannot access the application.",
    )

    errors = validate_ticket(ticket)
    assert errors == []

def test_ticket_without_subject_is_rejected():
    customer = Customer(name="Alice Johnson", customer_id="C1001", email="john@gmail.com")

    ticket = SupportTicket(
        customer=customer,
        subject="",
        ticket_id="T1001",
        description="Customer cannot access the application.",
    )

    with pytest.raises(TicketValidationError):
        validate_ticket(ticket)