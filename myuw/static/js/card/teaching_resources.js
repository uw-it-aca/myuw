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
            'seattle_affil': window.user.seattle_emp,
            'bothell_affil': window.user.bothell_emp,
            'tacoma_affil': window.user.tacoma_emp
        }));
    },
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.TeachingResourcesCard = TeachingResourcesCard;
