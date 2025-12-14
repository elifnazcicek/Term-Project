from typing import Dict, List
from uuid import uuid4


def open_order(table_number: int) -> Dict:
    """
    Open a new order for a table.
    """
    return {
        "order_id": str(uuid4()),
        "table_number": table_number,
        "items": [],
        "open": True
    }


def add_item_to_order(
    order: Dict,
    menu_item: Dict,
    quantity: int,
    note: str = ""
) -> Dict:
    """
    Add an item to an order.
    """
    if not menu_item.get("available", True):
        raise ValueError("Menu item is not available")

    order["items"].append({
        "item_id": menu_item["id"],
        "name": menu_item["name"],
        "price": menu_item["price"],
        "quantity": quantity,
        "note": note,
        "status": "ordered"
    })

    return order


def remove_item_from_order(order: Dict, item_id: str) -> Dict:
    """
    Remove an item from an order.
    """
    order["items"] = [
        item for item in order["items"]
        if item["item_id"] != item_id
    ]
    return order


def update_item_status(order: Dict, item_id: str, status: str) -> Dict:
    """
    Update the status of an item in an order.
    """
    valid_statuses = {"ordered", "prepared", "served", "voided"}

    if status not in valid_statuses:
        raise ValueError("Invalid item status")

    for item in order["items"]:
        if item["item_id"] == item_id:
            item["status"] = status
            return order

    raise KeyError("Item not found in order")


def calculate_bill(
    order: Dict,
    tax_rate: float,
    tip_rate: float
) -> Dict:
    """
    Calculate subtotal, tax, tip, and total for an order.
    """
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in order["items"]
        if item["status"] != "voided"
    )

    tax = round(subtotal * tax_rate, 2)
    tip = round(subtotal * tip_rate, 2)
    total = round(subtotal + tax + tip, 2)

    return {
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "tip": tip,
        "total": total
    }


def split_bill(
    order: Dict,
    method: str,
    parties: int | List[int]
) -> List[Dict]:
    """
    Split a bill evenly or by seat counts.
    """
    bill = calculate_bill(order, tax_rate=0, tip_rate=0)
    total = bill["subtotal"]

    splits = []

    if method == "even":
        amount = round(total / parties, 2)
        for _ in range(parties):
            splits.append({"amount": amount})

    elif method == "by_seat":
        total_seats = sum(parties)
        for seat_count in parties:
            share = round((seat_count / total_seats) * total, 2)
            splits.append({"amount": share})

    else:
        raise ValueError("Invalid split method")

    return splits
