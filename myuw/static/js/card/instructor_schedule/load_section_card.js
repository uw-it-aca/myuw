var InstructorSectionCard = {
    name: 'InstructorSectionCard',
    dom_target: undefined,
    section: null,
    term: null,

    render_init: function() {
        if ('section_data' in window &&
            'section' in window.section_data) {
            InstructorSectionCard.section = window.section_data.section;
            match = window.section_data.section.match(/(\d{4},[a-zA-Z]+),.*/);
            if (match && match[1]) {
                InstructorSectionCard.term = match[1].toLowerCase();
            }

            WSData.fetch_instructed_section_data(InstructorSectionCard.section,
                                                 InstructorSectionCard.render_upon_data,
                                                 InstructorSectionCard.render_error);
        } else {
            $("#InstructorSectionCard").hide();
        }
    },

    render_upon_data: function() {
        if (!InstructorSectionCard._has_all_data()) {
            return;
        }
        InstructorSectionCard._render();
        LogUtils.cardLoaded(InstructorSectionCard.name, InstructorSectionCard.dom_target);
    },

    render_error: function() {
        var error_code = WSData.instructed_section_data_error_code(InstructorSectionCard.section),
            source,
            course_template;

        if (error_code == 410) {
            Error410.render();
            return;
        }

        if (error_code === 403) {
            source = $("#instructor_section_card_not_instructor").html();
            courses_template = Handlebars.compile(source);
            InstructorSectionCard.dom_target.html(courses_template());
        } else if (error_code === 404) {
            source = $("#instructor_section_card_no_course").html();
            courses_template = Handlebars.compile(source);
            InstructorSectionCard.dom_target.html(courses_template());
        } else {
            source = CardWithError.render("Teaching Section");
            InstructorSectionCard.dom_target.html(source);
        }
    },

    _has_all_data: function () {
        if (WSData.normalized_instructed_section_data(InstructorSectionCard.section)) {
            return true;
        }
        return false;
    },

    _render: function () {
        var section = InstructorSectionCard.section;
        var course_data = WSData.normalized_instructed_section_data(InstructorSectionCard.section);
        var source = $("#instructor_section_card_panel").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);

        InstructorSectionCard.dom_target.html(raw);

        var course_sections = course_data.sections;
        $.each(course_sections, function () {
            this.year = course_data.year;
            this.quarter = course_data.quarter;
            this.summer_term = course_data.summer_term;
            this.time_schedule_published = course_data.term.time_schedule_published;
            this.registration_start = course_data.term.registration_periods[0].start;
            InstructorCourseCardContent.render(this, null);
        });
    }
};
