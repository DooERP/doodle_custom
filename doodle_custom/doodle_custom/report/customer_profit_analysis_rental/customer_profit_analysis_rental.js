// Copyright (c) 2026, Doodle Tech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Profit Analysis Rental"] = {
	filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "customer",
            label: __("Customer"),
            fieldtype: "Link",
            options: "Customer"
        },
        {
            fieldname: "delivery_note_status",
            label: __("Delivery Note Status"),
            fieldtype: "Select",
            options: [
                "",
                "Draft",
                "To Bill",
                "Completed",
                "Closed",
                "Return Issued"
            ]
        }
    ]
};
