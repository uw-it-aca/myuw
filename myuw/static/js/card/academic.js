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

            var div = $("#academic_card_resources");
            var expose = $("#show_academic_resources_wrapper");
            var hide = $("#hide_academic_resources_wrapper");
            var card = $(ev.target).closest("[data-type='card']");

            if (div.css('display') == 'none') {
                div.show();
                div.attr("hidden", false);
                // Without this timeout, the animation doesn't happen - the block just appears.
                window.setTimeout(function() {
                    div.toggleClass("slide-show");
                    expose.attr("hidden", true);
                    expose.attr("aria-hidden", true);
                    hide.attr("hidden", false);
                    hide.attr("aria-hidden", false);

                    div.attr("aria-expanded", true);
                    div.focus();
                }, 0);

                window.myuw_log.log_card(card, "expand");
            }
            else {
                div.toggleClass("slide-show");
                window.myuw_log.log_card(card, "collapse");

                setTimeout(function() {
                    expose.attr("hidden", false);
                    expose.attr("aria-hidden", false);
                    hide.attr("hidden", true);
                    hide.attr("aria-hidden", true);
                    div.attr("aria-expanded", false);
                    div.attr("hidden", true);
                    div.hide();
                }, 700);
            }
        });
    },

    show_error: function() {
        // don't show card if no account
        AcademicCard.dom_target.hide();
    }
};
