import json

def initialize_tables(path: str) -> list:
    """JSON dosyasını okuyup tablo listesini döndürür.
       Dosya yoksa boş liste döner."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def add_table(tables: list, table_data: dict) -> list:
    """Yeni tablo ekler."""
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
    """Tabloyu belirtilen parti boyutuna göre oturtur."""
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

def release_table(tables: list, table_number: int) -> bool:
    """Masayı boşaltır"""
    for table in tables:
        if table["number"] == table_number:
            table["status"] = "free"
            table["party_size"] = 0
            return True
    return False

def update_server(tables: list, table_number: int, server_name: str) -> dict:
    """Tablonun garsonunu günceller."""
    for table in tables:
        if table["number"] == table_number:
            table["server"] = server_name
            return table
    return None
