"""
main.py - Interactive Terminal Application for BankLink

Entry point for the BankLink Bank Account Management System.
Implements the terminal menu, user input validation, and workflows.
Runtime accounts are stored strictly in a custom BankLinkedList.
"""

import sys
from decimal import Decimal
from typing import Optional

# Ensure standard output and error streams handle Unicode properly on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from linked_list import BankLinkedList
from account import AccountNode
from account_service import AccountService
from sorting import merge_sort_accounts
from visualizer import print_visualization
from storage import save_accounts, load_accounts, DEFAULT_STORAGE_FILE



def print_banner() -> None:
    """Print the BankLink application header."""
    print("=" * 50)
    print("        BANKLINK MANAGEMENT SYSTEM")
    print("    Educational Linked List Banking Simulation")
    print("=" * 50)


def print_menu() -> None:
    """Display the 12-item menu conforming to the architecture spec."""
    print("\n" + "=" * 50)
    print("              MAIN OPERATIONS MENU")
    print("=" * 50)
    print("  1. Create Account")
    print("  2. Display All Accounts")
    print("  3. Search Account")
    print("  4. Deposit Money")
    print("  5. Withdraw Money")
    print("  6. Transfer Money")
    print("  7. Delete Account")
    print("  8. View Transaction History")
    print("  9. Sort Accounts (Merge Sort on Linked List)")
    print(" 10. Visualize Linked List Structure")
    print(" 11. Show Bank Summary")
    print(" 12. Save and Exit")
    print("=" * 50)


def display_all_accounts_view(bank_list: BankLinkedList) -> None:
    """Display all registered accounts in a formatted ASCII table."""
    if bank_list.head is None:
        print("\n[!] The bank currently has no active accounts.")
        return

    print("\n" + "=" * 75)
    print(f"{'Acc No':<12} {'Customer Name':<22} {'Type':<12} {'Balance (INR)':<15} {'Status':<10}")
    print("=" * 75)

    curr: Optional[AccountNode] = bank_list.head
    while curr is not None:
        tag = ""
        if curr == bank_list.head and curr == bank_list.tail:
            tag = "[HEAD/TAIL]"
        elif curr == bank_list.head:
            tag = "[HEAD]"
        elif curr == bank_list.tail:
            tag = "[TAIL]"

        print(f"{curr.account_no:<12} {curr.name:<22} {curr.account_type:<12} ₹{curr.balance:<14} {tag}")
        curr = curr.next

    print("-" * 75)
    print(f"Total Accounts: {bank_list.size} | Total Balance: ₹{bank_list.get_total_balance()}")
    print("=" * 75)


def handle_create_account(service: AccountService) -> None:
    """Workflow to create a new account."""
    print("\n--- CREATE NEW ACCOUNT ---")
    acc_no = input("Enter unique Account Number (e.g. 101, ACC1001): ").strip()
    if not acc_no:
        print("[Error] Account number cannot be empty.")
        return

    # Check existence before prompting further
    existing = service.search_account(acc_no)
    if existing is not None:
        print(f"[Error] Account #{acc_no} already exists (Held by: {existing.name}).")
        return

    name = input("Enter Customer Name: ").strip()
    if not name:
        print("[Error] Customer name cannot be empty.")
        return

    print("Account Types: [1] Savings  [2] Current")
    type_choice = input("Select Account Type [1/2, default 1]: ").strip()
    acc_type = "Current" if type_choice == "2" else "Savings"

    bal_input = input("Enter Opening Balance (₹, min 0.00): ").strip() or "0.00"

    success, msg, node = service.create_account(
        account_no=acc_no,
        name=name,
        account_type=acc_type,
        opening_balance=bal_input,
    )

    if success and node:
        print(f"[Success] {msg}")
        print(f"  Account No   : {node.account_no}")
        print(f"  Holder Name  : {node.name}")
        print(f"  Account Type : {node.account_type}")
        print(f"  Balance      : ₹{node.balance}")
    else:
        print(f"[Error] {msg}")


def handle_search_account(service: AccountService) -> None:
    """Workflow to search an account by account number."""
    print("\n--- SEARCH ACCOUNT ---")
    acc_no = input("Enter Account Number to search: ").strip()
    if not acc_no:
        print("[Error] Account number cannot be empty.")
        return

    node = service.search_account(acc_no)
    if node is None:
        print(f"[!] Account #{acc_no} was not found in the bank database.")
    else:
        print("\n" + "=" * 45)
        print("           ACCOUNT DETAILS")
        print("=" * 45)
        print(f"  Account Number : {node.account_no}")
        print(f"  Customer Name  : {node.name}")
        print(f"  Account Type   : {node.account_type}")
        print(f"  Current Balance: ₹{node.balance}")
        print(f"  Transactions   : {len(node.transactions)} recorded")
        next_val = f"Node #{node.next.account_no}" if node.next else "NULL"
        print(f"  Next Pointer   : {next_val}")
        print("=" * 45)


