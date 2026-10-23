"""
tests.py - Comprehensive Unit Tests for BankLink

Tests all linked list operations, pointer manipulation, edge cases,
banking business rules, merge sort, transactions, and JSON storage.
"""

import unittest
import os
import tempfile
import json
from decimal import Decimal

from linked_list import BankLinkedList
from account import AccountNode
from transactions import TransactionLinkedList, TransactionNode
from account_service import AccountService
from sorting import merge_sort_accounts
from storage import save_accounts, load_accounts
from visualizer import render_linked_list


class TestBankLinkedList(unittest.TestCase):
    """Tests for BankLinkedList data structure and pointer updates."""

    def setUp(self) -> None:
        self.bank_list = BankLinkedList()

    def test_empty_list_state(self) -> None:
        """Verify initial state of an empty linked list."""
        self.assertIsNone(self.bank_list.head)
        self.assertIsNone(self.bank_list.tail)
        self.assertEqual(self.bank_list.size, 0)
        self.assertTrue(self.bank_list.is_empty())
        self.assertEqual(self.bank_list.get_total_balance(), Decimal("0.00"))
        self.assertIsNone(self.bank_list.get_highest_balance_account())
        self.assertIsNone(self.bank_list.search_account("101"))

        # Deleting from empty list should fail gracefully
        success, msg = self.bank_list.delete_account("101")
        self.assertFalse(success)
        self.assertIn("no accounts", msg.lower())

    def test_insert_single_node(self) -> None:
        """Verify inserting the first node sets both head and tail."""
        success, msg, node = self.bank_list.insert_account("101", "Asha Sharma", "Savings", Decimal("5000.00"))
        self.assertTrue(success)
        self.assertIsNotNone(node)
        self.assertEqual(self.bank_list.size, 1)
        self.assertEqual(self.bank_list.head, node)
        self.assertEqual(self.bank_list.tail, node)
        self.assertIsNone(node.next)
        self.assertEqual(node.balance, Decimal("5000.00"))
        self.assertEqual(len(node.transactions), 1)

    def test_insert_multiple_nodes_and_order(self) -> None:
        """Verify insertion maintains correct order and tail pointer."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        self.bank_list.insert_account("102", "Ravi", "Current", "2000")
        self.bank_list.insert_account("103", "Kavita", "Savings", "3000")

        self.assertEqual(self.bank_list.size, 3)
        self.assertEqual(self.bank_list.head.account_no, "101")
        self.assertEqual(self.bank_list.head.next.account_no, "102")
        self.assertEqual(self.bank_list.head.next.next.account_no, "103")
        self.assertEqual(self.bank_list.tail.account_no, "103")
        self.assertIsNone(self.bank_list.tail.next)

    def test_reject_duplicate_account_number(self) -> None:
        """Verify uniqueness enforcement via linear search."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        success, msg, node = self.bank_list.insert_account("101", "Duplicate Asha", "Current", "5000")
        self.assertFalse(success)
        self.assertIsNone(node)
        self.assertIn("already exists", msg.lower())
        self.assertEqual(self.bank_list.size, 1)

    def test_search_account(self) -> None:
        """Verify linear search finds existing node and returns None for missing."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        self.bank_list.insert_account("102", "Ravi", "Current", "2000")

        found = self.bank_list.search_account("102")
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Ravi")

        # Case-insensitive lookup
        found_case = self.bank_list.search_account("102")
        self.assertIsNotNone(found_case)

        # Missing lookup
        missing = self.bank_list.search_account("999")
        self.assertIsNone(missing)

    def test_delete_only_node(self) -> None:
        """Verify deleting the single node clears head and tail."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        success, msg = self.bank_list.delete_account("101")
        self.assertTrue(success)
        self.assertIsNone(self.bank_list.head)
        self.assertIsNone(self.bank_list.tail)
        self.assertEqual(self.bank_list.size, 0)
        self.assertTrue(self.bank_list.is_empty())

    def test_delete_head_node(self) -> None:
        """Verify deleting the head node updates head to the next node."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        self.bank_list.insert_account("102", "Ravi", "Current", "2000")
        self.bank_list.insert_account("103", "Kavita", "Savings", "3000")

        success, msg = self.bank_list.delete_account("101")
        self.assertTrue(success)
        self.assertEqual(self.bank_list.size, 2)
        self.assertEqual(self.bank_list.head.account_no, "102")
        self.assertEqual(self.bank_list.tail.account_no, "103")

    def test_delete_tail_node(self) -> None:
        """Verify deleting the tail node updates tail to the previous node."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        self.bank_list.insert_account("102", "Ravi", "Current", "2000")
        self.bank_list.insert_account("103", "Kavita", "Savings", "3000")

        success, msg = self.bank_list.delete_account("103")
        self.assertTrue(success)
        self.assertEqual(self.bank_list.size, 2)
        self.assertEqual(self.bank_list.head.account_no, "101")
        self.assertEqual(self.bank_list.tail.account_no, "102")
        self.assertIsNone(self.bank_list.tail.next)

    def test_delete_middle_node(self) -> None:
        """Verify deleting a middle node bypasses it correctly."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        self.bank_list.insert_account("102", "Ravi", "Current", "2000")
        self.bank_list.insert_account("103", "Kavita", "Savings", "3000")

        success, msg = self.bank_list.delete_account("102")
        self.assertTrue(success)
        self.assertEqual(self.bank_list.size, 2)
        self.assertEqual(self.bank_list.head.account_no, "101")
        self.assertEqual(self.bank_list.head.next.account_no, "103")
        self.assertEqual(self.bank_list.tail.account_no, "103")

    def test_delete_non_existent_node(self) -> None:
        """Verify attempting to delete a non-existent account returns False."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000")
        success, msg = self.bank_list.delete_account("999")
        self.assertFalse(success)
        self.assertEqual(self.bank_list.size, 1)
        self.assertEqual(self.bank_list.head.account_no, "101")

    def test_total_balance_and_highest(self) -> None:
        """Verify calculation of total balance and maximum balance node."""
        self.bank_list.insert_account("101", "Asha", "Savings", "1000.50")
        self.bank_list.insert_account("102", "Ravi", "Current", "5500.25")
        self.bank_list.insert_account("103", "Kavita", "Savings", "2400.00")

        self.assertEqual(self.bank_list.get_total_balance(), Decimal("8900.75"))
        highest = self.bank_list.get_highest_balance_account()
        self.assertIsNotNone(highest)
        self.assertEqual(highest.account_no, "102")
        self.assertEqual(highest.balance, Decimal("5500.25"))


