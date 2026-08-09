import pytest
from datetime import datetime, timezone
from src.models import Customer, SupportTicket, TicketPriority
from src import repository
from src.repository import load_sample_tickets_json, load_tickets, parse_ticket_timestamp
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


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (None, "created_at is required"),
        ("", "created_at is required"),
        ("not-a-timestamp", "Invalid isoformat string"),
        ("2026-08-09T09:30:00", "must include a timezone"),
        ("2026-08-09T09:30:00+05:00", "must be in UTC"),
    ],
)
def test_parse_ticket_timestamp_rejects_invalid_values(value, message):
    with pytest.raises(ValueError, match=message):
        parse_ticket_timestamp(value)


def test_load_sample_tickets_rejects_one_invalid_ticket_in_valid_data(
    tmp_path, monkeypatch
):
    csv_data = """ticket_id,customer_id,customer_name,customer_email,subject,description,priority,status,created_at
T2001,C2001,Valid One,one@example.com,Valid ticket,This is a valid ticket description.,HIGH,OPEN,2026-08-09T09:30:00+00:00
T2002,C2002,Invalid Two,two@example.com,Invalid ticket,This ticket has an invalid timestamp.,MEDIUM,OPEN,2026-08-09T09:30:00
T2003,C2003,Valid Three,three@example.com,Valid ticket,This is another valid ticket description.,LOW,CLOSED,2026-08-09T10:30:00+00:00
"""
    csv_path = tmp_path / "tickets.csv"
    csv_path.write_text(csv_data)
    monkeypatch.setattr(repository, "SAMPLE_TICKETS_PATH", csv_path)

    with pytest.raises(ValueError, match="must include a timezone"):
        repository.load_sample_tickets()


def test_load_sample_tickets_json():
    tickets = load_sample_tickets_json()

    assert len(tickets) == 100
    assert all(ticket.created_at.utcoffset().total_seconds() == 0 for ticket in tickets)


def test_load_tickets_uses_environment_path(tmp_path, monkeypatch):
    data_path = tmp_path / "tickets.json"
    data_path.write_text(
        "[{\"ticket_id\": \"T3001\", \"customer_id\": \"C3001\", "
        "\"customer_name\": \"Environment User\", "
        "\"customer_email\": \"user@example.com\", "
        "\"subject\": \"Configured data path\", "
        "\"description\": \"This ticket came from the configured data path.\", "
        "\"priority\": \"HIGH\", \"status\": \"OPEN\", "
        "\"created_at\": \"2026-08-09T09:30:00+00:00\"}]"
    )
    monkeypatch.setenv("TICKET_DATA_PATH", str(data_path))

    tickets = load_tickets()

    assert len(tickets) == 1
    assert tickets[0].ticket_id == "T3001"