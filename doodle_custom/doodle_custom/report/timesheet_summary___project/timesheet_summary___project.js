// Copyright (c) 2026, Admin and contributors
// For license information, please see license.txt

frappe.query_reports["Timesheet Summary - Project"] = {
	"filters": [
        {
            "fieldname": "start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -7)
        },
        {
            "fieldname": "end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee"
        },
        {
            "fieldname": "project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project"
        }
	],
    //     onload: function(report) {
    //     report.page.add_inner_button(__("Export Excel File"), function() {
    //         const filters = report.get_values();
    //         const report_name = "Timesheet Summary - Project";

    //         const url = `/api/method/baugette_custom.reportformat.export_report_xlsx?report_name=${encodeURIComponent(report_name)}&filters=${encodeURIComponent(JSON.stringify(filters))}`;

    //         window.open(url);
    //     });
    // }
};
