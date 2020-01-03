var InstructorCourseCards = {
    name: 'InstructorCourseCards',
    dom_target: undefined,
    term: 'current',

    hide_card: function() {
        if (window.user.instructor) {
            return false;
        }
        return true;
    },

    render_init: function() {
        if (InstructorCourseCards.hide_card()) {
            $("#InstructorCourseCards").hide();
            return;
        }

        if (InstructorCourseCards.term === 'current') {
            InstructorCourseCards.term = window.term.display_term;
        }

        WSData.fetch_instructed_course_data_for_term(InstructorCourseCards.term,
                                                     InstructorCourseCards.render_upon_resp,
                                                     InstructorCourseCards.render_upon_resp);
    },

    render_upon_resp: function() {
        var error_code = WSData.instructed_course_data_error_code(InstructorCourseCards.term);
        if (error_code) {
            InstructorCourseCards._render_error(error_code);
            return;
        }
        InstructorCourseCards._render();
        LogUtils.cardLoaded(InstructorCourseCards.name, InstructorCourseCards.dom_target);
    },

    _render_error: function(error_code) {
        if (error_code === 410) {
            Error410.render();
            return;
        }

        if (error_code === 404) {
            if ($('.instructed-terms').length) {
                InstructorCourseCards._render_no_courses_found();
            } else {
                $("#InstructorCourseCards").hide();
            }
        } else {
            raw = CardWithError.render("Teaching Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _render_no_courses_found: function() {
        var source = $("#instructor_course_card_no_courses").html();
        var courses_template = Handlebars.compile(source);
        $(".instructor_cards .instructor-course-card").remove();
        $(".instructor_cards .myuw-card").remove();
        $(".instructor_cards").append(courses_template());

        $("div[data-tab-type='instructor-term-nav']").removeClass("myuw-tab-selected");
        $("div[data-tab-type='instructor-term-nav'][data-term='"+InstructorCourseCards.term+"']").addClass("myuw-tab-selected");
        $("#teaching-term-select option[value='"+InstructorCourseCards.term+"']").prop('selected', true);
        InstructorCourseCards._show_correct_term_dropdown();
    },

    _show_correct_term_dropdown: function() {
        var has_active = $("div[data-tab-type='instructor-term-nav'].myuw-tab-selected").length;
        if (has_active) {
            $("#teaching-term-select option[value='']").prop('selected', 'selected');
            $("#teaching-term-select option[value='']").prop('disabled', false);
            $("#teaching-term-select").removeClass('myuw-dropmenu-selected');
        }
        else {
            $("div[data-tab-type='instructor-term-nav'] a[aria-selected='true']").attr({
                "aria-selected" : "false"
            });
            $("#teaching-term-select option[value='']").prop('disabled', 'disabled');
            $("#teaching-term-select").addClass('myuw-dropmenu-selected');
        }
    },

    _render: function () {
        Handlebars.registerPartial('term_panel', $("#term_panel").html());
        var term = InstructorCourseCards.term;
        var course_data = WSData.instructed_course_data(term, true);
        var source = $("#instructor_course_card_list").html();
        var courses_template = Handlebars.compile(source);

        var i = 0,
            tab_terms = [],
            number_to_add = 0;

        for (i = 0; i < course_data.related_terms.length; i++) {
            if (course_data.related_terms[i].is_current) {
                number_to_add = 4;
            }
            if (number_to_add > 0) {
                tab_terms.push(course_data.related_terms[i]);
                number_to_add--;
            }
        }

        $.each(course_data.related_terms, function () {
            var term_id = this.year +","+this.quarter.toLowerCase();
            if (term_id === InstructorCourseCards.term) {
                this.matching_term = true;
            }
            else {
                this.matching_term = false;
            }
        });

        course_data.tab_terms = tab_terms;
        course_data.reversed_related_terms = course_data.related_terms.slice().reverse();
        var raw = courses_template(course_data);
        InstructorCourseCards.dom_target.html(raw);

        if (course_data.sections.length === 0) {
            InstructorCourseCards._render_no_courses_found();
        } else {
            $.each(course_data.sections, function () {
                InstructorCourseCardContent.render(this, null);
            });
        }

        InstructorCourseCards.add_events(InstructorCourseCards.term);
        InstructorCourseCards._show_correct_term_dropdown();

        if (window.location.hash) {
            var l = $('div[data-identifier="' +
                      window.location.hash.substr(1).replace(/-/g, ' ') +
                      '"]');
            if (l.length) {
                setTimeout(function () {
                    $('html,body').animate({scrollTop: l.offset().top},'slow');
                }, 250);
            }
        }
    },

    add_events: function(term) {
        try{
            $('[data-toggle="popover"]').popover();
        }
        catch(err){}

        $(document).on('click', 'a[href^="#"]', function (event) {
            event.preventDefault();
            $('html,body').animate({scrollTop:
                $($.attr(this, 'href')).offset().top},'slow');
        });

        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".show_map").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });

        $(".course_canvas_site").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });

        $(".instructed-terms").change(function(ev) {
            InstructorCourseCards.term = $(ev.target).find(':selected').val();
            InstructorCourseCards.render_init();
            WSData.log_interaction("show_instructed_courses_for_" +
                                   InstructorCourseCards.term);
        });

        $(".tab-nav-terms").click(function(ev) {
            InstructorCourseCards.term = $(ev.target).attr('data-term');
            InstructorCourseCards.render_init();
            WSData.log_interaction("show_instructed_courses_for_" +
                                   InstructorCourseCards.term);
            return false;
        });
        $(".close-mini-card").click(function(ev) {
            ev.preventDefault();
            var section_abbr = ev.currentTarget.getAttribute("cabb");
            var course_number = ev.currentTarget.getAttribute("cnum");
            var section_id = ev.currentTarget.getAttribute("sid");
            var label = safe_label(section_abbr) + "_" + course_number + "_" + section_id;
            WSData.log_interaction("close_mini_card_of_" + label, term);
            var section_label = (term + "," + section_abbr + "," +
                                 course_number + "/" + section_id);
            $.ajax({
                url: "/api/v1/inst_section_display/" + section_label + "/close_mini",
                dataType: "JSON",
                async: true,
                type: 'GET',
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.done) {
                        window.location = "/teaching/" + term;
                    }
                },
                error: function(xhr, status, error) {
                    return false;
                }
            });
        });
        $(".pin-mini-card").click(function(ev) {
            ev.preventDefault();
            var section_abbr = ev.currentTarget.getAttribute("cabb");
            var course_number = ev.currentTarget.getAttribute("cnum");
            var section_id = ev.currentTarget.getAttribute("sid");
            var label = safe_label(section_abbr) + "_" + course_number + "_" + section_id;
            WSData.log_interaction("pin_mini_card_of_" + label, term);
            var section_label = (term + "," + section_abbr + "," +
                                 course_number + "/" + section_id);
            $.ajax({
                url: "/api/v1/inst_section_display/" + section_label + "/pin_mini",
                dataType: "JSON",
                async: true,
                type: 'GET',
                accepts: {html: "text/html"},
                success: function(results) {
                    if (results.done) {
                        window.location = ev.currentTarget.href;
                    }
                },
                error: function(xhr, status, error) {
                    return false;
                }
            });
        });
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.InstructorCourseCards = InstructorCourseCards;
