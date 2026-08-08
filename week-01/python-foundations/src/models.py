from dataclasses import dataclass
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
    internal_notes: str = ""
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN
    
    def to_dict(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "customer_id": self.customer.customer_id,
            "subject": self.subject,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
        }