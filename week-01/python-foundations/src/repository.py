import csv
from datetime import datetime
from pathlib import Path

from .models import Customer, SupportTicket, TicketPriority, TicketStatus


SAMPLE_TICKETS_PATH = Path(__file__).with_name("data") / "sample_tickets.csv"


def parse_ticket_timestamp(value: str | None) -> datetime:
    if not value or not value.strip():
        raise ValueError("created_at is required.")

    timestamp = datetime.fromisoformat(value.strip())
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("created_at must include a timezone.")
    if timestamp.utcoffset().total_seconds() != 0:
        raise ValueError("created_at must be in UTC.")
    return timestamp


def load_sample_tickets() -> list[SupportTicket]:
    """Load deterministic, non-sensitive tickets from the sample CSV."""
    with SAMPLE_TICKETS_PATH.open(newline="", encoding="utf-8") as sample_file:
        rows = csv.DictReader(sample_file)
        return [
            SupportTicket(
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
            for row in rows
        ]