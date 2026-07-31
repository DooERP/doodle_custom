frappe.query_reports["Project Based Timesheet Summary"] = {
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
            fieldname: "project",
            label: __("Project"),
            fieldtype: "Link",
            options: "Project"
        },
        {
            fieldname: "project_status",
            label: __("Project Status"),
            fieldtype: "MultiSelectList",
            get_data: function(txt) {
                const options = [
                    "Open",
                    "In Progress",
                    "On Hold",
                    "Completed",
                    "Cancelled"
                ];

                return options
                    .filter(d => !txt || d.toLowerCase().includes(txt.toLowerCase()))
                    .map(d => ({ description: d, value: d }));
            }
        },
        {
            fieldname: "department",
            label: __("Department"),
            fieldtype: "Link",
            options: "Department"
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
    // onload: function () {
    //     setTimeout(load_summary, 500);
    // },

    // after_datatable_render: function () {
    //     load_summary();
    // }
};


// function load_summary() {

//     let project = frappe.query_report.get_filter_value("project");
//     let start_date = frappe.query_report.get_filter_value("start_date");
//     let end_date = frappe.query_report.get_filter_value("end_date");
//     let employee = frappe.query_report.get_filter_value("employee");

//     if (!project) {
//         $(".project-summary").remove();
//         return;
//     }

//     frappe.call({
//         method: "doodle_custom.doodle_custom.report.project_based_timesheet_summary.project_based_timesheet_summary.get_project_summary",
//         args: {
//             filters: {
//                 project: project,
//                 start_date: start_date,
//                 end_date: end_date,
//                 employee: employee
//             }
//         },
//         callback: function (r) {

//             console.log("SUMMARY RESPONSE:", r);

//             if (!r.message) return;

//             let d = r.message;

//             $(".project-summary").remove();

//             // 👉 APPEND BELOW REPORT
//             $(".report-wrapper").append(`
//                 <div class="project-summary"
//                     style="
//                         display:flex;
//                         gap:20px;
//                         padding:12px;
//                         margin:15px 0;
// 						margin-left:250px;
//                         background: linear-gradient(90deg, #eef2ff, #ffffff);
//                         border-radius:8px;
//                         font-weight:500;
//                         box-shadow: 0 1px 4px rgba(0,0,0,0.05);
//                         font-size: 13px;
//                         align-items: center;
//                     ">
//                     <div>Budget Hours: <b>${d.budget}</b></div>
//                     <div>⏱ Used Hours: <b>${d.used}</b></div>
//                     <div>⏳ Remaining Hours: <b>${d.remaining}</b></div>
//                 </div>
//             `);
//         }
//     });
// }