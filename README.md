# BankLink: Bank Account Management System

> **Educational Data Structures & Algorithms (DSA) Simulation**  
> Built in Python 3 using a **Custom Singly Linked List** with Head & Tail Pointers.

---

## 1. Project Overview

**BankLink** is an educational, terminal-based banking simulation designed to demonstrate the real-world application of **fundamental Data Structures and Algorithms (DSA)**.

Instead of relying on built-in Python lists, dictionaries, databases, or third-party ORMs for runtime state, **all active account records and transaction histories are strictly stored and manipulated using custom singly linked lists**.

### Key Highlights
- **Strict DSA Foundation:** Custom `AccountNode`, `BankLinkedList`, `TransactionNode`, and `TransactionLinkedList`.
- **$O(1)$ Insertion:** Tail pointer guarantees constant-time insertion after a linear uniqueness check.
- **Robust Pointer Updates:** Comprehensive handling of edge cases (empty list, single node, deleting head, deleting tail, and deleting middle nodes).
- **Linked-List Merge Sort:** Implements $O(n \log n)$ merge sort directly on node pointers without converting accounts to a Python list.
- **Accurate Currency Arithmetic:** Uses Python's standard `decimal.Decimal` to prevent floating-point round-off errors.
- **Atomic Money Transfers:** Transfers validate both accounts and balances before altering any funds; failure leaves all balances unchanged.
- **Terminal Visualizer:** Displays ASCII diagram of nodes and pointers (`HEAD -> [101: Asha] -> [102: Ravi] -> NULL`).
- **JSON Persistence:** Automatically saves and loads records without altering the runtime linked-list structure.

---

## 2. Project File Structure

```text
BankLink/
├── main.py               # Application entry point & interactive terminal menu loop
├── account.py            # AccountNode class definition & data attributes
├── linked_list.py        # BankLinkedList class with head/tail pointers and CRUD methods
├── account_service.py    # Banking business rules, validations, and transfer orchestration
├── transactions.py       # TransactionNode & TransactionLinkedList per-account history
├── sorting.py            # In-place Merge Sort operating directly on node pointers
├── visualizer.py         # ASCII diagram generator illustrating linked list structure
├── storage.py            # JSON persistence layer with graceful corrupt/missing file handling
├── tests.py              # 23 unit tests verifying all DSA operations and banking invariants
├── ARCHITECTURE.md       # Detailed technical design document
├── README.md             # Complete user guide, complexity analysis, and documentation
└── data/
    └── accounts.json     # Saved accounts and transaction records (auto-created)
```

---

## 3. Setup and How to Run

BankLink requires **Python 3.10+** and uses **only Python standard-library modules** (no `pip install` required).

### Prerequisites
Make sure Python 3 is installed. Verify with:
```bash
python --version
# or on Windows:
py -3 --version
```

### Running the Application
From the `BankLink` directory, launch the terminal menu:
```bash
# Windows (PowerShell / Command Prompt)
py -3 main.py

# macOS / Linux
python3 main.py
```

### Running the Test Suite
To run all 23 unit tests:
```bash
# Windows
py -3 tests.py

# macOS / Linux
python3 tests.py
```

---

## 4. Menu Guide

When you launch `main.py`, you will be greeted by the 12-item operations menu:

```text
==================================================
              MAIN OPERATIONS MENU
==================================================
  1. Create Account
  2. Display All Accounts
  3. Search Account
  4. Deposit Money
  5. Withdraw Money
  6. Transfer Money
  7. Delete Account
  8. View Transaction History
  9. Sort Accounts (Merge Sort on Linked List)
 10. Visualize Linked List Structure
 11. Show Bank Summary
 12. Save and Exit
==================================================
Enter your choice (1-12):
```

| # | Option | Description |
|---|---|---|
| **1** | **Create Account** | Validates account number uniqueness via linear traversal, ensures non-negative balance, and appends the new node at `tail` in $O(1)$. |
| **2** | **Display All Accounts** | Traverses from `head` to `tail` and prints a formatted tabular view with tags marking `[HEAD]` and `[TAIL]`. |
| **3** | **Search Account** | Performs linear search $O(n)$ by account number and displays node details and next pointer reference. |
| **4** | **Deposit Money** | Validates positive amount, increments balance, and appends a `Deposit` node to the account's transaction history list. |
| **5** | **Withdraw Money** | Validates positive amount, prevents overdrafts, decrements balance, and records a `Withdrawal` transaction node. |
| **6** | **Transfer Money** | Atomically validates sender, recipient, and funds before transferring. Credits recipient, debits sender, and logs paired transactions. |
| **7** | **Delete Account** | Asks for explicit confirmation (`y/n`), removes the target node, and updates `head` and `tail` pointers accordingly. |
| **8** | **View Transaction History** | Traverses the account's custom `TransactionLinkedList` and displays its passbook statement. |
| **9** | **Sort Accounts** | Runs linked-list Merge Sort on node pointers by Balance, Name, or Account Number. |
| **10** | **Visualize Linked List** | Renders an ASCII diagram: `HEAD -> [Node A] -> [Node B] -> NULL` with pointer indicators. |
| **11** | **Show Bank Summary** | Displays total active accounts, total balance, highest balance account, and head/tail status. |
| **12** | **Save and Exit** | Persists current linked-list state to `data/accounts.json` and terminates cleanly. |

