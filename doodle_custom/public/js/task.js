frappe.ui.form.on("Task", {
    refresh(frm) {
        set_division_mandatory_fields(frm);
    },

    custom_division(frm) {
        set_division_mandatory_fields(frm);
    }
});

function set_division_mandatory_fields(frm) {
    const is_doodle_erp =
        frm.doc.custom_division === "Doodle ERP - DTL";

    frm.toggle_reqd("type", is_doodle_erp);
    frm.toggle_reqd("custom_task_assign_to", is_doodle_erp);
    frm.toggle_reqd("expected_time", is_doodle_erp);
}