from tables import assign_table, release_table
from orders import open_order, add_item_to_order, calculate_bill
from menu import filter_menu
from storage import load_state, save_state, log_kitchen_ticket

DATA_DIR = "data"
TICKETING_DIR = "ticketing"


def host_menu(tables):
    print("\n--- Host Menu ---")
    table_number = int(input("Enter table number: "))
    party_size = int(input("Enter party size: "))

    table = assign_table(tables, table_number, party_size)

    if table:
        print("Table assigned successfully.")
    else:
        print("Unable to assign table (capacity or availability issue).")


def server_menu(tables, menu, orders):
    print("\n--- Server Menu ---")
    table_number = int(input("Enter table number: "))

    order = open_order(table_number)
    orders.append(order)

    while True:
        print("\n1. Add item to order")
        print("2. Send order to kitchen")
        print("3. Close order")
        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter menu category: ")
            items = filter_menu(menu, category)

            if not items:
                print("No items found.")
                continue

            for item in items:
                print(item)

            item_id = input("Enter item ID: ")
            quantity = int(input("Enter quantity: "))

            # Find the selected menu item
            for cat in menu.values():
                if item_id in cat:
                    menu_item = {
                        "id": item_id,
                        "name": cat[item_id]["name"],
                        "price": cat[item_id]["price"],
                        "available": cat[item_id]["available"]
                    }
                    add_item_to_order(order, menu_item, quantity)
                    print("Item added.")
                    break

        elif choice == "2":
            log_kitchen_ticket(order, TICKETING_DIR)
            print("Order sent to kitchen.")

        elif choice == "3":
            bill = calculate_bill(order, 0.07, 0.18)
            print("\n--- Bill ---")
            print(bill)

            order["open"] = False
            release_table(tables, table_number)
            print("Order closed and table released.")
            break

        else:
            print("Invalid option.")


def main():
    tables, menu, orders = load_state(DATA_DIR)

    while True:
        print("\n=== Restaurant System ===")
        print("1. Host")
        print("2. Server")
        print("3. Exit")

        choice = input("Select role: ")

        if choice == "1":
            host_menu(tables)
        elif choice == "2":
            server_menu(tables, menu, orders)
        elif choice == "3":
            save_state(DATA_DIR, tables, menu, orders)
            print("State saved. Goodbye!")
            break
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()
