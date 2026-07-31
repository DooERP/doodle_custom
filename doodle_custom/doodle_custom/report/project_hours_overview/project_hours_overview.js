// Copyright (c) 2026, Doodle Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Project Hours Overview"] = {
    "filters": [
        {
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Link",
            "options": "Project"
        },
                {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department"
        },
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date"
        },
        {
    fieldname: "project_status",
    label: "Project Status",
    fieldtype: "MultiSelectList",
    get_data: function(txt) {
        const options = [
            "Open",
            "In Progress",
            "On Hold",
            "Completed",
            "Canceled"
        ];

        return options
            .filter(d => !txt || d.toLowerCase().includes(txt.toLowerCase()))
            .map(d => ({
                description: d,
                value: d
            }));
    },
    default: ["Open", "In Progress", "On Hold"]
}
    ],
            onload: function(report) {
        // ✅ SET DEFAULT VALUES HERE
        report.set_filter_value("project_status", [
            "Open",
            "In Progress",
            "On Hold"
        ]);
    },
	    formatter: function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);

        if (column.fieldname === "more_info" && data.more_info) {
            return `<a href="${data.more_info}" target="_blank">View Details</a>`;
        }
        if (column.fieldname === "remaining_hours") {

            if (data.remaining_hours < 0) {
                value = `<span style="color:red;font-weight:bold;">
                            ${value}
                         </span>`;
            } else {
                value = `<span style="color:green;">
                            ${value}
                         </span>`;
            }
        }
        return value;
    }
};

