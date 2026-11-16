frappe.ui.form.on("Opportunity", {
    onload: function(frm) {
        fetch_lead_contact_details(frm);
    },

    refresh: function(frm) {
        console.log("Loading");
        fetch_lead_contact_details(frm);
    }
});


function fetch_lead_contact_details(frm) {

    if (
        frm.doc.opportunity_from !== "Lead" ||
        !frm.doc.party_name
    ) {
        return;
    }

    frappe.db.get_value(
        "Lead",
        frm.doc.party_name,
        [
            "phone",
            "whatsapp_no"
        ]
    ).then(r => {

        if (!r.message) {
            return;
        }

        // Lead Phone → Opportunity Phone
        if (r.message.phone) {
            frm.set_value(
                "phone",
                r.message.phone
            );
        }

        // Lead WhatsApp → Opportunity WhatsApp
        if (r.message.whatsapp_no) {
            frm.set_value(
                "whatsapp",
                r.message.whatsapp_no
            );
        }
    });
}