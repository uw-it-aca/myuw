var CourseCards = {
    name: 'CourseCards',
    dom_target: undefined,
    term: 'current',

    render_init: function() {
        if (!window.user.grad && !window.user.undergrad) {
            $("#CourseCards").hide();
            return;
        }

        WSData.fetch_course_data_for_term(CourseCards.term, CourseCards.render_upon_data, CourseCards.render_error);
    },

    render_upon_data: function() {
        if (!CourseCards._has_all_data()) {
            return;
        }
        CourseCards._render();
        LogUtils.cardLoaded(CourseCards.name, CourseCards.dom_target);
    },

    render_error: function() {
        var error_code = WSData.course_data_error_code();
        if (error_code == 410) {
            Error410.render();
            return;
        }
        var raw = (error_code === 404
                   ? CardWithNoCourse.render(CourseCards.term)
                   : CardWithError.render("Course Information"));
        if (CourseCards.term === "current") {
            CourseCards.dom_target.html(raw);
        } else {
            $("#future_content").html(raw);
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_course_data(CourseCards.term)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var term = CourseCards.term;
        var course_data = WSData.normalized_course_data(term);

        if (term === 'current' && window.card_display_dates.in_coursevel_fetch_window) {
            WSData.fetch_iasystem_data(LoadCourseEval.render_upon_data, null);
        }

        var source = $("#course_card_list").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);
        CourseCards.dom_target.html(raw);

        LoadCourseEval.render(term, false);

        CourseCards.add_events(term);
    },

    add_events: function(term) {
        $(".course_website").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".lib_subject_guide").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_lib_subject_guide_"+course_id, term);
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

        $(".show_course_textbook").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("href");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_textbook_"+course_id, term);
        });

        $(".instructor").on("click", function(ev) {
            WSData.log_interaction("view_instructor_from_course_list", term);
            var hist = window.History;
            if (term) {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel,
                    term: term
                },  "", "/instructor/"+term+"/"+ev.target.rel);
            }
            else {
                hist.pushState({
                    state: "instructor",
                    instructor: ev.target.rel
                },  "", "/instructor/"+ev.target.rel);
            }
            return false;
        });
    },
};
