import json
from datetime import datetime
from typing import List, Dict, Optional


def initialize_tables(path: str) -> List[Dict]:
    """
    Load tables from a JSON file.
    If the file does not exist or is empty, return an empty list.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def add_table(tables: List[Dict], table_data: Dict) -> List[Dict]:
    """
    Add a new table to the restaurant.
    """
    tables.append({
        "table_number": table_data["table_number"],
        "capacity": table_data["capacity"],
        "server": table_data.get("server", ""),
        "status": "free",
        "party_size": 0,
        "start_time": None
    })
    return tables


def assign_table(
    tables: List[Dict],
    table_number: int,
    party_size: int
) -> Optional[Dict]:
    """
    Assign a party to a table if capacity allows and table is free.
    """
    for table in tables:
        if table["table_number"] == table_number:
            if table["status"] == "occupied":
                return None

            if party_size > table["capacity"]:
                return None

            table["status"] = "occupied"
            table["party_size"] = party_size
            table["start_time"] = datetime.now().isoformat()
            return table

    return None


def release_table(tables: List[Dict], table_number: int) -> bool:
    """
    Release a table and reset its state.
    """
    for table in tables:
        if table["table_number"] == table_number:
            table["status"] = "free"
            table["party_size"] = 0
            table["start_time"] = None
            return True

    return False


def update_server(
    tables: List[Dict],
    table_number: int,
    server_name: str
) -> Optional[Dict]:
    """
    Update the server assigned to a table.
    """
    for table in tables:
        if table["table_number"] == table_number:
            table["server"] = server_name
            return table

    return None

