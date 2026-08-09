from dataclasses import dataclass
from datetime import datetime, timezone
from .exceptions import TicketValidationError
from enum import Enum

class TicketPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    
class TicketStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str = ""
    
    def __post_init__(self):
            self.name = " ".join(self.name.split())
    
            if not self.name:
                raise TicketValidationError(
                    "Customer name cannot be blank."
                )

@dataclass
class SupportTicket:
    ticket_id: str
    customer: Customer
    subject: str   
    description: str
    created_at: datetime
    internal_notes: str = ""
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN

    def __post_init__(self):
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise TicketValidationError("created_at must be timezone-aware UTC.")
        if self.created_at.utcoffset() != timezone.utc.utcoffset(self.created_at):
            raise TicketValidationError("created_at must be in UTC.")
        self.created_at = self.created_at.astimezone(timezone.utc)
    
    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "customer_id": self.customer.customer_id,
            "subject": self.subject,
            "description": self.description,
            "created_at": self.created_at,
            "priority": self.priority.value,
            "status": self.status.value,
        }