var HfsCard = {
    name: 'HFSCard',
    dom_target: undefined,

    render_init: function() {
        WSData.fetch_hfs_data(HfsCard.render_upon_data, HfsCard.render_error);
    },

    render_upon_data: function () {
        if (!HfsCard._has_all_data()) {
            return;
        }
        HfsCard._render();
    },

    _render: function () {
        var hfs_data = WSData.hfs_data();
        var source = $("#hfs_card_content").html();
        var template = Handlebars.compile(source);
        var template_data;
        if (!hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
            template_data = {hfs_data: null};
        } else {
            template_data = {
                hfs_data: hfs_data
            };
        }
        HfsCard.dom_target.html(template(template_data));
    },

    _has_all_data: function () {
        if (WSData.hfs_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        HfsCard.dom_target.html(CardWithError.render("Husky Card & Dining"));
    }
};
