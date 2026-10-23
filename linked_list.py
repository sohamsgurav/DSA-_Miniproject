"""
linked_list.py - Custom Singly Linked List for BankLink Account Records

Implements BankLinkedList with head and tail pointers.
Stores all runtime account records directly in this linked list.
No Python list or dictionary is used as the primary storage.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional, Generator, Tuple, Union
from account import AccountNode


class BankLinkedList:
    """
    A custom singly linked list that stores and manages AccountNode instances.
    
    Attributes:
        head: Points to the first AccountNode in the list, or None if empty.
        tail: Points to the last AccountNode in the list, or None if empty.
        size: Total number of active accounts in the list.
    """

    def __init__(self) -> None:
        self.head: Optional[AccountNode] = None
        self.tail: Optional[AccountNode] = None
        self.size: int = 0

    def is_empty(self) -> bool:
        """Check if the linked list contains no accounts."""
        return self.head is None

    def get_account_count(self) -> int:
        """Return total number of accounts in O(1) time."""
        return self.size

    def __len__(self) -> int:
        """Allow use of len(bank_list)."""
        return self.size

    def __iter__(self) -> Generator[AccountNode, None, None]:
        """
        Traverse the linked list from head to tail, yielding each AccountNode.
        Time Complexity: O(n)
        """
        curr = self.head
        while curr is not None:
            yield curr
            curr = curr.next

    def search_account(self, account_no: str) -> Optional[AccountNode]:
        """
        Perform a linear search for an account by its account number.
        Time Complexity: O(n)
        
        Args:
            account_no: The account number to look up.
            
        Returns:
            The AccountNode if found, or None if not present.
        """
        if not account_no:
            return None
            
        target = str(account_no).strip().upper()
        curr = self.head
        while curr is not None:
            if curr.account_no.upper() == target:
                return curr
            curr = curr.next
        return None

    def insert_node(self, node: AccountNode) -> None:
        """
        Append an existing AccountNode to the tail of the list in O(1) time.
        Ensures node.next is cleared and updates head, tail, and size.
        
        Args:
            node: The AccountNode to append.
        """
        node.next = None
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self.size += 1

    def insert_account(
        self,
        account_no: str,
        name: str,
        account_type: str,
        balance: Union[Decimal, str, int, float],
    ) -> Tuple[bool, str, Optional[AccountNode]]:
        """
        Validate uniqueness via linear search O(n), create node, and append at tail O(1).
        
        Args:
            account_no: Unique account number.
            name: Customer name.
            account_type: 'Savings' or 'Current'.
            balance: Opening balance (non-negative).
            
        Returns:
            Tuple of (success: bool, message: str, node: Optional[AccountNode])
        """
        account_no_clean = str(account_no).strip()
        name_clean = str(name).strip()
        type_clean = str(account_type).strip().capitalize()

        if not account_no_clean:
            return False, "Account number cannot be empty.", None

        if not name_clean:
            return False, "Customer name cannot be empty.", None

        if type_clean not in {"Savings", "Current"}:
            return False, f"Invalid account type '{account_type}'. Must be 'Savings' or 'Current'.", None

        try:
            balance_dec = Decimal(str(balance)).quantize(Decimal("0.01"))
            if balance_dec < Decimal("0.00"):
                return False, "Opening balance cannot be negative.", None
        except Exception as e:
            return False, f"Invalid opening balance format: {e}", None

        # Check for duplicate account number (O(n) linear search)
        if self.search_account(account_no_clean) is not None:
            return False, f"Account #{account_no_clean} already exists. Account numbers must be unique.", None

        # Create new node
        new_node = AccountNode(
            account_no=account_no_clean,
            name=name_clean,
            account_type=type_clean,
            balance=balance_dec,
        )

        # Record opening balance transaction
        new_node.transactions.append(
            trans_id="TXN-INIT",
            trans_type="Opening",
            amount=balance_dec,
            balance_after=balance_dec,
            description="Account opening balance",
        )

        # Insert at tail in O(1)
        self.insert_node(new_node)
        return True, f"Account #{account_no_clean} created successfully for {name_clean}.", new_node

    def delete_account(self, account_no: str) -> Tuple[bool, str]:
        """
        Delete an account node by account_no with correct pointer updates.
        Handles:
          - Empty list
          - Deleting the only node (head == tail)
          - Deleting the head node (size > 1)
          - Deleting the tail node (size > 1)
          - Deleting a middle node
          - Account not found
          
        Time Complexity: O(n)
        
        Args:
            account_no: Account number to delete.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if self.head is None:
            return False, "Deletion failed: Bank has no accounts."

        target = str(account_no).strip().upper()

        curr: Optional[AccountNode] = self.head
        prev: Optional[AccountNode] = None

        # Traverse to find the matching node and its predecessor
        while curr is not None and curr.account_no.upper() != target:
            prev = curr
            curr = curr.next

        if curr is None:
            return False, f"Deletion failed: Account #{account_no} not found."

        # Case 1: Target is the only node in the list
        if curr == self.head and curr == self.tail:
            self.head = None
            self.tail = None
            self.size = 0
            return True, f"Account #{account_no} was the only account and was successfully deleted."

        # Case 2: Target is the head node (list has more than 1 node)
        if curr == self.head:
            self.head = self.head.next
            curr.next = None  # Detach deleted node
            self.size -= 1
            return True, f"Account #{account_no} (HEAD) was successfully deleted."

        # Case 3: Target is the tail node (list has more than 1 node)
        if curr == self.tail:
            assert prev is not None
            prev.next = None
            self.tail = prev
            curr.next = None  # Detach deleted node
            self.size -= 1
            return True, f"Account #{account_no} (TAIL) was successfully deleted."

        # Case 4: Target is in the middle
        assert prev is not None
        prev.next = curr.next
        curr.next = None  # Detach deleted node
        self.size -= 1
        return True, f"Account #{account_no} was successfully deleted."

    def get_total_balance(self) -> Decimal:
        """
        Calculate the sum of balances across all accounts in O(n) time.
        Uses Decimal to preserve exact currency precision.
        """
        total = Decimal("0.00")
        curr = self.head
        while curr is not None:
            total += curr.balance
            curr = curr.next
        return total

    def get_highest_balance_account(self) -> Optional[AccountNode]:
        """
        Find and return the AccountNode with the highest balance in O(n) time.
        Returns None if the list is empty.
        """
        if self.head is None:
            return None

        highest_node = self.head
        curr = self.head.next
        while curr is not None:
            if curr.balance > highest_node.balance:
                highest_node = curr
            curr = curr.next
        return highest_node

    def recalculate_tail_and_size(self) -> None:
        """
        Utility method to recount size and restore the tail pointer
        after direct pointer rearrangements (e.g. merge sort).
        """
        if self.head is None:
            self.tail = None
            self.size = 0
            return

        count = 1
        curr = self.head
        while curr.next is not None:
            count += 1
            curr = curr.next

        self.tail = curr
        self.size = count

    def clear(self) -> None:
        """Remove all nodes from the linked list."""
        self.head = None
        self.tail = None
        self.size = 0