---

## 5. Data Structures & Algorithm Design

### 5.1 AccountNode (`account.py`)
Each customer account is encapsulated inside an `AccountNode`:
```python
class AccountNode:
    def __init__(self, account_no, name, account_type, balance):
        self.account_no = account_no            # Unique ID (e.g. '101')
        self.name = name                        # Customer Name
        self.account_type = account_type        # 'Savings' or 'Current'
        self.balance = balance                  # Decimal('5000.00')
        self.next = None                        # Pointer to next AccountNode
        self.transactions = TransactionLinkedList() # Head of transaction history list
```

### 5.2 BankLinkedList (`linked_list.py`)
Manages the collection of accounts using `head` and `tail` references:
- **`head`**: Points to the first node in the sequence (`None` when empty).
- **`tail`**: Points to the final node in the sequence (`None` when empty).
- **`size`**: Tracks active account count in $O(1)$.

#### Insertion at Tail in $O(1)$
```python
def insert_node(self, node: AccountNode) -> None:
    node.next = None
    if self.head is None:
        self.head = node
        self.tail = node
    else:
        self.tail.next = node
        self.tail = node
    self.size += 1
```

#### Pointer Updates on Deletion
BankLink carefully handles all five deletion scenarios:
1. **Empty list:** Returns failure gracefully without raising exceptions.
2. **Only node (`curr == head and curr == tail`):** Sets `head = None`, `tail = None`, `size = 0`.
3. **Head node (`curr == head`):** Advances `head = head.next`, detaches old head (`curr.next = None`).
4. **Tail node (`curr == tail`):** Links predecessor `prev.next = None`, updates `tail = prev`.
5. **Middle node:** Relinks predecessor around target: `prev.next = curr.next`, detaches `curr.next = None`.

### 5.3 Linked-List Merge Sort (`sorting.py`)
Unlike arrays, singly linked lists cannot be indexed in $O(1)$, making algorithms like Quicksort less natural. **Merge Sort** is the optimal $O(n \log n)$ sorting algorithm for linked lists because:
1. It does not require random access.
2. Splitting takes $O(n)$ using the **Slow and Fast (Tortoise and Hare)** pointer technique.
3. Merging requires only relinking existing pointer references (`.next`), allocating **zero extra node objects** ($O(1)$ auxiliary memory).

```text
[101: 5000] ──> [102: 1200] ──> [103: 8900] ──> [104: 300]
                     │ Split via Slow/Fast pointers
         ┌───────────┴───────────┐
[101: 5000] ──> [102: 1200]   [103: 8900] ──> [104: 300]
         │ Recursively sort      │ Recursively sort
[102: 1200] ──> [101: 5000]   [104: 300] ──> [103: 8900]
         └───────────┬───────────┘
                     │ Merge by comparing and relinking pointers
[104: 300] ──> [102: 1200] ──> [101: 5000] ──> [103: 8900]
```

### 5.4 Transaction History Linked List (`transactions.py`)
Each `AccountNode` references its own `TransactionLinkedList`. Every deposit, withdrawal, and transfer appends a `TransactionNode` in $O(1)$ time, forming an immutable audit trail.

---

## 6. Time and Space Complexity Analysis

Let $n$ be the number of active account nodes in the bank.

| Operation | Time Complexity | Auxiliary Space | Explanation / Rationale |
|---|:---:|:---:|---|
| **Insert at Tail** | $O(1)$ | $O(1)$ | Tail pointer enables direct constant-time appending. |
| **Create Account** | $O(n)$ | $O(1)$ | Linear uniqueness check dominates the $O(1)$ insertion. |
| **Search Account** | $O(n)$ | $O(1)$ | Must linearly traverse from `head` through `next` pointers. |
| **Display Accounts** | $O(n)$ | $O(1)$ | Traverses all $n$ nodes sequentially. |
| **Delete Account** | $O(n)$ | $O(1)$ | $O(n)$ search to locate predecessor; $O(1)$ pointer relinking. |
| **Deposit / Withdraw** | $O(n)$ | $O(1)$ | $O(n)$ account lookup + $O(1)$ balance and history update. |
| **Transfer Funds** | $O(n)$ | $O(1)$ | Two sequential linear searches + $O(1)$ atomic updates. |
| **Bank Summary** | $O(n)$ | $O(1)$ | Single pass over nodes to sum balances and find max balance. |
| **Merge Sort** | $O(n \log n)$ | $O(\log n)$ | Divide-and-conquer recursion stack; no extra node allocation. |

