var ThriveCard = {
    name: 'ThriveCard',
    dom_target: undefined,

    render_init: function() {
        //WSData.fetch_hfs_data(ThriveCard.render_upon_data, ThriveCard.render_error);
        ThriveCard._render();
    },

    render_upon_data: function () {
        if (!ThriveCard._has_all_data()) {
            return;
        }
        ThriveCard._render();
    },

    _render: function () {
        //var hfs_data = WSData.hfs_data();
        var source = $("#thrive_card").html();
        var template = Handlebars.compile(source);
        ThriveCard.dom_target.html(template());
        //if (!hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
        //    ThriveCard.dom_target.hide();
        //} else {
        //
        //}
    },

    _has_all_data: function () {
        //if (WSData.hfs_data()) {
        //    return true;
        //}
        //return false;
    },

    render_error: function () {
        ThriveCard.dom_target.html(CardWithError.render("Thrive Messaging"));
    }
};
