
import frappe
import traceback


def save_deleted_lead(doc, method=None):

    def debug_log(message):
        frappe.log_error(
            title="Desert Forest Lead Delete",
            message=message
        )

    try:
        # STEP 1: Check whether hook is triggered
        debug_log(
            f"STEP 1: Before Delete triggered\n"
            f"Lead: {doc.name}\n"
            f"User: {frappe.session.user}\n"
            f"Method: {method}"
        )

        # STEP 2: Get External ID
        external_id = doc.get("custom_desert_forest_lead_id")

        debug_log(
            f"STEP 2: External ID fetched\n"
            f"Lead: {doc.name}\n"
            f"External ID: {external_id}"
        )

        if not external_id:
            debug_log(
                f"STEP 3: Skipped Lead {doc.name}\n"
                "Reason: custom_desert_forest_lead_id is empty"
            )
            return

        external_id = str(external_id).strip()

        if not external_id:
            debug_log(
                f"STEP 3: Skipped Lead {doc.name}\n"
                "Reason: External ID is blank after stripping"
            )
            return

        # STEP 4: Check whether External ID already exists
        existing = frappe.db.exists(
            "External Id Document",
            {"external_id": external_id}
        )

        debug_log(
            f"STEP 4: Duplicate check completed\n"
            f"External ID: {external_id}\n"
            f"Existing record: {existing}"
        )

        if existing:
            debug_log(
                f"STEP 5: Skipped Lead {doc.name}\n"
                f"External ID already exists: {existing}"
            )
            return

        # STEP 6: Create External Id record
        deleted_lead = frappe.get_doc({
            "doctype": "External Id Document",
            "lead_id": doc.name,
            "external_id": external_id,
            "phone_number": doc.get("mobile_no") or ""
        })

        debug_log(
            f"STEP 6: External Id document prepared\n"
            f"Lead: {doc.name}\n"
            f"External ID: {external_id}"
        )

        # STEP 7: Insert record
        # deleted_lead.flags.ignore_validate = True
        deleted_lead.insert(ignore_permissions=True)

        debug_log(
            f"STEP 7: SUCCESS\n"
            f"External Id created: {deleted_lead.name}\n"
            f"Lead: {doc.name}\n"
            f"External ID: {external_id}"
        )

    except Exception:
        frappe.log_error(
            title="Desert Forest Lead Delete FAILED",
            message=traceback.format_exc()
        )

        # Re-raise so failed logging/insert doesn't silently
        # allow the Lead to be deleted.
        raise
