import pytest
from datetime import datetime, timezone
from src.models import Customer, SupportTicket, TicketPriority
from src.repository import parse_ticket_timestamp
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
        created_at=datetime(2026, 8, 9, 9, 30, tzinfo=timezone.utc),
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
        created_at=datetime(2026, 8, 9, 9, 30, tzinfo=timezone.utc),
    )

    with pytest.raises(TicketValidationError):
        validate_ticket(ticket)


def test_parse_ticket_timestamp_accepts_utc():
    timestamp = parse_ticket_timestamp("2026-08-09T09:30:00+00:00")

    assert timestamp == datetime(2026, 8, 9, 9, 30, tzinfo=timezone.utc)


def test_parse_ticket_timestamp_rejects_naive_value():
    with pytest.raises(ValueError):
        parse_ticket_timestamp("2026-08-09T09:30:00")