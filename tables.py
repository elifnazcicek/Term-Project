import json

def initialize_tables(path: str) -> list:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_table(tables: list, table_data: dict) -> list:
    new_table = {
        "number": table_data["number"],
        "capacity": table_data["capacity"],
        "status": "free",
        "server": "",
        "party_size": 0
    }
    tables.append(new_table)
    return tables

def assign_table(tables: list, table_number: int, party_size: int):
    for table in tables:
        if table["number"] == table_number:
            if table["status"] == "occupied":
                return None
            if party_size > table["capacity"]:
                return None
            table["status"] = "occupied"
            table["party_size"] = party_size
            return table
    return None

#release_table ve update_server daha kodlamadım
