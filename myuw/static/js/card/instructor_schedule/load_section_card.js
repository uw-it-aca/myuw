var InstructorSectionCard = {
    name: 'InstructorSectionCard',
    dom_target: undefined,
    section: null,
    term: null,

    render_init: function() {
        if (window.hasOwnProperty('section_data') && 
            window.section_data.hasOwnProperty('section') && 
            myuwFeatureEnabled('instructor_schedule')) {
            InstructorSectionCard.section = window.section_data.section;
            match = window.section_data.section.match(/(\d{4},[a-zA-Z]+),.*/);
            if (match && match[1]) {
                InstructorSectionCard.term = match[1].toLowerCase();
            }

            WebServiceData.require({section_data: new InstructedSectionData(InstructorSectionCard.section)},
                                   InstructorSectionCard.render);
        } else {
            $("#InstructorSectionCard").hide();
        }
    },

    render_error: function(instructor_section_error) {
        if (instructor_section_error) {
            var error_code = instructor_section_error.status,
                source,
                course_template;

            if (error_code == 410) {
                Error410.render();
            } else if (error_code === 403) {
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

            return true;
        }

        return false;
    },

    render: function (resources) {
        var section = InstructorSectionCard.section;
        var course_data_resource = resources.section_data;

        if (InstructorSectionCard.render_error(course_data_resource.error)) {
            return;
        }

        var course_data = course_data_resource.data;
        var source = $("#instructor_section_card_panel").html();
        var courses_template = Handlebars.compile(source);
        var raw = courses_template(course_data);

        InstructorSectionCard.dom_target.html(raw);

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

        LogUtils.cardLoaded(InstructorSectionCard.name, InstructorSectionCard.dom_target);
    }
};
