# BankLink — Bank Account Management System Using a Linked List

## 1. Project Overview

**Project name:** BankLink  
**Language:** Python 3  
**Interface:** Terminal / command-line interface  
**Core DSA:** Singly linked list  
**Project type:** Educational DSA mini-project

### Objective

Build a menu-driven banking simulation in which customer account records are stored and managed using a **custom singly linked list** rather than a Python list or database. The project demonstrates linked-list insertion, traversal, searching, deletion, pointer updates, sorting, and time-complexity analysis.

> This is an educational simulation, not a production banking system.

## 2. Architecture at a Glance

```text
                  ┌──────────────────────────┐
                  │       User / Terminal    │
                  └────────────┬─────────────┘
                               │
                  ┌────────────▼─────────────┐
                  │          main.py         │
                  │ Menu, input, output      │
                  └────────────┬─────────────┘
                               │
                  ┌────────────▼─────────────┐
                  │    account_service.py    │
                  │ Banking rules and checks│
                  └────────────┬─────────────┘
                               │
              ┌────────────────▼────────────────┐
              │          DSA Layer               │
              │                                  │
              │ linked_list.py                   │
              │ AccountNode + BankLinkedList     │
              │                                  │
              │ transactions.py                  │
              │ TransactionNode + history list   │
              │                                  │
              │ sorting.py                       │
              │ Merge sort on linked-list nodes  │
              └────────────────┬────────────────┘
                               │
                  ┌────────────▼─────────────┐
                  │        storage.py        │
                  │ JSON save/load           │
                  └────────────┬─────────────┘
                               │
                  ┌────────────▼─────────────┐
                  │         data/            │
                  │     accounts.json        │
                  └──────────────────────────┘

       visualizer.py prints the linked-list structure.
       tests.py verifies data structures and banking operations.
```

## 3. Folder and File Structure

```text
BankLink/
├── main.py
├── account.py
├── linked_list.py
├── account_service.py
├── transactions.py
├── storage.py
├── sorting.py
├── visualizer.py
├── tests.py
├── README.md
├── ARCHITECTURE.md
└── data/
    └── accounts.json
```

### File Responsibilities

| File | Responsibility |
|---|---|
| `main.py` | Application entry point, terminal menu, user input and output |
| `account.py` | Defines `AccountNode` and account fields |
| `linked_list.py` | Defines `BankLinkedList`; manages `head`, `tail`, insertion, search, deletion and traversal |
| `account_service.py` | Implements account creation, deposits, withdrawals, transfers and validation rules |
| `transactions.py` | Defines transaction nodes and per-account transaction history |
| `storage.py` | Saves data to JSON and reconstructs the linked list at startup |
| `sorting.py` | Implements merge sort directly on linked-list nodes |
| `visualizer.py` | Prints an ASCII representation of the linked list |
| `tests.py` | Tests linked-list operations, banking rules, sorting and persistence |
| `README.md` | Setup, usage, features, examples and complexity explanation |
| `ARCHITECTURE.md` | Project design and module responsibilities |
| `data/accounts.json` | Runtime persistence file; create it when needed |

## 4. Core Data Structures

### 4.1 Account Node

Each account is a node in the singly linked list.

Suggested fields:

- `account_no`: unique account identifier
- `name`: customer name
- `account_type`: e.g. Savings or Current
- `balance`: monetary amount stored using `Decimal` or integer paise
- `next`: reference to the next account node
- `transactions_head`: head of this account's transaction-history linked list

Example:

```python
class AccountNode:
    def __init__(self, account_no, name, account_type, balance):
        self.account_no = account_no
        self.name = name
        self.account_type = account_type
        self.balance = balance
        self.next = None
        self.transactions_head = None
```

### 4.2 Bank Linked List

The `BankLinkedList` class manages all account nodes.

Required state:

- `head`: first account node, or `None` when empty
- `tail`: last account node, or `None` when empty
- `size`: number of account nodes

Required methods:

- `insert_account(...)`
- `search_account(account_no)`
- `delete_account(account_no)`
- `display_accounts()`
- `get_account_count()`
- `get_total_balance()`
- traversal support for services and storage

**Important:** Maintain correct `head` and `tail` pointers when inserting or deleting nodes. The account-number uniqueness check requires a traversal unless a separate index is deliberately added. For this project's DSA focus, use linear search.

### 4.3 Transaction History Linked List

Each transaction node can store:

- transaction ID
- transaction type (deposit, withdrawal, transfer in, transfer out)
- amount
- note or description
- timestamp
- `next`

Keep transaction histories as linked lists too, so the project demonstrates linked-list use beyond account records.

## 5. Application Features

### Essential Features

1. Create a new account with a unique account number.
2. Display all account records.
3. Search by account number.
4. Deposit money.
5. Withdraw money, preventing overdrafts.
6. Transfer money between two existing accounts.
7. Delete an account after confirmation.
8. Display total account count and total balance.
9. Visualize the linked list in the terminal.
10. Save records and reload them when the application restarts.
11. Exit safely.

### Extra Features

1. Display transaction history for an account.
2. Sort accounts by customer name or balance using linked-list merge sort.
3. Display the account with the highest balance.
4. Compare selected operation timings for linked-list and Python-list implementations in a separate demonstration module, if time permits.

