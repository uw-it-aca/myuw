var VisualScheduleCard = {
    name: 'VisualScheduleCard',
    dom_target: undefined,
    term: 'current',

    should_display_card: function() {
        if (!(window.user.student || window.user.is_instructor) || 
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
        WSData.fetch_instructed_course_data_for_term(VisualScheduleCard.term, VisualScheduleCard.render_upon_data, VisualScheduleCard.render_error);
    },

    _has_all_data: function () {
        var course_data = WSData.normalized_course_data(VisualScheduleCard.term);
        var instructed_course_data = WSData.normalized_instructed_course_data(VisualScheduleCard.term)
        var course_err_status = WSData.course_data_error_code(VisualScheduleCard.term);
        var instructed_course_err_status = WSData.instructed_course_data_error_code(VisualScheduleCard.term);

        return ((course_data ||
                 (course_data === undefined && course_err_status === 404)) &&
                (instructed_course_data || 
                 (instructed_course_data === undefined && instructed_course_err_status === 404)));
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
        var instructed_course_data = WSData.normalized_instructed_course_data(term)

        $("#VisualScheduleCard").show();
        VisualScheduleCard.render_schedule(course_data, instructed_course_data, term);

//        FinalExamSchedule.render(course_data, term, true);

        LogUtils.cardLoaded(VisualScheduleCard.name, VisualScheduleCard.dom_target);
    },
        
    render_schedule: function(course_data, instructed_course_data, term) {
        VisualScheduleCard.shown_am_marker = false;
        var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        var visual_data = {
            has_early_fall_start: (course_data && course_data.has_early_fall_start),
            is_pce: user.pce,
            total_sections: ((course_data) ? course_data.sections.length : 0) + 
                ((instructed_course_data) ? instructed_course_data.sections.length : 0) ,
            year: (course_data) ? course_data.year : instructed_course_data.year,
            quarter: (course_data) ? course_data.quarter : instructed_course_data.quarter,
            term: term,
            summer_term: (course_data) ? course_data.summer_term : instructed_course_data.summer_term,
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
            is_instructor: false
        };

        var set_meeting = function(course_data, meeting, index, is_instructor) {
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
                    is_instructor: is_instructor,
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

                $.each(days, function (day_index) {
                    day = this;
                    if (meeting.meeting_days[day]) {
                        if (day === "saturday") {
                            visual_data.has_6_days = true;
                        }
                        visual_data[day].push(meeting_info);
                    }
                });
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
        };
        var day, day_index, i, height, top;

        if (course_data) {
            $.each(course_data.sections, function (index) {
                $.each(this.meetings, function (meeting_index) {
                    set_meeting(course_data, this, index, false);
                });
            });
        }

        if (instructed_course_data) {
            visual_data.is_instructor = true;
            $.each(instructed_course_data.sections, function (index) {
                $.each(this.meetings, function (meeting_index) {
                    set_meeting(instructed_course_data, this, index, true);
                });
            });
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

        source   = $("#visual_schedule_card_content").html();
        template = Handlebars.compile(source);
        t = template(visual_data);
        VisualScheduleCard.dom_target.html(t);

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
