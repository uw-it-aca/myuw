var ReenrollConEduCard = {
    name: 'ReenrollConEduCard',
    dom_target: undefined,

    render_init: function() {
        ReenrollConEduCard._render();
    },

    _render: function () {
        var source = $("#reenroll_ctnu_edu_content").html();
        var template = Handlebars.compile(source);
        ReenrollConEduCard.dom_target.html(template({}));
        LogUtils.cardLoaded(ReenrollConEduCard.name,
                            ReenrollConEduCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.ReenrollConEduCard = ReenrollConEduCard;
