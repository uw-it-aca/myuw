var TeachingResourcesCard = {
    name: 'TeachingResourcesCard',
    dom_target: undefined,

    render_init: function() {
        TeachingResourcesCard.render();
    },

    render: function () {
        var source = $("#teaching_resources_card").html();
        var template = Handlebars.compile(source);
        TeachingResourcesCard.dom_target.html(template({
            seattle_affil: (window.user.seattle_affil || window.user.seattle),
            bothell_affil: (window.user.bothell_affil || window.user.bothell),
            tacoma_affil: (window.user.tacoma_affil || window.user.tacoma)
        }));
    },
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TeachingResourcesCard = TeachingResourcesCard;
