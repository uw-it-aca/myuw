var InstructorCourseCards = {
    name: 'InstructorCourseCards',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (myuwFeatureDisabled('instructor_schedule')) {
            $("#InstructorCourseCards").hide();
            return;
        }

        WSData.fetch_instructed_course_data_for_term(InstructorCourseCards.term,
                                                     InstructorCourseCards.render_upon_data,
                                                     InstructorCourseCards.render_error);
    },

    render_upon_data: function() {
        if (!InstructorCourseCards._has_all_data()) {
            return;
        }
        InstructorCourseCards._render();
        LogUtils.cardLoaded(InstructorCourseCards.name, InstructorCourseCards.dom_target);
    },

    render_error: function() {
        var error_code = WSData.instructed_course_data_error_code(InstructorCourseCards.term);
        if (error_code == 410) {
            Error410.render();
            return;
        }

        if (error_code === 404) {
            // no instructed courses found
            $("#InstructorCourseCards").hide();
        } else {
            raw = CardWithError.render("Teaching Schedule");
            InstructorCourseCards.dom_target.html(raw);
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_instructed_course_data(InstructorCourseCards.term)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = InstructorCourseCards.term;
        var course_data = WSData.normalized_instructed_course_data(term);
        var source = $("#instructor_course_card_list").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);

        InstructorCourseCards.dom_target.html(raw);

        var course_sections = course_data.sections;
        var index;
        for (index = 0; index < course_sections.length; index++) {
            section = course_sections[index];
            section.year = course_data.year;
            section.quarter = course_data.quarter;
            section.summer_term = course_data.summer_term;

            InstructorCourseCardContent.render(section, null);
        }

        InstructorCourseCards.add_events(term);
    },

    add_events: function(term) {
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
    }
};
