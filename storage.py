"""
storage.py - JSON Persistence Layer for BankLink

Provides saving and loading functionality for the BankLinkedList.
Uses Python's standard json module.
Temporary dictionaries and lists are used solely for JSON serialization,
while runtime account management strictly uses the custom BankLinkedList.
"""

import json
import os
from typing import Tuple
from linked_list import BankLinkedList
from account import AccountNode

DEFAULT_STORAGE_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.json")


def save_accounts(bank_list: BankLinkedList, file_path: str = DEFAULT_STORAGE_FILE) -> Tuple[bool, str]:
    """
    Serialize all accounts in the BankLinkedList to a JSON file.
    
    Args:
        bank_list: The BankLinkedList instance to persist.
        file_path: Target JSON file path.
        
    Returns:
        Tuple of (success: bool, status_message: str)
    """
    try:
        # Ensure target directory exists
        dirname = os.path.dirname(file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

        # Temporary list of dicts used ONLY during JSON file dump
        serialized_records = []
        curr = bank_list.head
        while curr is not None:
            serialized_records.append(curr.to_dict())
            curr = curr.next

        payload = {
            "version": "1.0",
            "count": len(serialized_records),
            "accounts": serialized_records,
        }

        # Write safely to JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        return True, f"Successfully persisted {len(serialized_records)} account(s) to '{file_path}'."
    except Exception as e:
        return False, f"Failed to save accounts to '{file_path}': {e}"


def load_accounts(file_path: str = DEFAULT_STORAGE_FILE) -> Tuple[BankLinkedList, str]:
    """
    Reconstruct a BankLinkedList from a saved JSON file.
    Handles missing file, empty file, or corrupted data gracefully.
    
    Args:
        file_path: Path to the JSON file to read.
        
    Returns:
        Tuple of (BankLinkedList, status_message: str)
    """
    new_list = BankLinkedList()

    if not os.path.exists(file_path):
        return new_list, f"Data file '{file_path}' not found. Starting with a fresh empty bank database."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return new_list, f"Data file '{file_path}' was empty. Initialized with fresh bank database."
            data = json.loads(content)

        raw_accounts = data.get("accounts", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])

        loaded_count = 0
        for item in raw_accounts:
            try:
                node = AccountNode.from_dict(item)
                new_list.insert_node(node)
                loaded_count += 1
            except Exception as node_err:
                # Skip malformed record and continue loading remaining
                print(f"[Warning] Skipped corrupt account node: {node_err}")

        return new_list, f"Loaded {loaded_count} account record(s) from '{file_path}'."

    except json.JSONDecodeError as err:
        return new_list, f"Data file '{file_path}' contained invalid JSON ({err}). Started with empty list."
    except Exception as e:
        return new_list, f"Error loading '{file_path}': {e}. Started with empty list."