---

## 7. Currency Precision: Why `Decimal` instead of `float`

In standard binary floating-point arithmetic (IEEE 754 `float`), base-10 fractional values cannot be represented exactly:
```python
# Standard float error:
0.1 + 0.2  # => 0.30000000000000004
```
In banking systems, such accumulation causes balance drift, broken equality checks, and auditing discrepancies.

**BankLink strictly uses `decimal.Decimal`** with a fixed two-decimal quantizer (`0.01`):
```python
from decimal import Decimal
balance = Decimal("1000.50").quantize(Decimal("0.01"))
```
This guarantees 100% exact currency arithmetic throughout deposits, withdrawals, transfers, and JSON serialization.

---

## 8. Example Terminal Run

### 1. Creating Accounts
```text
Enter your choice (1-12): 1
--- CREATE NEW ACCOUNT ---
Enter unique Account Number (e.g. 101, ACC1001): 101
Enter Customer Name: Asha Sharma
Select Account Type [1/2, default 1]: 1
Enter Opening Balance (₹, min 0.00): 5000.00
[Success] Account #101 created successfully for Asha Sharma.
```

### 2. Visualizing the Linked List
```text
Enter your choice (1-12): 10
┌─────────────────────────────────────────────────────────────────────────┐
│                      LINKED LIST STRUCTURAL DIAGRAM                     │
└─────────────────────────────────────────────────────────────────────────┘

HEAD ──> [101: Asha Sharma (₹5000.00)] ──> [102: Ravi Kumar (₹12500.50)] ──> NULL

POINTER METADATA:
  • HEAD points to: Node #101 (Asha Sharma)
  • TAIL points to: Node #102 (Ravi Kumar)
  • Total active nodes (size): 2

NODE DETAIL MAP:
  Index  Account No   Holder Name        Balance        Next Node Pointer   
  ────────────────────────────────────────────────────────────────────────
  [0  ]  101          Asha Sharma        ₹5000.00        Node #102 [HEAD]
  [1  ]  102          Ravi Kumar         ₹12500.50       NULL (End of List) [TAIL]
```

### 3. Atomic Transfer
```text
Enter your choice (1-12): 6
--- TRANSFER FUNDS ---
Enter Sender Account Number: 101
Sender: Asha Sharma (Available Balance: ₹5000.00)
Enter Recipient Account Number: 102
Recipient: Ravi Kumar
Enter Transfer Amount (₹): 1500.00
Enter Reference / Note [Optional]: Freelance fee
[Success] Successfully transferred ₹1500.00 from #101 (Asha Sharma) to #102 (Ravi Kumar).
```

### 4. Passbook Transaction Statement
```text
Enter your choice (1-12): 8
--- TRANSACTION HISTORY ---
Enter Account Number: 101
================================================================================
  PASSBOOK HISTORY FOR: #101 (Asha Sharma)
  Account Type: Savings | Current Balance: ₹3500.00
================================================================================
  Txn ID           Type           Amount       Balance After  Date/Time           
  ----------------------------------------------------------------------------
  TXN-INIT         Opening        ₹5000.00     ₹5000.00       2026-10-13 13:14:00 
    └─ Note: Account opening balance
  TXN-TRF-OUT-501  Transfer Out   ₹1500.00     ₹3500.00       2026-10-13 13:17:22 
    └─ Note: Transfer (Freelance fee) to #102 (Ravi Kumar)
================================================================================
```

---

## 9. Educational Limitations

> [!WARNING]
> BankLink is engineered as an **educational DSA demonstration**, not for production financial use.

- **Security & Authentication:** There are no passwords, encryption, biometric authentication, or role-based access control.
- **Concurrency & Locking:** There is no thread locking or distributed transaction isolation (ACID database transactions).
- **Storage Scalability:** Singly linked lists require $O(n)$ search time. Production banks rely on B+ Trees, clustered primary keys, and relational/distributed databases for sub-millisecond lookups.

---

## 10. Verification & Test Results

The test suite in `tests.py` validates all functionality across 23 unit tests:
- **Linked List Pointer Mechanics:** Head/tail updates, empty list, single node, middle node, and tail node deletions.
- **Business Rules:** Rejection of duplicates, negative amounts, overdraft attempts, and self-transfers.
- **Sorting:** Linked list merge sort on balance and customer name.
- **Persistence:** JSON round-trip serialization and recovery from missing or corrupted data files.

Run:
```bash
py -3 tests.py
```
Output:
```text
.......................
----------------------------------------------------------------------
Ran 23 tests in 0.078s

OK
```