def handle_deposit(service: AccountService) -> None:
    """Workflow to deposit money."""
    print("\n--- DEPOSIT FUNDS ---")
    acc_no = input("Enter Account Number: ").strip()
    node = service.search_account(acc_no)
    if node is None:
        print(f"[Error] Account #{acc_no} does not exist.")
        return

    print(f"Account Found: {node.name} (Current Balance: ₹{node.balance})")
    amount_str = input("Enter Deposit Amount (₹): ").strip()
    note = input("Enter Note/Description [Optional]: ").strip() or "Counter Deposit"

    success, msg, _ = service.deposit(acc_no, amount_str, note)
    if success:
        print(f"[Success] {msg}")
    else:
        print(f"[Error] {msg}")


def handle_withdraw(service: AccountService) -> None:
    """Workflow to withdraw money."""
    print("\n--- WITHDRAW FUNDS ---")
    acc_no = input("Enter Account Number: ").strip()
    node = service.search_account(acc_no)
    if node is None:
        print(f"[Error] Account #{acc_no} does not exist.")
        return

    print(f"Account Found: {node.name} (Available Balance: ₹{node.balance})")
    amount_str = input("Enter Withdrawal Amount (₹): ").strip()
    note = input("Enter Note/Description [Optional]: ").strip() or "ATM/Counter Withdrawal"

    success, msg, _ = service.withdraw(acc_no, amount_str, note)
    if success:
        print(f"[Success] {msg}")
    else:
        print(f"[Error] {msg}")


def handle_transfer(service: AccountService) -> None:
    """Workflow to transfer money between two existing accounts."""
    print("\n--- TRANSFER FUNDS ---")
    sender_no = input("Enter Sender Account Number: ").strip()
    sender = service.search_account(sender_no)
    if sender is None:
        print(f"[Error] Sender account #{sender_no} does not exist.")
        return

    print(f"Sender: {sender.name} (Available Balance: ₹{sender.balance})")

    recipient_no = input("Enter Recipient Account Number: ").strip()
    if recipient_no.upper() == sender_no.upper():
        print("[Error] Sender and Recipient accounts cannot be the same.")
        return

    recipient = service.search_account(recipient_no)
    if recipient is None:
        print(f"[Error] Recipient account #{recipient_no} does not exist.")
        return

    print(f"Recipient: {recipient.name}")
    amount_str = input("Enter Transfer Amount (₹): ").strip()
    note = input("Enter Reference / Note [Optional]: ").strip() or "Inter-account Transfer"

    success, msg = service.transfer(sender_no, recipient_no, amount_str, note)
    if success:
        print(f"[Success] {msg}")
    else:
        print(f"[Error] {msg}")


def handle_delete_account(service: AccountService) -> None:
    """Workflow to delete an account with confirmation."""
    print("\n--- DELETE ACCOUNT ---")
    acc_no = input("Enter Account Number to delete: ").strip()
    node = service.search_account(acc_no)
    if node is None:
        print(f"[Error] Account #{acc_no} not found.")
        return

    print(f"\n[CAUTION] You are about to permanently delete:")
    print(f"  Account #{node.account_no} | Name: {node.name} | Balance: ₹{node.balance}")
    confirm = input("Are you sure you want to delete this account? (Type 'yes' or 'y' to confirm): ").strip().lower()

    if confirm in {"yes", "y"}:
        success, msg = service.delete_account(acc_no)
        if success:
            print(f"[Success] {msg}")
        else:
            print(f"[Error] {msg}")
    else:
        print("[Cancelled] Deletion aborted. Account remains active.")


def handle_transaction_history(service: AccountService) -> None:
    """Workflow to view an account's transaction history linked list."""
    print("\n--- TRANSACTION HISTORY ---")
    acc_no = input("Enter Account Number: ").strip()
    node = service.search_account(acc_no)
    if node is None:
        print(f"[Error] Account #{acc_no} not found.")
        return

    print("\n" + "=" * 80)
    print(f"  PASSBOOK HISTORY FOR: #{node.account_no} ({node.name})")
    print(f"  Account Type: {node.account_type} | Current Balance: ₹{node.balance}")
    print("=" * 80)

    if node.transactions.is_empty():
        print("  No transactions recorded for this account yet.")
    else:
        print(f"  {'Txn ID':<16} {'Type':<14} {'Amount':<12} {'Balance After':<14} {'Date/Time':<20}")
        print("  " + "-" * 76)
        for txn in node.transactions:
            print(
                f"  {txn.trans_id:<16} {txn.trans_type:<14} ₹{txn.amount:<11} ₹{txn.balance_after:<13} {txn.timestamp:<20}"
            )
            if txn.description:
                print(f"    └─ Note: {txn.description}")
    print("=" * 80)


