var VisualScheduleCard = {
    name: 'VisualScheduleCard',
    dom_target: undefined,
    term: 'current',

    should_display_card: function() {
        if (!window.user.student ||
            !window.card_display_dates.is_before_last_day_of_classes) {
                if (!window.force_visual_schedule_display) {
                    return false;
                }
        }
        return true;
    },

    force_visual_schedule_display: function() {
        window.force_visual_schedule_display = true;
    },

    render_init: function(term, course_index) {
        if (!VisualScheduleCard.should_display_card()) {
            $("#VisualScheduleCard").hide();
            return;
        }
        WSData.fetch_course_data_for_term(VisualScheduleCard.term, VisualScheduleCard.render_upon_data, VisualScheduleCard.render_error);
    },

    _has_all_data: function () {
        if (WSData.normalized_course_data(VisualScheduleCard.term)) {
            return true;
        }
        return false;
    },

    render_error: function() {
        // CourseCards displays the message
        $("#VisualScheduleCard").hide();
    },

    render_upon_data: function(course_index) {
        if (!VisualScheduleCard._has_all_data()) {
            return;
        }
        VisualScheduleCard._render();
    },

    // The course_index will be given when a modal is shown.
    _render: function() {
        var term = VisualScheduleCard.term;
        var course_data = WSData.normalized_course_data(term);
        course_data.schedule_periods = VisualScheduleCard._get_schedule_periods(course_data);

        VisualScheduleCard.render_schedule(course_data, term);

        FinalExamSchedule.render(course_data, term, true);

        LogUtils.cardLoaded(VisualScheduleCard.name, VisualScheduleCard.dom_target);
    },

    _get_schedule_periods: function(course_data) {
        var schedule_periods = {};
        $(course_data.sections).each(function(idx, section){
            // get start and end dates for section
            var section_dates = VisualScheduleCard._get_dates_for_section(section);
            schedule_periods = VisualScheduleCard._add_to_periods(section_dates,
                                                                  section,
                                                                  schedule_periods);

            if(section.final_exam !== undefined &&
                section.final_exam.start_date !== undefined){
                schedule_periods = VisualScheduleCard._add_to_finals(section, schedule_periods);
            }
        });
        return VisualScheduleCard._format_dates(schedule_periods);
    },

    _format_dates: function(schedule_periods){
        for (var period_id in schedule_periods){
            schedule_periods[period_id].start_date = schedule_periods[period_id].start_date.format("YYYY-MM-DD");
            schedule_periods[period_id].end_date = schedule_periods[period_id].end_date.format("YYYY-MM-DD");
        }
        return schedule_periods;
    },

    _add_to_finals: function(section, schedule_periods){
        var week_range = VisualScheduleCard._get_week_range_from_date(section.final_exam.start_date);
        if ("finals" in schedule_periods){
            schedule_periods.finals.sections.push(section);
        } else {
            schedule_periods.finals =
            {"start_date": week_range[0],
                "end_date" : week_range[1],
                "sections": [section]
            };
        }
        return schedule_periods;
    },


    _add_to_periods: function(dates, section, periods){
        if(Object.keys(periods).length === 0){
            periods["0"] =
            {"start_date": dates[0],
                "end_date" : dates[1],
                "sections": [section]
            };
        } else {
            for (var period_key in periods){
                var period = periods[period_key];
                if(period.start_date.isSame(dates[0]) &&
                    period.end_date.isSame(dates[1])){
                    period.sections.push(section);
                    return periods;
                }
            }
            periods[Object.keys(periods).length] = {"start_date": dates[0],
                "end_date" : dates[1],
                "sections": [section]
            };
        }
    return periods;
    },

    _get_dates_for_section: function(section){
        var start_date = section.start_date,
            end_date = section.end_date;

        if(start_date === "None"){
            if (window.term.summer_term === "None"){
                start_date = window.term.first_day_quarter;
                end_date = window.term.last_day_instruction;
            }
        }
        return [moment(new Date(start_date)), moment(new Date(end_date))];
    },

    _get_week_range_from_date: function(date){
        var exam_date = moment(date);
        var start = exam_date.startOf('week');
        var end = exam_date.clone().endOf('week');

        return [start, end];
    },

    _get_data_for_period: function(course_data, term, period){
    var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        var visual_data = {
            has_early_fall_start: course_data.has_early_fall_start,
            is_pce: user.pce,
            total_sections: course_data.schedule_periods[period].sections.length,
            year: course_data.year,
            quarter: course_data.quarter,
            term: term,
            summer_term: course_data.summer_term,
            latest_ending: 0,
            earliest_start: 24*60,
            monday: [],
            tuesday: [],
            wednesday: [],
            thursday: [],
            friday: [],
            saturday: [],
            display_hours: [],
            has_6_days: false,
            courses_meeting_tbd: [],
            schedule_periods: course_data.schedule_periods
        };
        var day, day_index, i, height, top;

        var index = 0;
        for (index = 0; index < course_data.schedule_periods[period].sections.length; index++) {
            var section = course_data.schedule_periods[period].sections[index];
            var meeting_index = 0;
            for (meeting_index = 0; meeting_index < section.meetings.length; meeting_index++) {
                var meeting = section.meetings[meeting_index];

                if (!meeting.days_tbd) {

                    var start_parts = meeting.start_time.split(":");
                    var start_minutes = parseInt(start_parts[0], 10) * 60 + parseInt(start_parts[1], 10);


                    var end_parts = meeting.end_time.split(":");
                    var end_minutes = parseInt(end_parts[0], 10) * 60 + parseInt(end_parts[1], 10);

                    if (start_minutes < visual_data.earliest_start) {
                        visual_data.earliest_start = start_minutes;
                    }
                    if (end_minutes > visual_data.latest_ending) {
                        visual_data.latest_ending = end_minutes;
                    }

                    var meeting_info = {
                        is_meeting: true,
                        start: start_minutes,
                        end: end_minutes,
                        color_id: section.color_id,
                        curriculum: section.curriculum_abbr,
                        course_number: section.course_number,
                        term: term,
                        section_id: section.section_id,
                        section_index: index,
                        building_tbd: meeting.building_tbd,
                        building: meeting.building,
                        building_name: meeting.building_name,
                        room_tbd: meeting.room_tbd,
                        room: meeting.room,
                        latitude: meeting.latitude,
                        longitude: meeting.longitude,
                        early_fall_start: section.early_fall_start,
                        has_early_fall_start: course_data.has_early_fall_start
                    };

                    day_index = 0;
                    for (day_index = 0; day_index < days.length; day_index++) {
                        day = days[day_index];

                        if (meeting.meeting_days[day]) {
                            if (day === "saturday") {
                                visual_data.has_6_days = true;
                            }
                            visual_data[day].push(meeting_info);
                        }
                    }
                }
                else {
                    visual_data.courses_meeting_tbd.push({
                        color_id: section.color_id,
                        curriculum: section.curriculum_abbr,
                        course_number: section.course_number,
                        section_id: section.section_id,
                        section_index: index
                    });
                }
            }
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

        i = 0;
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
        if (!visual_data.has_6_days) {
            weekends = 5;
        }
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
    },
        
    render_schedule: function(course_data, term) {
        var visual_data = VisualScheduleCard._get_data_for_period(course_data, term, "0");
        VisualScheduleCard.shown_am_marker = false;

        source   = $("#visual_schedule_card_content").html();
        template = Handlebars.compile(source);
        VisualScheduleCard.dom_target.html(template(visual_data));

        VisualScheduleCard.add_events(term);
    },
            
    // This is the height of the days bar... needed for positioning math below
    day_label_offset: 0,

    get_scaled_percentage: function(pos, min, max) {
        var base_percentage = (pos - min) / (max - min);
        var offset_percentage = (VisualScheduleCard.day_label_offset * 2) + (base_percentage * (100 - (VisualScheduleCard.day_label_offset * 2)));

        // The second one is for positioning the last hour label.
        return offset_percentage - VisualScheduleCard.day_label_offset;
    },

    add_events: function(term) {
        $(".show_visual_map").on("click", function(ev) {
            var building_name = ev.currentTarget.getAttribute("rel");
            building_name = building_name.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_visual_card_"+building, term);
        });
        
        $("#toggle_finalexams").on("click", function(ev) {
            ev.preventDefault();
            $("#final_exam_schedule_panel").toggleClass("slide-show");
            if ($("#final_exam_schedule_panel").hasClass("slide-show")) {
                $("#toggle_finalexams").text("Hide Final Exam Schedule");
                $("#toggle_finalexams").attr('title', 'Hide Final Exam Schedule');
                window.myuw_log.log_card("FinalExam", "expand");
            }
            else {
                $("#toggle_finalexams").attr('title', 'Show Final Exam Schedule');
                window.myuw_log.log_card("FinalExam", "collapse");
                
                setTimeout(function() {
                      $("#toggle_finalexams").text("Show Final Exam Schedule");
               }, 700);
            }
        });

        $(".show_full_term_meetings").on("click", function(ev) {
            $(".efs_course").hide();
            $(".non_efs_course").show();
            $(".show_efs_meetings").show();
            $(".show_full_term_meetings").hide();
            return false;
        });
        $(".show_efs_meetings").on("click", function(ev) {
            $(".efs_course").show();
            $(".non_efs_course").hide();
            $(".show_full_term_meetings").show();
            $(".show_efs_meetings").hide();
            return false;
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.VisualScheduleCard = VisualScheduleCard;
