from orders import open_order, add_item_to_order, calculate_bill
from tables import add_table, assign_table


def test_order_total():
    order = open_order(1)
    item = {"id": "T1", "name": "Test Item", "price": 10.0, "available": True}
    add_item_to_order(order, item, 2)

    bill = calculate_bill(order, 0.1, 0.2)
    assert bill["total"] == 26.0


def test_table_capacity_limit():
    tables = []
    add_table(tables, {"table_number": 1, "capacity": 2})
    result = assign_table(tables, 1, 4)
    assert result is None


def test_unavailable_item():
    order = open_order(1)
    item = {"id": "X", "name": "Bad Item", "price": 5.0, "available": False}

    try:
        add_item_to_order(order, item, 1)
        assert False
    except ValueError:
        assert True

