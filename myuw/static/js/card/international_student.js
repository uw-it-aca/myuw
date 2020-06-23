var IntlStudCard = {
    name: 'IntlStudCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.intl_stud) {
            $("#IntlStudCard").hide();
            return;
        }
        Handlebars.registerPartial("seattle_international",
                                   $("#seattle_international").html());
        Handlebars.registerPartial("bothell_international",
                                   $("#bothell_international").html());
        Handlebars.registerPartial("tacoma_international",
                                   $("#tacoma_international").html());

        IntlStudCard._render();
    },

    _render: function () {
        var data = {
            is_f1: window.user.f1,
            is_j1: window.user.j1,
            is_intl_stud: window.user.intl_stud,
            seattle: window.user.seattle,
            bothell: window.user.bothell,
            tacoma: window.user.tacoma
            };
        IntlStudCard._render_with_context(data);
        LogUtils.cardLoaded(IntlStudCard.name, IntlStudCard.dom_target);
    },

    _render_with_context: function (context){
        var source = $("#international_student_card_content").html();
        var internationalStudents_template = Handlebars.compile(source);
        var raw = internationalStudents_template(context);
        IntlStudCard.dom_target.html(raw);
    },
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.IntlStudCard = IntlStudCard;
