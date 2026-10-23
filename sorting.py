"""
sorting.py - Linked List Merge Sort for BankLink Accounts

Implements Merge Sort directly on AccountNode pointers.
Sorts in O(n log n) time and O(log n) call-stack space.
Does NOT convert nodes into a Python list or dictionary.
"""

from typing import Optional
from decimal import Decimal
from account import AccountNode
from linked_list import BankLinkedList


def _compare(node_a: AccountNode, node_b: AccountNode, key: str, reverse: bool) -> bool:
    """
    Compare two nodes based on the specified attribute and ordering.
    Returns True if node_a should come before or equal to node_b.
    """
    if key == "balance":
        val_a = node_a.balance
        val_b = node_b.balance
    elif key == "name":
        val_a = node_a.name.lower()
        val_b = node_b.name.lower()
    elif key == "account_no":
        val_a = node_a.account_no
        val_b = node_b.account_no
    else:
        val_a = node_a.balance
        val_b = node_b.balance

    if reverse:
        return val_a >= val_b
    return val_a <= val_b


def _get_middle(head: AccountNode) -> AccountNode:
    """
    Find the midpoint node of a singly linked list using the two-pointer
    (slow and fast pointer / Tortoise and Hare) technique.
    Time Complexity: O(n)
    """
    slow: AccountNode = head
    fast: Optional[AccountNode] = head.next

    while fast is not None and fast.next is not None:
        assert slow.next is not None
        slow = slow.next
        fast = fast.next.next

    return slow


def _sorted_merge(
    left: Optional[AccountNode],
    right: Optional[AccountNode],
    key: str,
    reverse: bool,
) -> Optional[AccountNode]:
    """
    Merge two sorted linked lists by relinking pointers.
    Does not allocate new account nodes.
    Time Complexity: O(n)
    """
    # Create a dummy sentinel node to simplify pointer manipulation
    dummy = AccountNode("__dummy__", "dummy", "Savings", Decimal("0.00"))
    tail = dummy

    curr_left = left
    curr_right = right

    while curr_left is not None and curr_right is not None:
        if _compare(curr_left, curr_right, key, reverse):
            tail.next = curr_left
            curr_left = curr_left.next
        else:
            tail.next = curr_right
            curr_right = curr_right.next
        tail = tail.next

    # Splice remaining nodes
    if curr_left is not None:
        tail.next = curr_left
    elif curr_right is not None:
        tail.next = curr_right

    return dummy.next


def _merge_sort_nodes(
    head: Optional[AccountNode],
    key: str,
    reverse: bool,
) -> Optional[AccountNode]:
    """
    Recursive merge sort function operating directly on AccountNode pointers.
    Divides list into two halves and merges sorted sub-lists.
    Time Complexity: O(n log n)
    Space Complexity: O(log n) call-stack space
    """
    # Base cases: empty list or single node
    if head is None or head.next is None:
        return head

    # 1. Split the list in half using slow/fast pointer
    mid = _get_middle(head)
    next_to_mid = mid.next
    mid.next = None  # Sever link between halves

    # 2. Recursively sort each half
    left_sorted = _merge_sort_nodes(head, key, reverse)
    right_sorted = _merge_sort_nodes(next_to_mid, key, reverse)

    # 3. Merge the two sorted halves
    return _sorted_merge(left_sorted, right_sorted, key, reverse)


def merge_sort_accounts(
    bank_list: BankLinkedList,
    key: str = "balance",
    reverse: bool = False,
) -> None:
    """
    Sort the BankLinkedList in-place using linked-list merge sort.
    Updates head, tail, and size pointers directly.
    
    Args:
        bank_list: The BankLinkedList instance to sort.
        key: 'balance', 'name', or 'account_no'.
        reverse: True for descending order, False for ascending order.
    """
    if bank_list.head is None or bank_list.head.next is None:
        return

    # Sort nodes by relinking next pointers
    sorted_head = _merge_sort_nodes(bank_list.head, key=key, reverse=reverse)
    bank_list.head = sorted_head

    # Restore tail pointer and verify size
    bank_list.recalculate_tail_and_size()
