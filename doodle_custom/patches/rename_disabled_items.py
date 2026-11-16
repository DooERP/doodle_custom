
import frappe
from frappe.model.rename_doc import rename_doc

def execute():

    # Fetch all disabled items
    disabled_items = frappe.get_all(
        "Item",
        filters={"disabled": 1},
        fields=["name", "item_name"],
        order_by="name asc"
    )

    updated = 0
    skipped = 0

    for item in disabled_items:

        item_code = item.name
        current_item_name = item.item_name or item_code

        # Skip if Item Code already has suffix
        if item_code.strip().lower().endswith(
            ("-disable", "-disabled")
        ):
            print(f"ALREADY RENAMED: {item_code}")
            skipped += 1
            continue

        new_item_code = f"{item_code}-Disabled"

        # Avoid duplicate Item Codes
        if frappe.db.exists("Item", new_item_code):
            print(f"TARGET EXISTS: {new_item_code}")
            skipped += 1
            continue

        # Prepare new Item Name
        if current_item_name.strip().lower().endswith(
            ("-disable", "-disabled")
        ):
            new_item_name = current_item_name
        else:
            new_item_name = f"{current_item_name}-Disabled"

        # Rename Item Code
        rename_doc(
            "Item",
            item_code,
            new_item_code,
            force=True,
            merge=False,
            ignore_permissions=True
        )

        # Rename Item Name
        frappe.db.set_value(
            "Item",
            new_item_code,
            "item_name",
            new_item_name,
            update_modified=False
        )

        print(
            f"UPDATED: {item_code} -> {new_item_code} | "
            f"{current_item_name} -> {new_item_name}"
        )

        updated += 1

    print("\n========== SUMMARY ==========")
    print(f"Total Disabled Items: {len(disabled_items)}")
    print(f"Updated: {updated}")
    print(f"Skipped: {skipped}")
    print("=============================")
