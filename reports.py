import csv
from typing import Dict, List


def daily_sales_report(orders: List[Dict]) -> Dict:
    """
    Generate a daily sales summary.
    """
    total_revenue = 0.0
    closed_orders = 0

    for order in orders:
        if order.get("open"):
            continue

        closed_orders += 1

        for item in order["items"]:
            if item["status"] != "voided":
                total_revenue += item["price"] * item["quantity"]

    average_order = (
        round(total_revenue / closed_orders, 2)
        if closed_orders > 0 else 0.0
    )

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": closed_orders,
        "average_order_value": average_order
    }


def top_selling_items(
    orders: List[Dict],
    menu: Dict,
    limit: int = 5
) -> List[Dict]:
    """
    Return top selling menu items.
    """
    item_totals = {}

    for order in orders:
        if order.get("open"):
            continue

        for item in order["items"]:
            if item["status"] == "voided":
                continue

            item_totals[item["item_id"]] = (
                item_totals.get(item["item_id"], 0)
                + item["quantity"]
            )

    sorted_items = sorted(
        item_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for item_id, qty in sorted_items[:limit]:
        for category in menu.values():
            if item_id in category:
                results.append({
                    "item_id": item_id,
                    "name": category[item_id]["name"],
                    "quantity_sold": qty
                })

    return results


def server_performance(orders: List[Dict]) -> Dict:
    """
    Generate performance metrics per server.
    """
    performance = {}

    for order in orders:
        if order.get("open"):
            continue

        server = order.get("server", "Unknown")

        if server not in performance:
            performance[server] = {
                "tables_served": 0,
                "total_sales": 0.0
            }

        performance[server]["tables_served"] += 1

        for item in order["items"]:
            if item["status"] != "voided":
                performance[server]["total_sales"] += (
                    item["price"] * item["quantity"]
                )

    # Round totals
    for server in performance:
        performance[server]["total_sales"] = round(
            performance[server]["total_sales"], 2
        )

    return performance


def export_report(report: Dict, filename: str) -> str:
    """
    Export a report dictionary to a CSV file.
    """
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        for key, value in report.items():
            if isinstance(value, dict):
                writer.writerow([key])
                for sub_key, sub_val in value.items():
                    writer.writerow([sub_key, sub_val])
            else:
                writer.writerow([key, value])

    return filename
