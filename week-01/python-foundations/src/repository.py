import csv
import json
import os
from datetime import datetime
from pathlib import Path

from .models import Customer, SupportTicket, TicketPriority, TicketStatus


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SAMPLE_TICKETS_PATH = DATA_DIR / "sample_tickets.csv"
SAMPLE_TICKETS_JSON_PATH = DATA_DIR / "tickets.json"


def parse_ticket_timestamp(value: str | None) -> datetime:
    if not value or not value.strip():
        raise ValueError("created_at is required.")

    timestamp = datetime.fromisoformat(value.strip())
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("created_at must include a timezone.")
    if timestamp.utcoffset().total_seconds() != 0:
        raise ValueError("created_at must be in UTC.")
    return timestamp


def _ticket_from_row(row: dict[str, str]) -> SupportTicket:
    return SupportTicket(
        ticket_id=row["ticket_id"].strip(),
        customer=Customer(
            customer_id=row["customer_id"].strip(),
            name=row["customer_name"].strip(),
            email=row["customer_email"].strip(),
        ),
        subject=row["subject"].strip(),
        description=row["description"].strip(),
        created_at=parse_ticket_timestamp(row.get("created_at")),
        priority=TicketPriority[row["priority"].strip()],
        status=TicketStatus[row["status"].strip()],
    )


def load_sample_tickets() -> list[SupportTicket]:
    """Load deterministic, non-sensitive tickets from the sample CSV."""
    with SAMPLE_TICKETS_PATH.open(newline="", encoding="utf-8") as sample_file:
        return [_ticket_from_row(row) for row in csv.DictReader(sample_file)]


def load_sample_tickets_json() -> list[SupportTicket]:
    """Load deterministic, non-sensitive tickets from the sample JSON."""
    with SAMPLE_TICKETS_JSON_PATH.open(encoding="utf-8") as sample_file:
        rows = json.load(sample_file)
    return [_ticket_from_row(row) for row in rows]


def load_tickets() -> list[SupportTicket]:
    """Load tickets from TICKET_DATA_PATH or the default CSV file."""
    configured_path = os.getenv("TICKET_DATA_PATH")
    if not configured_path:
        return load_sample_tickets()

    data_path = Path(configured_path)
    if data_path.suffix.lower() == ".json":
        with data_path.open(encoding="utf-8") as data_file:
            rows = json.load(data_file)
    elif data_path.suffix.lower() == ".csv":
        with data_path.open(newline="", encoding="utf-8") as data_file:
            rows = csv.DictReader(data_file)
    else:
        raise ValueError("TICKET_DATA_PATH must point to a .csv or .json file.")

    return [_ticket_from_row(row) for row in rows]