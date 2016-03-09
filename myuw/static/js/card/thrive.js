var ThriveCard = {
    name: 'ThriveCard',
    dom_target: undefined,

    render_init: function() {
        if (window.user.fyp) {
            WSData.fetch_thrive_data(ThriveCard.render_upon_data, ThriveCard.render_error);
            return;
        }
        $("#ThriveCard").hide();
    },

    render_upon_data: function () {
        if (!ThriveCard._has_all_data()) {
            return;
        }
        ThriveCard._render();
    },

    _render: function () {
        var thrive = WSData.thrive_data();
        var source = $("#thrive_card").html();
        var template = Handlebars.compile(source);
        ThriveCard.dom_target.html(template(thrive));
        LogUtils.cardLoaded(ThriveCard.name, ThriveCard.dom_target);
    },

    _has_all_data: function () {
        if (WSData.thrive_data()) {
            return true;
        }
        return false;
    },

    render_error: function () {
        $("#ThriveCard").hide();
    }
};
