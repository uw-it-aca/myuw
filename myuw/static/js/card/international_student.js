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
            seattle: false,
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
        IntlStudCard.add_events();
    },




    add_events: function() {
        $("a.myuw-tab-label").click(function(ev) {
            var campus = $(ev.target).attr('rel');
            var tabcontent = document.getElementsByClassName("intl_tab_content");
            for (i = 0; i < tabcontent.length; i++) {
                if (tabcontent[i].id === campus) {
                    tabcontent[i].style.display = "block";
                    $(tabcontent[i]).attr('aria-hidden', false);
                } else {
                    tabcontent[i].style.display = "none";
                    $(tabcontent[i]).attr('aria-hidden', true);
                }
            }
            var tablinks = document.getElementsByClassName("myuw-tab-label");
            for (i = 0; i < tablinks.length; i++) {
                if (tablinks[i].rel === campus) {
                    $(tablinks[i]).attr('aria-selected', true);
                } else {
                    $(tablinks[i]).attr('aria-selected', false);
                }
            }
            WSData.log_interaction("open_intl_"+campus);
        });
    }
    


};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.IntlStudCard = IntlStudCard;
