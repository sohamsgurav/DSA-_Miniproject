"""
account_service.py - Banking Business Logic and Rules Engine for BankLink

Coordinates banking operations, input validation, balance safety,
and updates to the underlying BankLinkedList and Transaction history.
"""

from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple, Dict, Any
import time

from linked_list import BankLinkedList
from account import AccountNode
from storage import save_accounts


class AccountService:
    """
    Coordinates banking operations on the BankLinkedList.
    Enforces all business rules and transaction safety invariants.
    """

    def __init__(self, bank_list: BankLinkedList, auto_save: bool = True) -> None:
        self.bank_list: BankLinkedList = bank_list
        self.auto_save: bool = auto_save

    def _trigger_save_if_enabled(self) -> None:
        """Helper to persist changes to disk if auto_save is enabled."""
        if self.auto_save:
            save_accounts(self.bank_list)

    @staticmethod
    def parse_amount(amount_input: Any) -> Tuple[bool, Decimal, str]:
        """
        Safely parse and validate a monetary input into a positive Decimal.
        Disallows negative, zero, or non-numeric values.
        """
        try:
            val = Decimal(str(amount_input).strip())
            quantized = val.quantize(Decimal("0.01"))
            if quantized <= Decimal("0.00"):
                return False, Decimal("0.00"), "Amount must be strictly greater than zero."
            return True, quantized, ""
        except (InvalidOperation, ValueError, TypeError):
            return False, Decimal("0.00"), "Invalid amount format. Please enter a valid number (e.g. 500 or 1500.50)."

    def create_account(
        self,
        account_no: str,
        name: str,
        account_type: str,
        opening_balance: Any,
    ) -> Tuple[bool, str, Optional[AccountNode]]:
        """
        Create a new bank account with validated inputs and non-negative balance.
        """
        # Validate balance format
        try:
            bal = Decimal(str(opening_balance).strip()).quantize(Decimal("0.01"))
            if bal < Decimal("0.00"):
                return False, "Opening balance cannot be negative.", None
        except Exception:
            return False, "Invalid opening balance. Must be a valid non-negative number.", None

        success, msg, node = self.bank_list.insert_account(
            account_no=account_no,
            name=name,
            account_type=account_type,
            balance=bal,
        )

        if success:
            self._trigger_save_if_enabled()

        return success, msg, node

    def search_account(self, account_no: str) -> Optional[AccountNode]:
        """Look up an account node by account number."""
        return self.bank_list.search_account(account_no)

    def deposit(
        self,
        account_no: str,
        amount_input: Any,
        description: str = "Cash Deposit",
    ) -> Tuple[bool, str, Optional[AccountNode]]:
        """
        Deposit funds into an existing account.
        Validates positive amount, updates balance, and appends transaction record.
        """
        node = self.search_account(account_no)
        if node is None:
            return False, f"Deposit failed: Account #{account_no} does not exist.", None

        valid, amount, err = self.parse_amount(amount_input)
        if not valid:
            return False, f"Deposit failed: {err}", node

        # Update balance
        node.balance += amount

        # Append transaction node
        txn_id = f"TXN-DEP-{int(time.time() * 1000) % 1000000}"
        node.transactions.append(
            trans_id=txn_id,
            trans_type="Deposit",
            amount=amount,
            balance_after=node.balance,
            description=description.strip() or "Cash Deposit",
        )

        self._trigger_save_if_enabled()
        return True, f"Successfully deposited ₹{amount} into Account #{node.account_no}. New balance: ₹{node.balance}.", node

    def withdraw(
        self,
        account_no: str,
        amount_input: Any,
        description: str = "Cash Withdrawal",
    ) -> Tuple[bool, str, Optional[AccountNode]]:
        """
        Withdraw funds from an existing account.
        Prevents overdrafts and negative amounts.
        """
        node = self.search_account(account_no)
        if node is None:
            return False, f"Withdrawal failed: Account #{account_no} does not exist.", None

        valid, amount, err = self.parse_amount(amount_input)
        if not valid:
            return False, f"Withdrawal failed: {err}", node

        # Overdraft check
        if node.balance < amount:
            return (
                False,
                f"Withdrawal failed: Insufficient funds. Available balance: ₹{node.balance}, requested: ₹{amount}.",
                node,
            )

        # Deduct balance
        node.balance -= amount

        # Append transaction node
        txn_id = f"TXN-WTH-{int(time.time() * 1000) % 1000000}"
        node.transactions.append(
            trans_id=txn_id,
            trans_type="Withdrawal",
            amount=amount,
            balance_after=node.balance,
            description=description.strip() or "Cash Withdrawal",
        )

        self._trigger_save_if_enabled()
        return True, f"Successfully withdrew ₹{amount} from Account #{node.account_no}. New balance: ₹{node.balance}.", node

    def transfer(
        self,
        sender_acc_no: str,
        recipient_acc_no: str,
        amount_input: Any,
        description: str = "",
    ) -> Tuple[bool, str]:
        """
        Transfer funds between two distinct accounts.
        Enforces atomic validation: both accounts must exist, amount must be positive,
        and sender must have sufficient balance before ANY balances are altered.
        """
        s_clean = str(sender_acc_no).strip()
        r_clean = str(recipient_acc_no).strip()

        if not s_clean or not r_clean:
            return False, "Transfer failed: Both sender and recipient account numbers are required."

        if s_clean.upper() == r_clean.upper():
            return False, "Transfer failed: Sender and recipient account cannot be the same."

        valid, amount, err = self.parse_amount(amount_input)
        if not valid:
            return False, f"Transfer failed: {err}"

        # 1. Search for sender
        sender = self.search_account(s_clean)
        if sender is None:
            return False, f"Transfer failed: Sender account #{s_clean} does not exist."

        # 2. Search for recipient
        recipient = self.search_account(r_clean)
        if recipient is None:
            return False, f"Transfer failed: Recipient account #{r_clean} does not exist."

        # 3. Check sender balance
        if sender.balance < amount:
            return (
                False,
                f"Transfer failed: Sender #{sender.account_no} has insufficient funds. Available: ₹{sender.balance}, needed: ₹{amount}.",
            )

        # 4. Atomic balance modification (only after all checks pass)
        sender.balance -= amount
        recipient.balance += amount

        # 5. Record dual transaction history nodes
        timestamp_now = int(time.time() * 1000) % 1000000
        desc_note = f"Transfer ({description.strip()})" if description.strip() else "Fund Transfer"

        sender.transactions.append(
            trans_id=f"TXN-TRF-OUT-{timestamp_now}",
            trans_type="Transfer Out",
            amount=amount,
            balance_after=sender.balance,
            description=f"{desc_note} to #{recipient.account_no} ({recipient.name})",
        )

        recipient.transactions.append(
            trans_id=f"TXN-TRF-IN-{timestamp_now}",
            trans_type="Transfer In",
            amount=amount,
            balance_after=recipient.balance,
            description=f"{desc_note} from #{sender.account_no} ({sender.name})",
        )

        self._trigger_save_if_enabled()
        return (
            True,
            f"Successfully transferred ₹{amount} from #{sender.account_no} ({sender.name}) to #{recipient.account_no} ({recipient.name}).",
        )

    def delete_account(self, account_no: str) -> Tuple[bool, str]:
        """Delete an account after validating existence."""
        success, msg = self.bank_list.delete_account(account_no)
        if success:
            self._trigger_save_if_enabled()
        return success, msg

    def get_summary(self) -> Dict[str, Any]:
        """Generate high-level banking statistics."""
        highest = self.bank_list.get_highest_balance_account()
        return {
            "total_accounts": self.bank_list.get_account_count(),
            "total_balance": self.bank_list.get_total_balance(),
            "highest_account": highest,
        }
