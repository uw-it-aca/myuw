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
        if (WSData.explore_data()) {
            ExploreCard._render();
        }
    },

    _render: function () {
        var source = $("#explore_card").html();
        var template = Handlebars.compile(source);
        ExploreCard.dom_target.html(template());
        var name = ExploreCard.name + ExploreCard.target_group;
        LogUtils.cardLoaded(name, ExploreCard.dom_target);
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
