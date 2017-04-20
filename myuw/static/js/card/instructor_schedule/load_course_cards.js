var InstructorCourseCards = {
    name: 'InstructorCourseCards',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (myuwFeatureEnabled('instructor_schedule')) {
            if (InstructorCourseCards.term === 'current') {
                InstructorCourseCards.term = window.term.year + ',' + window.term.quarter;
            }

            WebServiceData.require([new InstructedCourseData(InstructorCourseCards.term)],
                                   InstructorCourseCards.render);
        } else {
            $("#InstructorCourseCards").hide();
        }
    },

    render_error: function(instructed_course_resource) {
        var error_code = instructed_course_resource.error ? instructed_course_resource.error.status : null;

        if (error_code == 410) {
            Error410.render();
            return true;
        }

        if (error_code === 404) {
            // no instructed courses found
            if ($('.instructed-terms').length) {
                var source = $("#instructor_course_card_no_courses").html();
                var courses_template = Handlebars.compile(source);
                $(".instructor_cards .card").remove();
                $(".instructor_cards").append(courses_template());
            } else {
                $("#InstructorCourseCards").hide();
            }

            return true;
        } else if (error_code) {
            raw = CardWithError.render("Teaching Schedule");
            InstructorCourseCards.dom_target.html(raw);
            return true;
        }

        return false;
    },

    render: function (instructed_course_resource) {
        if (InstructorCourseCards.render_error(instructed_course_resource)) {
            return;
        }

        var course_data = instructed_course_resource.normalized();
        var source = $("#instructor_course_card_list").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);

        InstructorCourseCards.dom_target.html(raw);

        var course_sections = course_data.sections;
        $.each(course_sections, function () {
            this.year = course_data.year;
            this.quarter = course_data.quarter;
            this.summer_term = course_data.summer_term;
            if (course_data.future_term) {
                InstructorFutureCourseCardContent.render(this, null);
            } else if (course_data.past_term) {
                InstructorPastCourseCardContent.render(this, null);
            } else {
                InstructorCourseCardContent.render(this, null);
            }
        });

        InstructorCourseCards.add_events();
        LogUtils.cardLoaded(InstructorCourseCards.name, InstructorCourseCards.dom_target);
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

        $(".instructed-terms").change(function(ev) {
            InstructorCourseCards.term = $('.instructed-terms option:selected').val();
            InstructorCourseCards.render_init();
            WSData.log_interaction("show_instructed_courses_for_" +
                                   InstructorCourseCards.term);
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructorCourseCards = InstructorCourseCards;
