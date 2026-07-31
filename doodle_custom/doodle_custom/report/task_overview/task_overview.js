// Copyright (c) 2026, Doodle Tech and contributors
// For license information, please see license.txt

frappe.query_reports["Task Overview"] = {
    filters: [

        {
            fieldname: "employee",
            label: "Employee",
            fieldtype: "Link",
            options: "Employee"
        },
        {
            fieldname: "department",
            label: "Department",
            fieldtype: "Link",
            options: "Department"
        },
                {
            fieldname: "start_date",
            label: __("Start Date"),
            fieldtype: "Date",
            // default: frappe.datetime.add_days(frappe.datetime.get_today(), -7)
        },
        {
            fieldname: "end_date",
            label: __("End Date"),
            fieldtype: "Date",
            // default: frappe.datetime.get_today()
        },
        {
    fieldname: "project",
    label: "Project",
    fieldtype: "Link",
    options: "Project"
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
                description: d,   // 🔥 IMPORTANT
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

        // 🎯 Highlight Remaining Hours column
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