class TestAccountService(unittest.TestCase):
    """Tests for banking business rules, deposits, withdrawals, and transfers."""

    def setUp(self) -> None:
        self.bank_list = BankLinkedList()
        self.service = AccountService(self.bank_list, auto_save=False)
        self.service.create_account("101", "Asha", "Savings", "1000.00")
        self.service.create_account("102", "Ravi", "Current", "500.00")

    def test_deposit_valid_and_invalid(self) -> None:
        """Verify deposits update balances correctly and reject invalid inputs."""
        # Valid deposit
        ok, msg, node = self.service.deposit("101", "250.50", "Bonus")
        self.assertTrue(ok)
        self.assertEqual(node.balance, Decimal("1250.50"))

        # Zero deposit rejected
        ok, msg, _ = self.service.deposit("101", "0")
        self.assertFalse(ok)

        # Negative deposit rejected
        ok, msg, _ = self.service.deposit("101", "-50")
        self.assertFalse(ok)

        # Non-numeric input rejected
        ok, msg, _ = self.service.deposit("101", "abc")
        self.assertFalse(ok)

        # Non-existent account
        ok, msg, _ = self.service.deposit("999", "100")
        self.assertFalse(ok)

    def test_withdraw_valid_and_overdraft(self) -> None:
        """Verify withdrawal safety and overdraft prevention."""
        # Valid withdrawal
        ok, msg, node = self.service.withdraw("101", "400.00")
        self.assertTrue(ok)
        self.assertEqual(node.balance, Decimal("600.00"))

        # Overdraft attempt rejected without changing balance
        ok, msg, _ = self.service.withdraw("101", "900.00")
        self.assertFalse(ok)
        self.assertIn("insufficient funds", msg.lower())
        self.assertEqual(node.balance, Decimal("600.00"))

        # Negative withdrawal rejected
        ok, msg, _ = self.service.withdraw("101", "-100")
        self.assertFalse(ok)
        self.assertEqual(node.balance, Decimal("600.00"))

    def test_transfer_atomic_success(self) -> None:
        """Verify transfer debits sender, credits recipient, and logs history."""
        ok, msg = self.service.transfer("101", "102", "300.00", "Rent Payment")
        self.assertTrue(ok)

        sender = self.service.search_account("101")
        recipient = self.service.search_account("102")

        self.assertEqual(sender.balance, Decimal("700.00"))
        self.assertEqual(recipient.balance, Decimal("800.00"))

        # Check transaction history recorded on both
        sender_last_tx = list(sender.transactions)[-1]
        recipient_last_tx = list(recipient.transactions)[-1]

        self.assertEqual(sender_last_tx.trans_type, "Transfer Out")
        self.assertEqual(sender_last_tx.amount, Decimal("300.00"))
        self.assertEqual(recipient_last_tx.trans_type, "Transfer In")
        self.assertEqual(recipient_last_tx.amount, Decimal("300.00"))

    def test_transfer_failure_preserves_balances(self) -> None:
        """Verify failed transfers do not alter either balance."""
        # Insufficient funds
        ok, msg = self.service.transfer("102", "101", "10000.00")
        self.assertFalse(ok)

        # Balances must be untouched
        self.assertEqual(self.service.search_account("101").balance, Decimal("1000.00"))
        self.assertEqual(self.service.search_account("102").balance, Decimal("500.00"))

        # Transfer to self
        ok, msg = self.service.transfer("101", "101", "100.00")
        self.assertFalse(ok)

        # Transfer to non-existent recipient
        ok, msg = self.service.transfer("101", "999", "100.00")
        self.assertFalse(ok)

        # Negative amount
        ok, msg = self.service.transfer("101", "102", "-50.00")
        self.assertFalse(ok)


    def test_invalid_account_creation(self) -> None:
        """Verify account creation input validation."""
        # Empty name
        ok, msg, _ = self.service.create_account("103", "", "Savings", "100")
        self.assertFalse(ok)

        # Invalid type
        ok, msg, _ = self.service.create_account("103", "John", "Investment", "100")
        self.assertFalse(ok)

        # Negative balance
        ok, msg, _ = self.service.create_account("103", "John", "Savings", "-100")
        self.assertFalse(ok)


