var RegStatusCard = {
    name: 'RegStatusCard',
    dom_target: undefined,

    render_init: function() {
        if (window.card_display_dates.is_after_start_of_registration_display_period &&
            window.card_display_dates.is_before_end_of_registration_display_period) {
            WSData.fetch_notice_data(RegStatusCard.render_upon_data,RegStatusCard.render_error);
            WSData.fetch_oquarter_data(RegStatusCard.render_upon_data, RegStatusCard.render_error);
        }
        else {
            $("#RegStatusCard").hide();
        }
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
    render_error: function () {
        RegStatusCard.dom_target.html(CardWithError.render("Registration"));
    },

    _render: function () {
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var reg_notices = Notices.get_notices_for_tag("reg_card_messages");
        var reg_holds = Notices.get_notices_for_tag("reg_card_holds");
        var reg_date = Notices.get_notices_for_tag("est_reg_date");     
        
        var next_term_data = WSData.oquarter_data()["next_term_data"];
        var reg_next_quarter = next_term_data["quarter"];
        var reg_next_year = next_term_data["year"];
        var has_registration = next_term_data["has_registration"];

        if (has_registration) {
            RegStatusCard.dom_target.hide();
            return;
        }
        
        //Get hold count from notice attrs
        var hold_count = reg_holds.length;

        // show registration resources
        $('body').on('click', '#show_reg_resources', function (ev) {

            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");

            $("#reg_resources").toggleClass("slide-show");

            if ($("#reg_resources").hasClass("slide-show")) {
                $("#show_reg_resources").text("Show less")
                $("#reg_resources").attr('aria-hidden', 'false');
                $("#show_reg_resources").attr('title', 'Collapse to hide additional registration resources');
                window.myuw_log.log_card(card, "expand");
            } else {

                $("#reg_resources").attr('aria-hidden', 'true');
                $("#show_reg_resources").attr('title', 'Expand to show additional registration resources');
                window.myuw_log.log_card(card, "collapse");

                setTimeout(function() {
                    $("#show_reg_resources").text("Show more");
                }, 700);
            }
        });
        
        // show hold details
        $("#show_reg_holds").text("Show " + hold_count + " holds");
        $('body').on('click', '.reg_disclosure', function (ev) {
            ev.preventDefault();

            $("#reg_holds").toggleClass("slide-show");
            if ($("#reg_holds").hasClass("slide-show")) {
                $("#show_reg_holds").hide();
                $("#hide_reg_holds").show();
                window.myuw_log.log_card("RegHolds", "expand");
            }
            else {
                window.myuw_log.log_card("RegHolds", "collapse");
                setTimeout(function () {
                    $("#show_reg_holds").show();
                    $("#hide_reg_holds").hide();
                }, 700);
            }
        });

        RegStatusCard.dom_target.html(template({"reg_notices": reg_notices,
                                                "reg_holds": reg_holds,
                                                "is_tacoma": window.user.tacoma,
                                                "is_bothell": window.user.bothell,
                                                "is_seattle": window.user.seattle,
                                                "hold_count": hold_count,
                                                "est_reg_date": reg_date,
                                                "reg_next_quarter" : reg_next_quarter,
                                                "reg_next_year": reg_next_year
                                                }));
    }
};
