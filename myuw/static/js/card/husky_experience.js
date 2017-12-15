var HuskyExperienceCard = {
    name: 'HuskyExperienceCard',
    dom_target: undefined,

    hide_card: function() {
        return false;
    },

    render_init: function() {
        console.log('asds');
        if (HuskyExperienceCard.hide_card()) {
            $("#HuskyExperienceCard").hide();
            return;
        }
        console.log('pre-fetch');
        WSData.fetch_hx_toolkit_week_msg(HuskyExperienceCard.render_upon_data,
                                         HuskyExperienceCard.render_error);
    },

    render_upon_data: function () {
        if (WSData.hx_toolkit_week_data()) {
            HuskyExperienceCard._render();
        }
    },

    _render: function () {
        var article_html = WSData.hx_toolkit_week_data();
        var source = $("#husky_experice").html();
        var template = Handlebars.compile(source);
        var rendered = template({article_html: article_html});
        HuskyExperienceCard.dom_target.html(rendered);
        var name = HuskyExperienceCard.name;
        LogUtils.cardLoaded(name, HuskyExperienceCard.dom_target);
        HuskyExperienceCard.add_events();
    },

    add_events: function(term) {
    },

    render_error: function () {
        $("#HuskyExperienceCard").hide();
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.HuskyExperienceCard = HuskyExperienceCard;
