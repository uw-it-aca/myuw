var TranscriptsCard = {
    name: 'TranscriptsCard',
    dom_target: undefined,

    render_init: function() {
        TranscriptsCard._render();
    },

    _render: function () {
        var source = $("#transcripts_card_content").html();
        var template = Handlebars.compile(source);
        TranscriptsCard.dom_target.html(template({}));
        LogUtils.cardLoaded(TranscriptsCard.name, TranscriptsCard.dom_target);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.TranscriptsCard = TranscriptsCard;
