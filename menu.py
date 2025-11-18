import json

menu_file = "data/menu.json"

def load_menu():
    try:
        with open(menu_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"items": {}}

def save_menu(menu):
    with open(menu_file, "w") as f:
        json.dump(menu, f, indent=2)

def add_menu_item(menu, name, category, price):
    new_id = str(len(menu["items"]) + 1)
    menu["items"][new_id] = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price
    }
    return menu["items"][new_id]

def update_menu_item(menu, item_id, updates):
    if item_id not in menu["items"]:
        return None
    menu["items"][item_id].update(updates)
    return menu["items"][item_id]

def filter_menu(menu, category):
    result = []
    for item in menu["items"].values():
        if item["category"] == category:
            result.append(item)
    return result
