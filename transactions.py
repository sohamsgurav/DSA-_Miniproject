"""
transactions.py - Transaction History Linked List for BankLink

Implements a custom singly linked list for per-account transaction history.
Demonstrates linked-list node creation, insertion at tail, traversal, and serialization.
"""

from __future__ import annotations

from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, Any, Generator, List


class TransactionNode:
    """
    A single node in an account's transaction history linked list.
    
    Attributes:
        trans_id: Unique string identifier for the transaction (e.g., TXN1001).
        trans_type: Type of transaction ('Deposit', 'Withdrawal', 'Transfer Out', 'Transfer In', 'Opening').
        amount: Monetary amount of the transaction as Decimal.
        balance_after: Resulting account balance after transaction as Decimal.
        description: Informational note or counterparty details.
        timestamp: Date and time of transaction (ISO string or formatted string).
        next: Reference to the next TransactionNode in the list.
    """

    def __init__(
        self,
        trans_id: str,
        trans_type: str,
        amount: Decimal,
        balance_after: Decimal,
        description: str = "",
        timestamp: Optional[str] = None,
    ) -> None:
        self.trans_id: str = str(trans_id).strip()
        self.trans_type: str = str(trans_type).strip()
        self.amount: Decimal = Decimal(str(amount))
        self.balance_after: Decimal = Decimal(str(balance_after))
        self.description: str = str(description).strip()
        self.timestamp: str = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next: Optional["TransactionNode"] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction node to a dictionary for JSON serialization."""
        return {
            "trans_id": self.trans_id,
            "trans_type": self.trans_type,
            "amount": str(self.amount),
            "balance_after": str(self.balance_after),
            "description": self.description,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransactionNode":
        """Create a TransactionNode from a dictionary."""
        return cls(
            trans_id=data["trans_id"],
            trans_type=data["trans_type"],
            amount=Decimal(data["amount"]),
            balance_after=Decimal(data["balance_after"]),
            description=data.get("description", ""),
            timestamp=data.get("timestamp"),
        )

    def __repr__(self) -> str:
        return f"<TransactionNode {self.trans_id} | {self.trans_type} | {self.amount}>"


class TransactionLinkedList:
    """
    Custom singly linked list managing transaction history for an account.
    Maintains head and tail pointers for O(1) appending of new transactions.
    """

    def __init__(self) -> None:
        self.head: Optional[TransactionNode] = None
        self.tail: Optional[TransactionNode] = None
        self.size: int = 0

    def append(
        self,
        trans_id: str,
        trans_type: str,
        amount: Decimal,
        balance_after: Decimal,
        description: str = "",
        timestamp: Optional[str] = None,
    ) -> TransactionNode:
        """
        Append a new transaction to the end of the history list in O(1) time.
        """
        node = TransactionNode(
            trans_id=trans_id,
            trans_type=trans_type,
            amount=amount,
            balance_after=balance_after,
            description=description,
            timestamp=timestamp,
        )
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self.size += 1
        return node

    def is_empty(self) -> bool:
        """Check if transaction history is empty."""
        return self.head is None

    def __len__(self) -> int:
        """Return number of transactions recorded."""
        return self.size

    def __iter__(self) -> Generator[TransactionNode, None, None]:
        """Iterate over transaction nodes from oldest to newest."""
        curr = self.head
        while curr is not None:
            yield curr
            curr = curr.next

    def to_list(self) -> List[Dict[str, Any]]:
        """Serialize transaction history to a list of dicts for JSON storage."""
        records: List[Dict[str, Any]] = []
        for node in self:
            records.append(node.to_dict())
        return records

    @classmethod
    def from_list(cls, records: List[Dict[str, Any]]) -> "TransactionLinkedList":
        """Reconstruct a TransactionLinkedList from a list of dict records."""
        history = cls()
        for record in records:
            history.append(
                trans_id=record["trans_id"],
                trans_type=record["trans_type"],
                amount=Decimal(record["amount"]),
                balance_after=Decimal(record["balance_after"]),
                description=record.get("description", ""),
                timestamp=record.get("timestamp"),
            )
        return history
