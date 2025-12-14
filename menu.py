import json
from typing import Dict, List


def load_menu(path: str) -> Dict:
    """
    Load the menu from a JSON file.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "starters": {},
            "mains": {},
            "desserts": {},
            "beverages": {}
        }


def save_menu(path: str, menu: Dict) -> None:
    """
    Save the menu to a JSON file.
    """
    with open(path, "w") as file:
        json.dump(menu, file, indent=4)


def add_menu_item(menu: Dict, item: Dict) -> Dict:
    """
    Add a new menu item to a category.
    Expected item keys:
    id, name, category, price, vegetarian
    """
    category = item["category"]
    item_id = item["id"]

    if category not in menu:
        raise ValueError("Invalid menu category")

    menu[category][item_id] = {
        "name": item["name"],
        "price": float(item["price"]),
        "vegetarian": bool(item["vegetarian"]),
        "available": True
    }

    return menu


def update_menu_item(menu: Dict, item_id: str, updates: Dict) -> Dict:
    """
    Update fields of an existing menu item.
    """
    for category in menu.values():
        if item_id in category:
            category[item_id].update(updates)
            return menu

    raise KeyError("Menu item not found")


def filter_menu(
    menu: Dict,
    category: str,
    vegetarian: bool | None = None
) -> List[Dict]:
    """
    Return a list of available menu items matching filters.
    """
    if category not in menu:
        return []

    results = []

    for item_id, item in menu[category].items():
        if not item["available"]:
            continue

        if vegetarian is not None and item["vegetarian"] != vegetarian:
            continue

        results.append({
            "id": item_id,
            "name": item["name"],
            "price": item["price"],
            "vegetarian": item["vegetarian"]
        })

    return results