class TestSorting(unittest.TestCase):
    """Tests for Merge Sort directly on linked list nodes."""

    def test_merge_sort_by_balance(self) -> None:
        """Verify sorting by balance in ascending and descending orders."""
        bank_list = BankLinkedList()
        bank_list.insert_account("101", "Asha", "Savings", "5000.00")
        bank_list.insert_account("102", "Ravi", "Current", "1200.00")
        bank_list.insert_account("103", "Kavita", "Savings", "8900.00")
        bank_list.insert_account("104", "Deepak", "Savings", "300.00")

        # Ascending balance
        merge_sort_accounts(bank_list, key="balance", reverse=False)
        balances = [node.balance for node in bank_list]
        self.assertEqual(balances, [Decimal("300.00"), Decimal("1200.00"), Decimal("5000.00"), Decimal("8900.00")])
        self.assertEqual(bank_list.head.account_no, "104")
        self.assertEqual(bank_list.tail.account_no, "103")
        self.assertEqual(bank_list.size, 4)

        # Descending balance
        merge_sort_accounts(bank_list, key="balance", reverse=True)
        balances_desc = [node.balance for node in bank_list]
        self.assertEqual(balances_desc, [Decimal("8900.00"), Decimal("5000.00"), Decimal("1200.00"), Decimal("300.00")])
        self.assertEqual(bank_list.head.account_no, "103")
        self.assertEqual(bank_list.tail.account_no, "104")

    def test_merge_sort_by_name(self) -> None:
        """Verify alphabetical sorting by customer name."""
        bank_list = BankLinkedList()
        bank_list.insert_account("101", "Zara", "Savings", "100")
        bank_list.insert_account("102", "Aman", "Savings", "200")
        bank_list.insert_account("103", "Mira", "Current", "300")

        merge_sort_accounts(bank_list, key="name", reverse=False)
        names = [node.name for node in bank_list]
        self.assertEqual(names, ["Aman", "Mira", "Zara"])
        self.assertEqual(bank_list.head.name, "Aman")
        self.assertEqual(bank_list.tail.name, "Zara")

    def test_sort_single_and_empty(self) -> None:
        """Verify sorting handles edge cases of 0 and 1 elements without errors."""
        empty_list = BankLinkedList()
        merge_sort_accounts(empty_list)
        self.assertIsNone(empty_list.head)
        self.assertEqual(empty_list.size, 0)

        single_list = BankLinkedList()
        single_list.insert_account("101", "Asha", "Savings", "100")
        merge_sort_accounts(single_list)
        self.assertEqual(single_list.head.account_no, "101")
        self.assertEqual(single_list.tail.account_no, "101")
        self.assertEqual(single_list.size, 1)


