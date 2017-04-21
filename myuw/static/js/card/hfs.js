var HfsCard = {
    name: 'HFSCard',
    dom_target: undefined,

    render_init: function() {
        WebServiceData.require({hfs_data: new HFSData()}, HfsCard.render);
    },

    render: function (resources) {
        var hfs_data_resource = resources.hfs_data;
        if (HfsCard.render_error(hfs_data_resource.error)) {
            return;
        }

        var hfs_data = hfs_data_resource.data;
        var source = $("#hfs_card_content").html();
        var template = Handlebars.compile(source);
        var template_data;
        if (!hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
            HfsCard.dom_target.hide();
        } else {
            HfsCard.dom_target.html(template(hfs_data));
            LogUtils.cardLoaded(HfsCard.name, HfsCard.dom_target);
        }
    },

    render_error: function (hfs_data_error) {
        if (hfs_data_error) {
            if (hfs_data_error.status === 404) {
                HfsCard.dom_target.hide();
            } else {
                var raw = CardWithError.render("Husky Card & Dining");
                HfsCard.dom_target.html(raw);
            }

            return true;
        }

        return false;
    }
};
