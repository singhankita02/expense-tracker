
from dataclasses import dataclass

@dataclass
class Expense:
    id: str
    client_request_id: str
    amount: str
    category: str
    description: str
    date: str
    created_at: str
