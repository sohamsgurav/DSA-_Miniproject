"""
account.py - Account Node Definition for BankLink

Defines AccountNode, the building block of the singly linked list
used to store bank customer accounts.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional, Dict, Any, Union
from transactions import TransactionLinkedList, TransactionNode


class AccountNode:
    """
    Represents a bank account node in the singly linked list.

    Attributes:
        account_no: Unique account identifier (string).
        name: Account holder's full name.
        account_type: Type of account (e.g., 'Savings', 'Current').
        balance: Account balance stored as Decimal to prevent floating-point inaccuracies.
        next: Reference to the next AccountNode in the BankLinkedList.
        transactions: Custom TransactionLinkedList holding this account's transaction history.
    """

    def __init__(
        self,
        account_no: str,
        name: str,
        account_type: str,
        balance: Union[Decimal, str, int, float],
        next_node: Optional["AccountNode"] = None,
    ) -> None:
        self.account_no: str = str(account_no).strip()
        self.name: str = str(name).strip()
        self.account_type: str = str(account_type).strip().capitalize()
        # Enforce Decimal with 2 decimal places precision for currency
        self.balance: Decimal = Decimal(str(balance)).quantize(Decimal("0.01"))
        self.next: Optional["AccountNode"] = next_node
        self.transactions: TransactionLinkedList = TransactionLinkedList()

    @property
    def transactions_head(self) -> Optional[TransactionNode]:
        """Expose head of transaction linked list as required by architecture."""
        return self.transactions.head

    def to_dict(self) -> Dict[str, Any]:
        """Convert account node to a dictionary for JSON serialization."""
        return {
            "account_no": self.account_no,
            "name": self.name,
            "account_type": self.account_type,
            "balance": str(self.balance),
            "transactions": self.transactions.to_list(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountNode":
        """Reconstruct an AccountNode (and its transaction history) from dictionary data."""
        node = cls(
            account_no=data["account_no"],
            name=data["name"],
            account_type=data["account_type"],
            balance=Decimal(data["balance"]),
        )
        if "transactions" in data and isinstance(data["transactions"], list):
            node.transactions = TransactionLinkedList.from_list(data["transactions"])
        return node

    def __repr__(self) -> str:
        return f"<AccountNode #{self.account_no}: {self.name} | {self.account_type} | Bal: {self.balance}>"
