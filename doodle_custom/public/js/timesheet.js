frappe.ui.form.on("Timesheet", {
    refresh(frm) {
        set_time_log_mandatory_fields(frm);
    }
});

function set_time_log_mandatory_fields(frm) {
    const grid = frm.fields_dict.time_logs.grid;

    grid.update_docfield_property(
        "task",
        "reqd",
        1
    );

    grid.update_docfield_property(
        "expected_hours",
        "reqd",
        1
    );
}