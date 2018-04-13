var ResourcesExploreCard = {
    name: 'ResourcesExploreCard',
    dom_target: undefined,
    target_group: undefined,

    render_init: function() {
        ResourcesExploreCard._render();
    },

    _render: function () {
        var source = $("#resources_card_explore").html();
        var template = Handlebars.compile(source);
        ResourcesExploreCard.dom_target.html(template());

    }

};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ResourcesExploreCard = ResourcesExploreCard;
