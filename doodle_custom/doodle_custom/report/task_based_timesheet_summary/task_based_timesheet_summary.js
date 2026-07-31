frappe.query_reports["Task Based Timesheet Summary"] = {
    filters: [
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
            fieldname: "employee",
            label: __("Employee"),
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
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project"
        },
        {
            fieldname: "task",
            label: __("Task"),
            fieldtype: "Link",
            options: "Task"
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
        },
        {
        fieldname: "task_status",
        label: __("Task Status"),
        fieldtype: "MultiSelectList",
        get_data: function(txt) {
            const options = [
                "Open",
                "Working",
                "Pending Review",
                "On Hold",
                "Overdue",
                "To be Done",
                "Completed",
                "Cancelled"
            ];
            return options
                .filter(d => !txt || d.toLowerCase().includes(txt.toLowerCase()))
                .map(d => ({
                    description: d,
                    value: d
                }));
        },
        default: ["Open", "Working", "Pending Review"]
    }
    ],
    onload: function(report) {

        // Project Status default
        report.set_filter_value("project_status", [
            "Open",
            "In Progress",
            "On Hold"
        ]);

        // Task Status default
        report.set_filter_value("task_status", [
            "Open",
            "Working",
            "Pending Review",
            "Overdue",
            "To be Done",
        ]);
    },


    // onload: function () {
    //     setTimeout(() => {
    //         load_summary();
    //     }, 500);
    // },

    // after_datatable_render: function () {
    //     load_summary();
    // },

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


// // ✅ MUST BE GLOBAL
// function load_summary() {

//     let filters = {
//         project: frappe.query_report.get_filter_value("project"),
//         start_date: frappe.query_report.get_filter_value("start_date"),
//         end_date: frappe.query_report.get_filter_value("end_date"),
//         employee: frappe.query_report.get_filter_value("employee"),
//         task: frappe.query_report.get_filter_value("task")
//     };
//     frappe.call({
//         method: "doodle_custom.doodle_custom.report.task_based_timesheet_summary.task_based_timesheet_summary.get_employee_workload_summary",
//         args: {
//             filters: filters
//         },
//         callback: function (r) {

//             if (!r.message) return;

//             let rows = r.message;

//             $(".task-summary").remove();

//             let html = `
//                 <div class="task-summary"
//                     style="
//                         margin-top:20px;
//                         padding:12px;
//                         background:#f8fafc;
//                         border-radius:8px;
//                     ">
//                     <h5>📌 Task Summary</h5>
//             `;

//             rows.forEach(row => {

//                 let remainingColor = row.remaining_hours < 0 ? "red" : "green";

//                 html += `
//                     <div style="
//                         display:flex;
//                         gap:15px;
//                         padding:6px 0;
//                         border-bottom:1px solid #eee;
//                     ">
//                         <div>Employee: ${row.employee}</div>

//                         <div>Expected: ${row.expected_hours}</div>
//                         <div>Completed: ${row.completed_hours}</div>

//                         <div style="color:${remainingColor}">
//                             Remaining: ${row.remaining_hours}
//                         </div>

//                         <div>Status: ${row.status}</div>
//                     </div>
//                 `;
//             });

//             html += `</div>`;

//             $(".report-wrapper").append(html);
//         }
//     });
// }