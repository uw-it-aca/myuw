var AcademicCard = {
    name: 'AcademicCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#AcademicCard").hide();
            return;
        }
        WSData.fetch_profile_data(AcademicCard.render_upon_data, AcademicCard.show_error);
    },

    render_upon_data: function() {
        if (!AcademicCard._has_all_data()) {
            return;
        }
        AcademicCard._render(WSData.profile_data());
    },

    _render: function (academic_data) {
        var source = $("#academic_card_content").html();
        var template = Handlebars.compile(source);
        if (!academic_data.class_level || academic_data.class_level === "NON_MATRIC") {
            AcademicCard.dom_target.hide();
        }
        else {
            AcademicCard.dom_target.html(template(academic_data));
            AcademicCard.add_events();
            LogUtils.cardLoaded(AcademicCard.name, AcademicCard.dom_target);
        }
    },

    _has_all_data: function () {
        if (WSData.profile_data()) {
            return true;
        }
        return false;
    },

    add_events: function() {
        $(".toggle_academic_card_resources").on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            var div = $("#academic_card_resources");
            var expose = $("#show_academic_resources_wrapper");
            var hide = $("#hide_academic_resources_wrapper");
            toggle_card_disclosure(card, div, expose, hide, "");
        });
    },

    show_error: function() {
        // don't show card if no account
        AcademicCard.dom_target.hide();
    }
};
