var RegStatusCard = {
    name: 'RegStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student ||
            !(window.card_display_dates.is_after_start_of_registration_display_period &&
              window.card_display_dates.is_before_end_of_registration_display_period)) {
            $("#RegStatusCard").hide();
            return;
        }

        WSData.fetch_notice_data(RegStatusCard.render_upon_data,RegStatusCard.render_error);
        WSData.fetch_oquarter_data(RegStatusCard.render_upon_data, RegStatusCard.render_error);
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
        // neither api data returns 404
        // if oquarter data or notice data failed, display error
        RegStatusCard.dom_target.html(CardWithError.render("Registration"));
    },

    _render_for_term: function(quarter, summer_card_label) {
        var reg_notices = Notices.get_notices_for_tag("reg_card_messages");
        var reg_holds = Notices.get_notices_for_tag("reg_card_holds");
        var reg_date = Notices.get_notices_for_tag("est_reg_date");
        var i, j;

        // Filter estimated registration dates for summer...
        var display_reg_dates = [];
        for (i = 0; i < reg_date.length; i++) {
            var notice = reg_date[i];
            for (j = 0; j < notice.attributes.length; j++) {
                var attribute = notice.attributes[j];
                if (quarter == "Summer") {
                    if ((attribute.name == "Quarter") && (attribute.value == "Summer")) {
                        display_reg_dates.push(notice);
                    }
                }
                else {
                    if ((attribute.name == "Quarter") && (attribute.value != "Summer")) {
                        display_reg_dates.push(notice);
                    }
                }
            }
        }

        var year, has_registration, next_term_data;
        if (quarter == "Summer") {
            next_term_data = WSData.oquarter_data().next_term_data;
            var terms = WSData.oquarter_data().terms;
            year = next_term_data.year;

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

        var finaid_tags = ["reg_summeraid_avail_title"];

        var financial_aid_notices = Notices.get_ordered_finaid_notices(finaid_tags);

        // Bug MUWM-3306
        var hide_card = true;
        if (financial_aid_notices && financial_aid_notices.length) {
            hide_card = false;
        }
        if (display_reg_dates.length) {
            hide_card = false;
        }
        if (reg_holds.length) {
            hide_card = false;
        }

        if (hide_card) {
            return;
        }

        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var template_data = {"finaid_notices": financial_aid_notices,
                             "reg_notices": reg_notices,
                             "reg_holds": reg_holds,
                             "card": summer_card_label,
                             "is_tacoma": window.user.tacoma,
                             "is_bothell": window.user.bothell,
                             "is_seattle": window.user.seattle,
                             "hold_count": reg_holds.length,
                             "est_reg_date": display_reg_dates,
                             "reg_next_quarter" : quarter,
                             "reg_next_year": year,
                            };
        var raw = template(template_data);
        return raw;
    },

    _add_events: function(summer_label) {
        // show registration resources
        var id, holds_class;
        if (summer_label) {
            id = "#show_reg_resources_"+summer_label;
            holds_class = ".reg_disclosure_"+summer_label;
        }
        else {
            id = "#show_reg_resources";
            holds_class = ".reg_disclosure";
        }

        // Prevent a closure on card
        (function(label) {
            $('body').on('click', id, function (ev) {
                var div, expose;
                if (label) {
                    // summer reg card
                    div = $("#reg_resources_"+label);
                    expose = $("#show_reg_resources_"+label);
                }
                else {
                    div = $("#reg_resources");
                    expose = $("#show_reg_resources");
                }

                ev.preventDefault();
                var card = $(ev.target).closest("[data-type='card']");
                div.toggleClass("slide-show");

                if (div.hasClass("slide-show")) {
                    expose.text("Show less");
                    div.attr('aria-hidden', 'false');
                    expose.attr('title', 'Collapse to hide additional registration resources');
                    window.myuw_log.log_card(card, "expand");
                } else {
                    div.attr('aria-hidden', 'true');
                    expose.attr('title', 'Expand to show additional registration resources');
                    window.myuw_log.log_card(card, "collapse");
                    setTimeout(function() {
                        expose.text("Show more");
                    }, 700);
                }
            });

            // show hold details
            $('body').on('click', holds_class, function (ev) {
                ev.preventDefault();
                var div, expose, hide;
                if (label) {
                    div = $("#reg_holds_"+label);
                    expose = $("#show_reg_holds_"+label);
                    hide = $("#hide_reg_holds_"+label);
                }
                else {
                    div = $("#reg_holds");
                    expose = $("#show_reg_holds");
                    hide = $("#hide_reg_holds");
                }

                div.toggleClass("slide-show");
                if (div.hasClass("slide-show")) {
                    expose.hide();
                    hide.show();
                    window.myuw_log.log_card("RegHolds", "expand");
                }
                else {
                    window.myuw_log.log_card("RegHolds", "collapse");
                    setTimeout(function () {
                        expose.show();
                        hide.hide();
                    }, 700);
                }
            });

        })(summer_label);
    },

    _render: function () {
        var next_term_data = WSData.oquarter_data().next_term_data;
        var reg_next_quarter = next_term_data.quarter;
        var content = RegStatusCard._render_for_term(reg_next_quarter);

        if (!content) {
            RegStatusCard.dom_target.hide();
            return;
        }

        RegStatusCard.dom_target.html(content);
        RegStatusCard._add_events();
        LogUtils.cardLoaded(RegStatusCard.name, RegStatusCard.dom_target);
    }
};
