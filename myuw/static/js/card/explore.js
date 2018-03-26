var ExploreCard = {
    name: 'ExploreCard',
    dom_target: undefined,
    target_group: undefined,

    hide_card: function() {
        return false;
    },

    render_init: function() {
        if (ExploreCard.hide_card()) {
            $("#ExploreCard").hide();
            return;
        }
        WSData.fetch_explore_data(ExploreCard.render_upon_data,
                                  ExploreCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.thrive_data()) {
            ExploreCard._render();
        }
    },

    _render: function () {
        var source = $("#thrive_card").html();
        var template = Handlebars.compile(source);
        ExploreCard.dom_target.html(template(thrive));
        var name = ExploreCard.name + ExploreCard.target_group;
        LogUtils.cardLoaded(name, ExploreCard.dom_target);
        ExploreCard.add_events();
    },

    add_events: function(term) {
        $(".what-is-thrive").on("click", function(ev) {
            WSData.log_interaction("click_what_is_thrive" + ExploreCard.target_group);
        });
        $(".view-thrive-msg").on("click", function(ev) {
            WSData.log_interaction("click_view_thrive_msg" + ExploreCard.target_group);
        });
    },

    render_error: function () {
        $("#ExploreCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ExploreCard = ExploreCard;
