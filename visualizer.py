"""
visualizer.py - Terminal Linked List Visualizer for BankLink

Produces clean ASCII visualizations of the BankLinkedList showing
nodes, data fields, next pointers, HEAD, and TAIL.
"""

import sys
from typing import Optional
from linked_list import BankLinkedList
from account import AccountNode

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def render_linked_list(bank_list: BankLinkedList) -> str:
    """
    Generate an ASCII string diagram showing the linked list structure.
    Example:
      HEAD -> [101: Asha | ₹5000.00] -> [102: Ravi | ₹12500.50] -> NULL
    """
    if bank_list.head is None:
        lines = [
            "┌────────────────────────────────────────────────────────┐",
            "│           LINKED LIST STRUCTURAL DIAGRAM               │",
            "└────────────────────────────────────────────────────────┘",
            "  HEAD ──> NULL",
            "  TAIL ──> NULL",
            "  Status: Linked list is empty (0 nodes).",
        ]
        return "\n".join(lines)

    lines = [
        "┌─────────────────────────────────────────────────────────────────────────┐",
        "│                      LINKED LIST STRUCTURAL DIAGRAM                     │",
        "└─────────────────────────────────────────────────────────────────────────┘",
    ]

    # Compact pointer chain
    chain_parts = ["HEAD"]
    curr: Optional[AccountNode] = bank_list.head
    while curr is not None:
        chain_parts.append(f"[{curr.account_no}: {curr.name} (₹{curr.balance})]")
        curr = curr.next
    chain_parts.append("NULL")

    # Format pointer chain, wrapping cleanly if lines are long
    chain_str = " ──> ".join(chain_parts)
    lines.append(f"\n{chain_str}\n")

    # Pointer indicators
    lines.append("POINTER METADATA:")
    lines.append(f"  • HEAD points to: Node #{bank_list.head.account_no} ({bank_list.head.name})")
    if bank_list.tail is not None:
        lines.append(f"  • TAIL points to: Node #{bank_list.tail.account_no} ({bank_list.tail.name})")
    lines.append(f"  • Total active nodes (size): {bank_list.size}")

    # Detailed node inspection
    lines.append("\nNODE DETAIL MAP:")
    lines.append(f"  {'Index':<6} {'Account No':<12} {'Holder Name':<18} {'Balance':<14} {'Next Node Pointer':<20}")
    lines.append("  " + "─" * 72)

    curr = bank_list.head
    idx = 0
    while curr is not None:
        next_ptr_str = f"Node #{curr.next.account_no}" if curr.next is not None else "NULL (End of List)"
        tag = ""
        if curr == bank_list.head and curr == bank_list.tail:
            tag = " [HEAD & TAIL]"
        elif curr == bank_list.head:
            tag = " [HEAD]"
        elif curr == bank_list.tail:
            tag = " [TAIL]"

        lines.append(
            f"  [{idx:<3}] {curr.account_no:<12} {curr.name:<18} ₹{curr.balance:<13} {next_ptr_str + tag}"
        )
        idx += 1
        curr = curr.next

    return "\n".join(lines)


def print_visualization(bank_list: BankLinkedList) -> None:
    """Convenience function to print visual diagram directly to console."""
    print(render_linked_list(bank_list))
