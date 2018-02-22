var ContinuingEducationCard = {
    name: 'ContinuingEducationCard',
    dom_target: undefined,

    render_init: function() {
        ContinuingEducationCard._render();
    },

    _render: function () {
        var source = $("#ctnu_edu_content").html();
        var template = Handlebars.compile(source);
        ContinuingEducationCard.dom_target.html(template({}));
        LogUtils.cardLoaded(ContinuingEducationCard.name,
                            ContinuingEducationCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ContinuingEducationCard = ContinuingEducationCard;