Complete the essential features before adding extras.

## 6. Terminal Menu

```text
========================================
       BANKLINK MANAGEMENT SYSTEM
========================================
1. Create Account
2. Display All Accounts
3. Search Account
4. Deposit Money
5. Withdraw Money
6. Transfer Money
7. Delete Account
8. View Transaction History
9. Sort Accounts
10. Visualize Linked List
11. Show Bank Summary
12. Save and Exit
========================================
Enter your choice:
```

## 7. Application Workflow

1. Start the program.
2. Load saved records from `data/accounts.json`, if the file exists.
3. Rebuild the runtime account linked list from the loaded records.
4. Display the menu.
5. Validate the user's menu choice and inputs.
6. Call the appropriate service method.
7. Update the linked list and transaction history after a successful operation.
8. Persist successful changes to the JSON file.
9. Return to the menu, or save and exit.

### Transfer Workflow

1. Find the sender account.
2. Find the recipient account.
3. Validate that both accounts exist and are different.
4. Validate that the transfer amount is positive and the sender has sufficient funds.
5. Only after all validations pass, debit the sender and credit the recipient.
6. Record matching transfer-out and transfer-in history entries.
7. Save the updated state.

Avoid partially applying a transfer if validation fails.

## 8. Data-Structure Rules

- The runtime source of truth for account records must be the custom `BankLinkedList`.
- Do **not** store the runtime accounts in a Python list, dictionary, database, or ORM.
- A temporary dictionary or list may be used when converting data for JSON serialization, but rebuild the linked list when loading.
- Implement merge sort on linked-list nodes without converting accounts to a Python list.
- Use Python standard-library modules only unless the instructor approves additional dependencies.
- Use integer paise or `Decimal` for balances; avoid `float` for money.
- This simulation does not provide real banking-grade authentication or security.

## 9. Input Validation and Edge Cases

The program should handle:

- duplicate account numbers
- empty names or invalid account types
- negative opening balances
- zero or negative deposit, withdrawal, or transfer amounts
- withdrawals or transfers exceeding available funds
- account numbers that do not exist
- transfer to the same account
- empty linked list
- deleting the head node
- deleting the tail node
- deleting the only node
- missing or malformed JSON file
- invalid menu choices and non-numeric input
- a restart after saved changes

## 10. Time Complexity

Let `n` be the number of accounts.

| Operation | Expected time complexity | Notes |
|---|---:|---|
| Insert at tail | `O(1)` | Assumes a tail pointer and that uniqueness has already been checked |
| Create unique account | `O(n)` | Linear uniqueness check dominates insertion |
| Search account | `O(n)` | Linear traversal |
| Display all accounts | `O(n)` | Visits every node |
| Delete account | `O(n)` | Must find the target and its predecessor |
| Deposit or withdraw | `O(n)` | Account search plus constant-time balance update |
| Transfer | `O(n)` | Two account searches; still linear overall |
| Total balance | `O(n)` | Visits every account |
| Merge sort | `O(n log n)` | Linked-list merge sort |

Space complexity for a linked list of `n` accounts is `O(n)`, with pointer overhead for each node. Merge sort on a linked list typically uses `O(log n)` recursion stack space when implemented recursively, excluding the existing nodes.

## 11. Testing Plan

Test at least the following:

- Insert into an empty list.
- Insert several accounts and verify order.
- Search for an existing and a missing account.
- Delete the head, middle, tail and only node.
- Verify `head`, `tail` and `size` after each deletion.
- Reject duplicate account numbers.
- Deposit valid and invalid amounts.
- Reject withdrawals that exceed the balance.
- Transfer successfully and reject invalid transfers without changing either balance.
- Sort accounts by name and balance.
- Save, restart and load records.
- Handle a missing or invalid JSON file gracefully.
- Verify transaction history for deposits, withdrawals and transfers.

## 12. Implementation Order

1. Create `account.py` and `linked_list.py`.
2. Write and run linked-list tests.
3. Implement `account_service.py` and transaction history.
4. Build the terminal menu in `main.py`.
5. Add `visualizer.py`.
6. Implement linked-list merge sort in `sorting.py`.
7. Add JSON persistence in `storage.py`.
8. Expand tests and complete `README.md`.
9. Run the complete test suite and fix failures before submission.

## 13. Definition of Done

The project is ready to demonstrate when:

- All account records are stored in the custom linked list at runtime.
- All essential banking operations work.
- Head and tail pointers remain correct after insertion and deletion.
- Invalid transactions are rejected without corrupting balances.
- Records survive a program restart through JSON persistence.
- Sorting operates on linked-list nodes.
- Tests pass.
- The README explains the architecture and Big-O complexity.
- The team can explain how the linked list works and why its performance differs from a Python list.

## 14. Instructions for Antigravity

Build this project in stages. Start with `account.py` and `linked_list.py`, add tests, and verify pointer handling before implementing the banking operations. Then implement transaction history, the terminal menu, sorting, visualization and JSON persistence. Run the tests after each stage, fix failures, and report the exact command needed to run the application.

Do not replace the custom linked list with a Python list or dictionary for runtime account storage.
