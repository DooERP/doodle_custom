frappe.ui.form.on('Lead', {

    setup(frm) {
        frm.set_query('custom_new_services', function() {
            return {
                filters: {
                    division: frm.doc.division
                }
            };
        });
    },

    // division(frm) {

    //     frm.set_value('custom_new_services', '');

    //     if (!frm.doc.division) {
    //         return;
    //     }

    //     frappe.db.get_value(
    //         'Services',
    //         { division: frm.doc.division },
    //         'services'
    //     ).then(r => {

    //         if (
    //             r.message &&
    //             r.message.services
    //         ) {
    //             frm.set_value(
    //                 'custom_new_services',
    //                 r.message.services
    //             );
    //         }

    //     });
    // }
});