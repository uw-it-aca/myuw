var FinalExams = {
    FRIDAY: 5,
    SATURDAY: 6,
    SUNDAY: 0,
    show_finals: function(term, course_index) {
        showLoading();
        if (term) {
            WSData.fetch_course_data_for_term(term, FinalExams.render_exams, [term, course_index]);
        }
        else {
            WSData.fetch_current_course_data(FinalExams.render_exams, [term, course_index]);
        }
    },

    sort_by_finals_date: function(a, b) {
        var a_date = date_from_string(a.final_exam.start_date);
        var b_date = date_from_string(b.final_exam.start_date);

        return a_date - b_date;
    },
    render_exams: function(term, course_index) {
        var course_data;
        if (term) {
            course_data = WSData.course_data_for_term(term);
        }
        else {
            course_data = WSData.current_course_data();
        }
        var index = 0;
        var tbd_or_nonexistent = [];
        var scheduled_finals = [];

        var last_day_of_finals = date_from_string(course_data.term.last_final_exam_date);
        var max_date = last_day_of_finals;
        var min_date;

        // If there's something unexpected, show a list, not the visual schedule
        var show_list_instead_of_visual = false;

        var source;
        if (term) {
            source = $("#future-quarter-list-finals").html();
        } else {
            source = $("#quarter-list-finals").html();
        }
        template = Handlebars.compile(source);
        $("#page-header").html(template({
	    year: course_data.year,
	    quarter: course_data.quarter,
	    summer_term: course_data.summer_term
	}));

        for (index = 0; index < course_data.sections.length; index++) {
            var section = course_data.sections[index];
            // We need to set this here, since the code that displays links doesn't have access
            // to the full list of sections, necessarily
            section.index = index;
            if (section.final_exam) {
                var final_exam = section.final_exam;
                var start_date = date_from_string(final_exam.start_date);

                if (final_exam.start_date) {
                    if (max_date == null || max_date < start_date) {
                        max_date = start_date;
                    }
                    if (min_date == null || min_date > start_date) {
                        min_date = start_date;
                    }
                    if (start_date > last_day_of_finals) {
                        show_list_instead_of_visual = true;
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
        if (scheduled_finals.length) {
            if ((max_date - min_date) > (1000 * 60 * 60 * 24 * 7)) {
                show_list_instead_of_visual = true;
            }
        }

        // It's our current understanding that the last day of finals is always a friday -
        // grades are due on the following tuesday.  If the last day of finals isn't a friday,
        // fall back to the list view.
        if (last_day_of_finals.getDay() != FinalExams.FRIDAY) {
            show_list_instead_of_visual = true;
        }

        var over_one_week = [];
        var visual_data = {};

        if (show_list_instead_of_visual) {
            over_one_week = scheduled_finals.sort(FinalExams.sort_by_finals_date);
        }
        else if (course_data.quarter != "summer") {
            // summer quarter doesn't have properly scheduled finals
            visual_data = FinalExams._build_visual_schedule_data(scheduled_finals, course_data.term);
        }

        var template_data = {
            term: term,
            tbd: tbd_or_nonexistent,
            over_one_week: over_one_week,
            is_summer: (course_data.quarter == "summer"),
            visual_data: visual_data,
        };

        var source = $("#final_exams").html();
        var template = Handlebars.compile(source);
        $("#courselist").html(template(template_data));

        if (!course_index) {
            Modal.hide();
        }
        else {
            if (course_index < course_data.sections.length) {
                FinalsModal.show_finals_modal(term, course_index);
            }
        }

        $(".show_section_details").bind("click", function(ev) {
            var course_id = this.rel;
            var log_course_id = ev.currentTarget.getAttribute("class").replace(/[^a-z0-9]/gi, '_');

            if (term) {
                var logging_term = term.replace(/[^a-z0-9]/gi, '_');
                WSData.log_interaction("open_finals_modal_"+log_course_id+"_term_"+logging_term);
                var hist = window.History;
                hist.pushState({
                    state: "final_exams",
                    course_index: course_id,
                    term: term
                },  "", "/mobile/final_exams/"+term+"/"+course_id);
            }
            else {
                WSData.log_interaction("open_finals_modal_"+log_course_id);
                var hist = window.History;
                hist.pushState({
                    state: "final_exams",
                    course_index: course_id
                },  "", "/mobile/final_exams/"+course_id);

            }

            return false;
        });



    },

    _build_visual_schedule_data: function(sections_with_finals, term) {
        var visual_data = {
            latest_ending: 0,
            earliest_start: 24*60,
            monday: [],
            tuesday: [],
            wednesday: [],
            thursday: [],
            friday: [],
            saturday: [],
            sunday: [],
            display_hours: [],
            has_7_days: false,
            courses_meeting_tbd: [],
            end_date: term.last_final_exam_date
        };

        var index = 0;
        for (index = 0; index < sections_with_finals.length; index++) {
            var section = sections_with_finals[index];
            var final_exam = section.final_exam;

            var start_date = date_from_string(final_exam.start_date);
            var end_date = date_from_string(final_exam.end_date);

            if (start_date.getDay() == FinalExams.SATURDAY) {
                visual_data.has_7_days = true;
            }
            if (start_date.getDay() == FinalExams.SUNDAY) {
                visual_data.has_7_days = true;
            }

            var start_minutes = start_date.getHours() * 60 + start_date.getMinutes();
            var end_minutes = end_date.getHours() * 60 + end_date.getMinutes();

            if (start_minutes < visual_data.earliest_start) {
                visual_data.earliest_start = start_minutes;
            }
            if (end_minutes > visual_data.latest_ending) {
                visual_data.latest_ending = end_minutes;
            }

            var exam_info = {
                start: start_minutes,
                end: end_minutes,
                color_id: section.color_id,
                curriculum: section.curriculum_abbr,
                course_number: section.course_number,
                section_id: section.section_id,
                section_index: section.index,
                is_confirmed: final_exam.is_confirmed
            };

            var days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
            var day = start_date.getDay();
            visual_data[days[day]].push(exam_info);
        }

        // Make it so the start and end times are always on the hour:
        var start_hour = parseInt(visual_data.earliest_start / 60, 10);
        if ((start_hour * 60) === visual_data.earliest_start) {
            visual_data.start_time = (start_hour * 60) - 60;
        }
        else {
            visual_data.start_time = (start_hour * 60);
        }

        var end_hour = parseInt(visual_data.latest_ending / 60, 10) + 1;
        if ((end_hour * 60) === visual_data.latest_ending) {
            visual_data.end_time = (end_hour * 60) - 60;
        }
        else {
            visual_data.end_time = (end_hour * 60);
        }

        var i = 0;
        // We don't want to add the last hour - it's just off the end of the visual schedule
        for (i = visual_data.start_time; i <= visual_data.end_time - 1; i += 60) {
            visual_data.display_hours.push({
                hour: (i / 60),
                position: i
            });
        }

        visual_data.total_hours = (visual_data.end_time - visual_data.start_time) / 60;

        var hours_count = parseInt((visual_data.end_time - visual_data.start_time) / 60, 0);
        if (hours_count <= 6) {
            visual_data.schedule_hours_class = "six-hour";
        }
        else if (hours_count <= 12) {
            visual_data.schedule_hours_class = "twelve-hour";
        }
        else {
            visual_data.schedule_hours_class = "twelve-plus";
        }

        return visual_data;
    }
};

 