def handle_sort_accounts(bank_list: BankLinkedList) -> None:
    """Workflow to sort accounts using linked-list merge sort."""
    if bank_list.head is None or bank_list.head.next is None:
        print("\n[!] The list has fewer than 2 accounts. Sorting is not necessary.")
        return

    print("\n--- SORT ACCOUNTS (LINKED LIST MERGE SORT) ---")
    print("  1. By Balance (Ascending: Lowest to Highest)")
    print("  2. By Balance (Descending: Highest to Lowest)")
    print("  3. By Customer Name (A-Z)")
    print("  4. By Customer Name (Z-A)")
    print("  5. By Account Number (Ascending)")

    choice = input("Select sort option [1-5]: ").strip()
    if choice == "1":
        merge_sort_accounts(bank_list, key="balance", reverse=False)
        print("[Success] Accounts sorted by Balance (Ascending) using Linked List Merge Sort.")
    elif choice == "2":
        merge_sort_accounts(bank_list, key="balance", reverse=True)
        print("[Success] Accounts sorted by Balance (Descending) using Linked List Merge Sort.")
    elif choice == "3":
        merge_sort_accounts(bank_list, key="name", reverse=False)
        print("[Success] Accounts sorted by Customer Name (A to Z) using Linked List Merge Sort.")
    elif choice == "4":
        merge_sort_accounts(bank_list, key="name", reverse=True)
        print("[Success] Accounts sorted by Customer Name (Z to A) using Linked List Merge Sort.")
    elif choice == "5":
        merge_sort_accounts(bank_list, key="account_no", reverse=False)
        print("[Success] Accounts sorted by Account Number (Ascending) using Linked List Merge Sort.")
    else:
        print("[Error] Invalid sort selection. Sorting cancelled.")
        return

    # Automatically display sorted results
    display_all_accounts_view(bank_list)


def handle_bank_summary(service: AccountService) -> None:
    """Display overall bank metrics."""
    summary = service.get_summary()
    print("\n" + "=" * 50)
    print("               BANK SUMMARY")
    print("=" * 50)
    print(f"  Total Accounts Registered : {summary['total_accounts']}")
    print(f"  Total Deposits / Balance  : ₹{summary['total_balance']}")

    highest = summary["highest_account"]
    if highest:
        print(f"  Highest Balance Account   : #{highest.account_no} ({highest.name}) with ₹{highest.balance}")
    else:
        print("  Highest Balance Account   : None (Bank is empty)")

    bank_list = service.bank_list
    head_info = f"#{bank_list.head.account_no} ({bank_list.head.name})" if bank_list.head else "NULL"
    tail_info = f"#{bank_list.tail.account_no} ({bank_list.tail.name})" if bank_list.tail else "NULL"
    print(f"  Linked List HEAD Pointer  : {head_info}")
    print(f"  Linked List TAIL Pointer  : {tail_info}")
    print("=" * 50)


def main() -> None:
    """Main execution loop for BankLink CLI."""
    print_banner()

    # Step 1: Load accounts from JSON storage at startup
    bank_list, load_msg = load_accounts(DEFAULT_STORAGE_FILE)
    print(f"[*] {load_msg}")

    service = AccountService(bank_list=bank_list, auto_save=True)

    while True:
        try:
            print_menu()
            choice = input("Enter your choice (1-12): ").strip()

            if choice == "1":
                handle_create_account(service)
            elif choice == "2":
                display_all_accounts_view(bank_list)
            elif choice == "3":
                handle_search_account(service)
            elif choice == "4":
                handle_deposit(service)
            elif choice == "5":
                handle_withdraw(service)
            elif choice == "6":
                handle_transfer(service)
            elif choice == "7":
                handle_delete_account(service)
            elif choice == "8":
                handle_transaction_history(service)
            elif choice == "9":
                handle_sort_accounts(bank_list)
            elif choice == "10":
                print_visualization(bank_list)
            elif choice == "11":
                handle_bank_summary(service)
            elif choice == "12":
                # Safe exit and explicit save
                success, msg = save_accounts(bank_list)
                print(f"[*] {msg}")
                print("\nThank you for using BankLink! Goodbye.\n")
                break
            else:
                print(f"[Error] Invalid option '{choice}'. Please select a number from 1 to 12.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] Session interrupted. Saving data safely before exit...")
            save_accounts(bank_list)
            print("[*] BankLink terminated safely. Goodbye.")
            break
        except Exception as e:
            print(f"[Unexpected Error] {e}")


if __name__ == "__main__":
    main()
