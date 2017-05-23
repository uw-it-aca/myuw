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

        WebServiceData.require({notice_data: new NoticeData(),
                                oquarter_data: new OQuarterData(),
                                profile_data: new ProfileData()},
                               RegStatusCard.pre_render);
    },

    render_error: function(notice_resource_error, oquarter_resource_error, profile_resource_error) {
        if (notice_resource_error || oquarter_resource_error || profile_resource_error) {
            // none of the api data returns 404.
            // if any data failure, display error
            RegStatusCard.dom_target.html(CardWithError.render("Registration"));
            return true;
        }

        return false;
    },

    _render_for_term: function(myplan_data, quarter, oquarter_data, profile, summer_card_label) {
        var est_reg_date_notices = Notices.get_notices_for_tag("est_reg_date");
        var display_est_reg_date;
        var is_summer_reg = (quarter === "Summer");
        var reg_is_open = false;
        var is_my_1st_reg_day = false;
        var has_est_reg_date_notice = false;
        var pre_reg_notice = Notices.get_notices_for_tag("reg_card_messages");
        var reg_holds = Notices.get_notices_for_tag("reg_card_holds");
        var i, j, attribute;

        // Get estimated registration date for the quarter
        for (i = 0; i < est_reg_date_notices.length; i++) {
            var notice = est_reg_date_notices[i];
            var registration_date = null;

            // 1. Extract the registration date:
            for (j = 0; j < notice.attributes.length; j++) {
                attribute = notice.attributes[j];
                if (attribute.name == "Date") {
                    registration_date = attribute.value;
                    break;
                }
            }
            // 2. Determine the quarter
            for (j = 0; j < notice.attributes.length; j++) {
                attribute = notice.attributes[j];
                if ((is_summer_reg &&
                     attribute.name === "Quarter" &&
                     attribute.value === "Summer") ||
                    (attribute.name === "Quarter" &&
                     attribute.value === quarter)) {
                    has_est_reg_date_notice = true;
                    reg_is_open = notice.my_reg_has_opened;
                    is_my_1st_reg_day = notice.is_my_1st_reg_day;
                    display_est_reg_date = {"notice": notice,
                                            "date": registration_date };
                    break;
                }
            }
        }

        var year, has_registration, next_term_data;
        var financial_aid_notices;

        if (is_summer_reg) {
            var finaid_tags = ["reg_summeraid_avail_title"];
            financial_aid_notices = Notices.get_ordered_finaid_notices(finaid_tags);
            next_term_data = oquarter_data.next_term_data;
            year = next_term_data.year;

            var terms = oquarter_data.terms;
            for (i = 0; i < terms.length; i++) {
                var term = terms[i];
                if ((term.quarter == quarter) && term.section_count) {
                    has_registration = true;
                }
            }
        }
        else {
            next_term_data = oquarter_data.next_term_data;
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
        if (hide_card && display_est_reg_date) {
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

        // Retrieve pending majors and minors for this quarter, if they exist
        var pending_minors = [];
        var pending_majors = [];

        var retrieve_quarter_degrees = function(degrees, degree_type) {
            for (i = 0; i < degrees.length; i++) {
                if (degrees[i].quarter.toUpperCase() === quarter.toUpperCase() && degrees[i].year === year) {
                    if (degrees[i].degrees_modified && !degrees[i].has_only_dropped) {
                        return degrees[i][degree_type];
                    }
                }
            }
        };

        pending_minors = retrieve_quarter_degrees(profile.term_minors, "minors");
        pending_majors = retrieve_quarter_degrees(profile.term_majors, "majors");


        //Get hold count from notice attrs
        var hold_count = reg_holds.length;
        var source = $("#reg_status_card").html();
        var template = Handlebars.compile(source);
        var template_data = {
            "finaid_notices": financial_aid_notices,
            "pre_reg_notice": pre_reg_notice,
            "reg_holds": reg_holds,
            "card": summer_card_label,
            "registration_is_open": (reg_is_open || !has_est_reg_date_notice),
            "is_my_1st_reg_day": is_my_1st_reg_day,
            "is_tacoma": window.user.tacoma || window.user.tacoma_affil,
            "is_bothell": window.user.bothell || window.user.bothell_affil,
            "is_seattle": window.user.seattle || window.user.seattle_affil,
            "hold_count": reg_holds.length,
            "est_reg_date": display_est_reg_date,
            "reg_next_quarter" : quarter,
            "reg_next_year": year,
            "plan_data": plan_data,
            "myplan_peak_load": window.card_display_dates.myplan_peak_load,
            "pending_minors": pending_minors,
            "pending_majors": pending_majors
        };

        var raw = template(template_data);
        return raw;
    },

    _add_events: function(summer_label) {

        var card_disclosure_class, holds_class, unready_courses;
        if (summer_label) {
            card_disclosure_class = ".show_myplan_courses_"+summer_label;
            holds_class = ".reg_disclosure_"+summer_label;
            unready_courses = ".myplan_unready_courses_disclosure_"+summer_label;
        }
        else {
            card_disclosure_class = ".show_myplan_courses";
            holds_class = ".reg_disclosure";
            unready_courses = ".myplan_unready_courses_disclosure";
        }

        // show myplan courses
        (function(summer_card_label) {
            $('body').on('click', card_disclosure_class, function (ev) {
                ev.preventDefault();
                var card = $(ev.target).closest("[data-type='card']");

                var div, expose, hide;
                if (summer_card_label) {
                    // summer reg card
                    div = $("#myplan_courses_"+summer_card_label);
                    expose = $("#show_myplan_courses_wrapper_"+summer_card_label);
                    hide = $("#hide_myplan_courses_wrapper_"+summer_card_label);
                }
                else {
                    div = $("#myplan_courses");
                    expose = $("#show_myplan_courses_wrapper");
                    hide = $("#hide_myplan_courses_wrapper");
                }
                toggle_card_disclosure(card, div, expose, hide, "myplan_courses");
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
                toggle_card_disclosure(card, div, expose, hide, "myplan_unready_courses");
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
                toggle_card_disclosure(card, div, expose, hide, "reg_holds");
            });

        })(summer_label);
    },

    pre_render: function (resources) {
        var notice_resource = resources.notice_data;
        var oquarter_resource = resources.oquarter_data;
        var profile_resource = resources.profile_data;
        if (SummerRegStatusCard.render_error(otice_resource.error,
                                             oquarter_resource.error,
                                             profile_resource.error)) {
            return;
        }

        // _render should be called only once.
        if (renderedCardOnce(RegStatusCard.name)) {
            return;
        }

        var oquarter_data = oquarter_resource.data;
        var next_term_data = oquarter_data.next_term_data;
        var reg_next_quarter = next_term_data.quarter;
        if (! window.card_display_dates.myplan_peak_load) {
            WebServiceData.require({myplan_data: new MyPlanData(next_term_data.year,
                                                                next_term_data.quarter)},
                                   RegStatusCard.render,
                                   resources);
            return;
        }

        RegStatusCard.render(resources);
    },

    render: function (resources, myplan_resources) {
        var oquarter_resource = resources.oquarter_data;
        var profile_resource = resources.profile_data;
        var oquarter_data = oquarter_resource.data;
        var next_term_data = oquarter_data.next_term_data;
        var profile_data = profile_resource.data;
        var reg_next_quarter = next_term_data.quarter;

        var myplan_data;
        if (! window.card_display_dates.myplan_peak_load && myplan_resources.myplan_data) {
            if (myplan_resources) {
                myplan_data = myplan_resources.myplan_data.data;
            }
        }

        if (window.card_display_dates.myplan_peak_load || myplan_data) {
            var content = RegStatusCard._render_for_term(myplan_data,
                                                         reg_next_quarter,
                                                         profile_data,
                                                         oquarter_data);
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
