var ThriveCard = {
    name: 'ThriveCard',
    dom_target: undefined,
    target_group: undefined,

    hide_card: function() {
        if (window.user.fyp ||
            window.user.aut_transfer ||
            window.user.win_transfer) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (ThriveCard.hide_card()) {
            $("#ThriveCard").hide();
            return;
        }
        WSData.fetch_thrive_data(ThriveCard.render_upon_data,
                                 ThriveCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.thrive_data()) {
            ThriveCard._render();
        }
    },

    _render: function () {
        Handlebars.registerPartial('thrive_highlight',
                                   $("#thrive_highlight").html());
        Handlebars.registerPartial('thrive_learnmore',
                                   $("#thrive_learnmore").html());
        var thrive = WSData.thrive_data();
        if (window.user.fyp) {
            thrive.target_fyp = true;
            ThriveCard.target_group = '_fyp';
        }
        if (window.user.aut_transfer) {
            thrive.target_aut_transfer = true;
            ThriveCard.target_group = '_au_xfer';
        }
        if (window.user.win_transfer) {
            thrive.target_win_transfer = true;
            ThriveCard.target_group = '_wi_xfer';
        }
        var source = $("#thrive_card").html();
        var template = Handlebars.compile(source);
        ThriveCard.dom_target.html(template(thrive));
        var name = ThriveCard.name + ThriveCard.target_group;
        LogUtils.cardLoaded(name, ThriveCard.dom_target);
        ThriveCard.add_events();
    },

    add_events: function(term) {
        $(".what-is-thrive").on("click", function(ev) {
            WSData.log_interaction("click_what_is_thrive" + ThriveCard.target_group);
        });
        $(".view-thrive-msg").on("click", function(ev) {
            WSData.log_interaction("click_view_thrive_msg" + ThriveCard.target_group);
        });
    },

    render_error: function () {
        $("#ThriveCard").hide();
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ThriveCard = ThriveCard;
