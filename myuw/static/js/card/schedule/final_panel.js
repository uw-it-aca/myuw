var FinalExamSchedule = {
    FRIDAY: 5,
    SATURDAY: 6,
    SUNDAY: 0,

    sort_by_finals_date: function(a, b) {
        var a_date = date_from_string(a.final_exam.start_date);
        var b_date = date_from_string(b.final_exam.start_date);

        return a_date - b_date;
    },

    //render: function(student_course_data, instructed_course_data, term, show_title, dom_target) {
    render: function(course_data, term, show_title, dom_target) {
        var index = 0;
        var finals = {
            tbd_or_nonexistent: [],
            tbd_or_nonexistent_taught: [],
            scheduled_finals: [],
            last_day_of_finals: null,
            is_summer_qtr: false,
            term_data: null,
            max_date: null,
            min_date: null,
            // If there's something unexpected, show a list, not the visual schedule
            show_list_instead_of_visual: false
        };

        FinalExamSchedule.process_final_data(course_data, term, false, finals);

        // This shouldn't happen, but if we have over a week span of finals, just list them out.
        if (finals.scheduled_finals.length) {
            if ((finals.max_date - finals.min_date) > (1000 * 60 * 60 * 24 * 7)) {
                finals.show_list_instead_of_visual = true;
            }
        }

        // It's our current understanding that the last day of finals is always a friday -
        // grades are due on the following tuesday.  If the last day of finals isn't a friday,
        // fall back to the list view.

        if (finals.last_day_of_finals.day() !== FinalExamSchedule.FRIDAY) {
            finals.show_list_instead_of_visual = true;
        }

        var list_data = [];
        var visual_data = {};

        list_data = finals.scheduled_finals.sort(FinalExamSchedule.sort_by_finals_date);

        if (!finals.is_summer_qtr) {
            // summer quarter doesn't have properly scheduled finals
            visual_data = FinalExamSchedule._build_visual_schedule_data(finals.scheduled_finals, term);
        }

        var template_data = {
            show_title: show_title,
            term: term,
            tbd: finals.tbd_or_nonexistent,
            tbd_taught: finals.tbd_or_nonexistent_taught,
            list_data: list_data,
            is_summer: finals.is_summer_qtr,
            visual_data: visual_data,
        };
        var source = $("#final_exam_schedule_content").html();
        var template = Handlebars.compile(source);
        if(dom_target === undefined){
            dom_target = "#final_exam_schedule_panel";
        }
        $(dom_target).html(template(template_data));
        FinalExamSchedule.add_events(term);
    },

    process_final_data: function(course_data, term, for_instructor, finals) {
        var date = moment(term.last_final_exam_date);
        finals.last_day_of_finals = date;
        finals.is_summer_qtr = term.quarter === "summer";
        finals.term_data = term.term;
        $.each(course_data.sections, function (index) {
            var section = this;
            // We need to set this here, since the code that displays links doesn't have access
            // to the full list of sections, necessarily
            section.index = index;
            section.is_remote = section.is_remote;
            if (for_instructor){
                section.is_instructor = true;
            }
            if (section.final_exam && !section.final_exam.no_exam_or_nontraditional) {
                var final_exam = section.final_exam;
                var start_date = date_from_string(final_exam.start_date);

                if (final_exam.start_date) {
                    if (finals.max_date === null || finals.max_date < start_date) {
                        finals.max_date = start_date;
                    }
                    if (finals.min_date === null || finals.min_date > start_date) {
                        finals.min_date = start_date;
                    }
                    if (start_date > finals.last_day_of_finals) {
                        finals.show_list_instead_of_visual = true;
                    }
                    if (section.is_remote) {
                        final_exam.is_remote = section.is_remote;
                    } else if (final_exam.building === "*") {
                        final_exam.building_tbd = true;
                    }
                    finals.scheduled_finals.push(section);
                }
                else {
                    if(for_instructor){
                        finals.tbd_or_nonexistent_taught.push(section);
                    } else {
                        finals.tbd_or_nonexistent.push(section);
                    }

                }
            }
            else {
                if(for_instructor){
                    finals.tbd_or_nonexistent_taught.push(section);
                } else {
                    finals.tbd_or_nonexistent.push(section);
                }
            }
        });
    },

    add_events: function(term) {
        $(".show_final_map").on("click", function(ev) {
            var building_name = ev.currentTarget.getAttribute("rel");
            building_name = building_name.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_final_card_"+building, term);
        });
    },

    _build_visual_schedule_data: function(sections_with_finals, term) {
        var days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
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

        var index = 0,
            day,
            top,
            height;
        for (index = 0; index < sections_with_finals.length; index++) {
            var section = sections_with_finals[index];
            var final_exam = section.final_exam;

            var start_date = date_from_string(final_exam.start_date);
            var end_date = date_from_string(final_exam.end_date);

            if (start_date.getDay() === FinalExamSchedule.SATURDAY) {
                visual_data.has_7_days = true;
            }
            if (start_date.getDay() === FinalExamSchedule.SUNDAY) {
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
                is_remote: section.is_remote,
                is_meeting: true,
                start: start_minutes,
                end: end_minutes,
                color_id: section.color_id,
                curriculum: section.curriculum_abbr,
                course_number: section.course_number,
                section_id: section.section_id,
                section_index: section.index,
                room_number: final_exam.room_number,
                building: final_exam.building,
                building_tbd: final_exam.building_tbd,
                building_name: final_exam.building_name,
                latitude: final_exam.latitude,
                longitude: final_exam.longitude,
                is_instructor: section.is_teaching,
                is_confirmed: final_exam.is_confirmed,
                quarter: term.quarter,
                year: term.year,
                sln: section.sln,
                netid: window.user.netid
            };

            day = start_date.getDay();
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
        var position_index = 0;
        // We don't want to add the last hour - it's just off the end of the visual schedule
        for (i = visual_data.start_time; i <= visual_data.end_time - 1; i += 60) {
            visual_data.display_hours.push({
                hour: (i / 60),
                position: i,
                hour_count: position_index
            });
            position_index += 1;
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

        var weekends = days.length;
        if (!visual_data.has_7_days) {
            weekends = 6;
        }
        var day_index;
        for (day_index = 0; day_index < weekends; day_index++) {
            day = days[day_index];
            i = 0;
            while (i < visual_data[day].length) {
                top = VisualScheduleCard.get_scaled_percentage(visual_data[day][i].start, visual_data.start_time, visual_data.end_time);
                height =  VisualScheduleCard.get_scaled_percentage(visual_data[day][i].end, visual_data.start_time, visual_data.end_time) - top;
                visual_data[day][i].top=top;
                visual_data[day][i].height=height;
                i += 1;
            }

            var start_at_hr = true;
            var position_start = visual_data.start_time;
            while (position_start < visual_data.end_time) {
                var position_end = position_start + 30;
                top = VisualScheduleCard.get_scaled_percentage(position_start, visual_data.start_time, visual_data.end_time);
                height =  VisualScheduleCard.get_scaled_percentage(position_end, visual_data.start_time, visual_data.end_time) - top;
                visual_data[day].push({
                    is_meeting: false,
                    start_at_hr: start_at_hr,
                    top:top,
                    height:height,
                    start: position_start,
                    end: position_end});
                position_start = position_end;
                start_at_hr = !start_at_hr;
            }
        }
        return visual_data;
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.FinalExamSchedule = FinalExamSchedule;
