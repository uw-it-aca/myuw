var FinalExams = {
    show_finals: function() {
        showLoading();
        WSData.fetch_course_data(FinalExams.render_exams, []);
    },

    render_exams: function() {
        var course_data = WSData.course_data();
        var index = 0;
        var tbd_or_nonexistent = [];
        var scheduled_finals = [];

        var max_date, min_date;

        source = $("#quarter-list-finals").html();
        template = Handlebars.compile(source);
        $("#page-header").html(template({year: course_data.year, quarter: course_data.quarter}));

        for (index = 0; index < course_data.sections.length; index++) {
            var section = course_data.sections[index];
            if (section.final_exam) {
                var final_exam = section.final_exam;
                var start_date = new Date(final_exam.start_date);

                if (final_exam.start_date) {
                    if (max_date == null || max_date < start_date) {
                        max_date = start_date;
                    }
                    if (min_date == null || min_date > start_date) {
                        min_date = start_date;
                    }
                    scheduled_finals.push(section);
                }
                else {
                    tbd_or_nonexistent.push(section);
                }
            }
            else {
                tbd_or_nonexistent.push(section);
            }
        }

        // This shouldn't happen, but if we have over a week span of finals, just list them out.
        var over_one_week = [];
        if (scheduled_finals.length) {
            if ((max_date - min_date) > (60 * 60 * 24 * 7)) {
                over_one_week = scheduled_finals;
            }
            else {
            }
        }


        var template_data = {
            tbd: tbd_or_nonexistent,
            over_one_week: over_one_week
        };

        var source = $("#final_exams").html();
        var template = Handlebars.compile(source);
        $("#courselist").html(template(template_data));

    }
};

 