class TestStorage(unittest.TestCase):
    """Tests for saving and loading linked lists to JSON."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "accounts.json")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_save_and_load_roundtrip(self) -> None:
        """Verify complete serialization and restoration of linked list."""
        original = BankLinkedList()
        original.insert_account("101", "Asha", "Savings", "1500.75")
        original.insert_account("102", "Ravi", "Current", "3200.50")

        # Add transaction
        node = original.search_account("101")
        node.transactions.append("TXN999", "Deposit", Decimal("500.00"), Decimal("2000.75"), "Cheque Deposit")

        # Save
        saved, msg = save_accounts(original, self.file_path)
        self.assertTrue(saved)
        self.assertTrue(os.path.exists(self.file_path))

        # Load
        loaded, load_msg = load_accounts(self.file_path)
        self.assertEqual(loaded.size, 2)
        self.assertEqual(loaded.head.account_no, "101")
        self.assertEqual(loaded.tail.account_no, "102")
        self.assertEqual(loaded.head.balance, Decimal("1500.75"))

        # Verify transaction history preserved
        loaded_node = loaded.search_account("101")
        txns = list(loaded_node.transactions)
        self.assertEqual(len(txns), 2)  # Opening + TXN999
        self.assertEqual(txns[1].trans_id, "TXN999")
        self.assertEqual(txns[1].amount, Decimal("500.00"))

    def test_missing_file(self) -> None:
        """Verify missing file does not raise exceptions."""
        non_existent = os.path.join(self.temp_dir.name, "does_not_exist.json")
        loaded, msg = load_accounts(non_existent)
        self.assertEqual(loaded.size, 0)
        self.assertIsNone(loaded.head)

    def test_corrupt_file(self) -> None:
        """Verify corrupted JSON is handled safely without crashing."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON DATA ---")

        loaded, msg = load_accounts(self.file_path)
        self.assertEqual(loaded.size, 0)
        self.assertIsNone(loaded.head)


class TestVisualizer(unittest.TestCase):
    """Tests for terminal ASCII visualizer."""

    def test_visualizer_output(self) -> None:
        """Verify visualizer output formatting."""
        bank_list = BankLinkedList()
        # Empty representation
        empty_str = render_linked_list(bank_list)
        self.assertIn("HEAD ──> NULL", empty_str)

        # Populated representation
        bank_list.insert_account("101", "Asha", "Savings", "1000.00")
        bank_list.insert_account("102", "Ravi", "Current", "2000.00")
        vis_str = render_linked_list(bank_list)

        self.assertIn("101: Asha", vis_str)
        self.assertIn("102: Ravi", vis_str)
        self.assertIn("HEAD points to: Node #101", vis_str)
        self.assertIn("TAIL points to: Node #102", vis_str)


if __name__ == "__main__":
    unittest.main()
