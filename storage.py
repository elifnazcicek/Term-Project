import json
import os
from datetime import datetime
from typing import List, Dict, Tuple


def _load_json(path: str, default):
    """
    Helper function to load JSON safely.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def load_state(data_dir: str) -> Tuple[List, Dict, List]:
    """
    Load tables, menu, and orders from disk.
    """
    tables = _load_json(os.path.join(data_dir, "tables.json"), [])
    menu = _load_json(os.path.join(data_dir, "menu.json"), {
        "starters": {},
        "mains": {},
        "desserts": {},
        "beverages": {}
    })
    orders = _load_json(os.path.join(data_dir, "orders.json"), [])

    return tables, menu, orders


def save_state(
    data_dir: str,
    tables: List,
    menu: Dict,
    orders: List
) -> None:
    """
    Save current tables, menu, and orders to disk.
    """
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, "tables.json"), "w") as file:
        json.dump(tables, file, indent=4)

    with open(os.path.join(data_dir, "menu.json"), "w") as file:
        json.dump(menu, file, indent=4)

    with open(os.path.join(data_dir, "orders.json"), "w") as file:
        json.dump(orders, file, indent=4)


def backup_day(data_dir: str, archive_dir: str) -> str:
    """
    Create a daily backup of all operational data.
    """
    os.makedirs(archive_dir, exist_ok=True)

    backup_name = datetime.now().strftime("%Y-%m-%d-backup.json")
    backup_path = os.path.join(archive_dir, backup_name)

    tables, menu, orders = load_state(data_dir)

    with open(backup_path, "w") as file:
        json.dump({
            "tables": tables,
            "menu": menu,
            "orders": orders
        }, file, indent=4)

    return backup_path


def log_kitchen_ticket(order: Dict, directory: str) -> str:
    """
    Write a kitchen ticket text file for an order.
    """
    os.makedirs(directory, exist_ok=True)

    filename = f"order_{order['order_id']}.txt"
    path = os.path.join(directory, filename)

    with open(path, "w") as file:
        file.write(f"TABLE: {order['table_number']}\n")
        file.write("-" * 20 + "\n")

        for item in order["items"]:
            if item["status"] == "ordered":
                file.write(
                    f"{item['quantity']}x {item['name']} "
                    f"({item['note']})\n"
                )

    return path
