var RegStatusCard = {
    name: 'RegStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#RegStatusCard").hide();
            return;
        }

        Handlebars.registerPartial("reg_holds",
                                   $("#reg_holds_tmpl").html());
        Handlebars.registerPartial("reg_finaid_notices",
                                   $("#reg_finaid_notices_tmpl").html());
        Handlebars.registerPartial("notice_est_reg_date",
                                   $("#notice_est_reg_date_tmpl").html());
        Handlebars.registerPartial("in_myplan",
                                   $("#in_myplan_tmpl").html());
        Handlebars.registerPartial("reg_resources",
                                   $("#reg_resources_tmpl").html());
        Handlebars.registerPartial("myplan_courses",
                                   $("#myplan_courses_tmpl").html());

        if (!(window.card_display_dates.is_after_start_of_registration_display_period &&
              window.card_display_dates.is_before_end_of_registration_display_period)) {
            $("#RegStatusCard").hide();
            return;
        }

        WSData.fetch_notice_data(RegStatusCard.render_upon_data,
                                 RegStatusCard.render_error);
        WSData.fetch_oquarter_data(RegStatusCard.render_upon_data,
                                   RegStatusCard.render_error);
    },

    render_upon_data: function() {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!RegStatusCard._has_all_data()) {
            return;
        }
        RegStatusCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data() && WSData.oquarter_data()) {
            return true;
        }
        return false;
    },

    render_error: function (status) {
        // none of the api data returns 404.
        // if any data failure, display error
        RegStatusCard.dom_target.html(CardWithError.render("Registration"));
    },

    _render_for_term: function(myplan_data, quarter, summer_card_label) {
        var reg_notices = Notices.get_notices_for_tag("reg_card_messages");
        var reg_holds = Notices.get_notices_for_tag("reg_card_holds");
        var reg_date = Notices.get_notices_for_tag("est_reg_date");
        var i, j;
        var registration_is_open = true;
        var display_reg_dates = [];

        // Filter estimated registration dates for summer...
        for (i = 0; i < reg_date.length; i++) {
            var notice = reg_date[i];
            var show_notice = false;
            var registration_date = null;

            for (j = 0; j < notice.attributes.length; j++) {
                var attribute = notice.attributes[j];

                // Extract the registration date:
                if (attribute.name == "Date") {
                    registration_date = attribute.value;
                }

                if (quarter === "Summer") {
                    if (attribute.name === "Quarter" &&
                        attribute.value === "Summer") {
                        show_notice = true;
                    }
                }
                else {
                    if (attribute.name === "Quarter" &&
                        attribute.value === quarter) {
                        show_notice = true;
                    }
                }

                if (show_notice) {
                    display_reg_dates.push({"notice": notice,
                                            "date": registration_date });
                    registration_is_open = false;
                }
            }
        }

        var year, has_registration, next_term_data;
        var financial_aid_notices;

        if (quarter == "Summer") {
            var finaid_tags = ["reg_summeraid_avail_title"];
            financial_aid_notices = Notices.get_ordered_finaid_notices(finaid_tags);
            next_term_data = WSData.oquarter_data().next_term_data;
            year = next_term_data.year;

            var terms = WSData.oquarter_data().terms;
            for (i = 0; i < terms.length; i++) {
                var term = terms[i];
                if ((term.quarter == quarter) && term.section_count) {
                    has_registration = true;
                }
            }
        }
        else {
            next_term_data = WSData.oquarter_data().next_term_data;
            quarter = next_term_data.quarter;
            year = next_term_data.year;
            has_registration = next_term_data.has_registration;
        }

        if (has_registration) {
            return;
        }

        var plan_data = null;
        if (myplan_data && myplan_data.terms) {
            plan_data = myplan_data.terms[0];
        }

        var hide_card = true;
        if (financial_aid_notices && financial_aid_notices.length) {
             hide_card = false;
        }
        if (hide_card && display_reg_dates && display_reg_dates.length) {
            hide_card = false;
        }
        if (hide_card && reg_holds && reg_holds.length) {
            hide_card = false;
        }
        if (hide_card && plan_data && plan_data.length) {
            hide_card = false;
        }

        if (hide_card) {
            return;
        }

        //Get hold count from notice attrs
        var hold_count = reg_holds.length;
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var template_data = {
            "finaid_notices": financial_aid_notices,
            "reg_notices": reg_notices,
            "reg_holds": reg_holds,
            "card": summer_card_label,
            "registration_is_open": registration_is_open,
            "is_tacoma": window.user.tacoma || window.user.tacoma_affil,
            "is_bothell": window.user.bothell || window.user.bothell_affil,
            "is_seattle": window.user.seattle || window.user.seattle_affil,
            "hold_count": reg_holds.length,
            "est_reg_date": display_reg_dates,
            "reg_next_quarter" : quarter,
            "reg_next_year": year,
            "plan_data": plan_data
        };
        var raw = template(template_data);
        return raw;
    },

    _add_events: function(summer_label) {
        // show registration resources
        var card_disclosure_class, holds_class, unready_courses;
        if (summer_label) {
            card_disclosure_class = ".show_reg_resources_"+summer_label;
            holds_class = ".reg_disclosure_"+summer_label;
            unready_courses = ".myplan_unready_courses_disclosure_"+summer_label;
        }
        else {
            card_disclosure_class = ".show_reg_resources";
            holds_class = ".reg_disclosure";
            unready_courses = ".myplan_unready_courses_disclosure";
        }

        // show registration resource
        (function(summer_card_label) {
            $('body').on('click', card_disclosure_class, function (ev) {
                ev.preventDefault();
                var card = $(ev.target).closest("[data-type='card']");

                var div, expose, hide;
                if (summer_card_label) {
                    // summer reg card
                    div = $("#reg_resources_"+summer_card_label);
                    expose = $("#show_reg_resources_wrapper_"+summer_card_label);
                    hide = $("#hide_reg_resources_wrapper_"+summer_card_label);
                }
                else {
                    div = $("#reg_resources");
                    expose = $("#show_reg_resources_wrapper");
                    hide = $("#hide_reg_resources_wrapper");
                }

                div.toggleClass("slide-show");

                if (div.hasClass("slide-show")) {
                    expose.attr("hidden", true);
                    expose.attr("aria-hidden", true);
                    hide.attr("hidden", false);
                    hide.attr("aria-hidden", false);
                    div.attr('aria-hidden', 'false');
                    window.myuw_log.log_card(card, "expand-res");
                } else {
                    window.myuw_log.log_card(card, "collapse-res");
                    setTimeout(function() {
                        expose.attr("hidden", false);
                        expose.attr("aria-hidden", false);
                        hide.attr("hidden", true);
                        hide.attr("aria-hidden", true);
                        div.attr('aria-hidden', 'true');
                    }, 700);
                }
            });

            // show myplan unready course details
            $('body').on('click', unready_courses, function (ev) {
                ev.preventDefault();
                var card = $(ev.target).closest("[data-type='card']");

                var div, expose, hide;
                if (summer_card_label) {
                    div = $("#myplan_unready_courses_"+summer_card_label);
                    expose = $("#show_unready_courses_wrapper_"+summer_card_label);
                    hide = $("#hide_unready_courses_wrapper_"+summer_card_label);
                }
                else {
                    div = $("#myplan_unready_courses");
                    expose = $("#show_unready_courses_wrapper");
                    hide = $("#hide_unready_courses_wrapper");
                }

                div.toggleClass("slide-show");

                if (div.hasClass("slide-show")) {
                    expose.attr("hidden", true);
                    expose.attr("aria-hidden", true);
                    hide.attr("hidden", false);
                    hide.attr("aria-hidden", false);
                    div.attr('aria-hidden', 'false');
                    window.myuw_log.log_card(card, "expand-myplan");
                } else {
                    window.myuw_log.log_card(card, "collapse-myplan");
                    setTimeout(function() {
                        expose.attr("hidden", false);
                        expose.attr("aria-hidden", false);
                        hide.attr("hidden", true);
                        hide.attr("aria-hidden", true);
                        div.attr("aria-hidden", true);
                    }, 700);
                }

            });

            // show hold details
            $('body').on('click', holds_class, function (ev) {
                ev.preventDefault();
                var card = $(ev.target).closest("[data-type='card']");

                var div, expose, hide;
                if (summer_card_label) {
                    div = $("#reg_holds_"+summer_card_label);
                    expose = $("#show_reg_holds_wrapper_"+summer_card_label);
                    hide = $("#hide_reg_holds_wrapper_"+summer_card_label);
                }
                else {
                    div = $("#reg_holds");
                    expose = $("#show_reg_holds_wrapper");
                    hide = $("#hide_reg_holds_wrapper");
                }

                div.toggleClass("slide-show");

                if (div.hasClass("slide-show")) {
                    expose.attr("hidden", true);
                    expose.attr("aria-hidden", true);
                    hide.attr("hidden", false);
                    hide.attr("aria-hidden", false);
                    div.attr("aria-hidden", false);
                    window.myuw_log.log_card(card, "expand-holds");
                }
                else {
                    window.myuw_log.log_card(card, "collapse-holds");
                    setTimeout(function () {
                        expose.attr("hidden", false);
                        expose.attr("aria-hidden", false);
                        hide.attr("hidden", true);
                        hide.attr("aria-hidden", true);
                        div.attr("aria-hidden", true);
                    }, 700);
                }
            });

        })(summer_label);
    },

    _render: function () {
        var next_term_data = WSData.oquarter_data().next_term_data;
        var reg_next_quarter = next_term_data.quarter;

        if (! window.card_display_dates.myplan_peak_load &&
            ! WSData.myplan_data(next_term_data.year, next_term_data.quarter)) {
            WSData.fetch_myplan_data(next_term_data.year,
                                     next_term_data.quarter,
                                     RegStatusCard.render_upon_data,
                                     RegStatusCard.render_error);
            return;
        }

        var myplan_data;
        if (! window.card_display_dates.myplan_peak_load) {
            myplan_data = WSData.myplan_data(next_term_data.year,
                                             next_term_data.quarter);
        }

        if (window.card_display_dates.myplan_peak_load || myplan_data) {

            var content = RegStatusCard._render_for_term(myplan_data,
                                                         reg_next_quarter);
            if (!content) {
                RegStatusCard.dom_target.hide();
                return;
            }

            RegStatusCard.dom_target.html(content);
            RegStatusCard._add_events();
            LogUtils.cardLoaded(RegStatusCard.name,
                                RegStatusCard.dom_target);
        }
    }
};
