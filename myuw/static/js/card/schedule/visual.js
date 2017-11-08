var VisualScheduleCard = {
    name: 'VisualScheduleCard',
    dom_target: undefined,
    term: 'current',
    ck_student_schedule: false,
    ck_instructor_schedule: false,
    day_label_offset: 0,

    hide_card: function() {
        if (window.user.student) {
            VisualScheduleCard.ck_student_schedule = true;
        }
        if (window.user.instructor) {
            VisualScheduleCard.ck_instructor_schedule = true;
        }
        if (VisualScheduleCard.ck_student_schedule || VisualScheduleCard.ck_instructor_schedule) {
            return false;
        }
        return true;
    },

    render_init: function(term, course_index) {
        console.log('INIT');
        if (VisualScheduleCard.hide_card()) {
            $("#VisualScheduleCard").hide();
            return;
        }
        console.log('123');
        console.log(VisualScheduleCard.term);
        WSData.fetch_visual_schedule_term(VisualScheduleCard.term,
                                          VisualScheduleCard.render_handler,
                                          VisualScheduleCard.render_handler);
    },

    render_handler: function() {
        var default_period = 0;

        VisualScheduleCard.display_schedule_for_period(default_period);
    },

    _render_error: function() {
        console.log('err');
        $("#VisualScheduleCard").hide();
    },

    _get_period_lables: function(schedule_data){
        var periods = {};
        $(schedule_data.periods).each(function(idx, period){
            periods[period.id] = {'start_date': period.start_date,
                'end_date': period.end_date};
        });
        return periods;
    },

    // The course_index will be given when a modal is shown.
    _render: function() {
    },
    _get_data_for_period: function(course_data, term){
        var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        var visual_data = {
            //has_early_fall_start: ((course_data && course_data.has_early_fall_start) ||
            //                       (instructed_course_data &&
            //                        instructed_course_data.has_early_fall_start)),
            is_pce: window.user.pce,
            total_sections: course_data.sections.length,
            quarter: term.quarter,
            year: term.year,
            //year: course_data ? course_data.year : instructed_course_data.year,
            //quarter: course_data ? course_data.quarter : instructed_course_data.quarter,
            //term: term,
            //summer_term: course_data ? course_data.summer_term : instructed_course_data.summer_term,
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
            courses_no_meeting: [],
            //schedule_periods: (course_data && course_data.schedule_periods) ? course_data.schedule_periods
            //    : (instructed_course_data && instructed_course_data.schedule_periods) ? instructed_course_data.schedule_periods
            //    : {},
            is_instructor: false
        };

        //if (instructed_course_data && instructed_course_data.schedule_periods) {
        //    if (period in instructed_course_data.schedule_periods) {
        //        visual_data.total_sections +=
        //            instructed_course_data.schedule_periods[period].sections.length;
        //    }
        //}

        var set_meeting = function(course_data, is_instructor) {
            //if (!(period in course_data.schedule_periods)) {
            //    return;
            //}

            $.each(course_data.sections, function(section_index) {
                var section = this;
                $.each(section.meetings, function(){
                    var meeting = this;
                    var has_meetings = VisualScheduleCard._meeting_has_meetings(meeting);
                    var seen = false;
                    if (!meeting.days_tbd && has_meetings) {

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
                            //term: term,
                            section_id: section.section_id,
                            section_index: section_index,
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

                        $.each(days, function(){
                            day = this.toString();
                            if (meeting.meeting_days[day]) {
                                if (day === "saturday") {
                                    visual_data.has_6_days = true;
                                }
                                visual_data[day].push(meeting_info);
                            }
                        });
                    }
                    else if (meeting.days_tbd){
                        $.each(visual_data.courses_meeting_tbd, function () {
                            if (this.section_index == section_index) {
                                seen = true;
                                return false;
                            }
                        });

                        // has meetings that are TBD
                        if (!seen) {
                            visual_data.courses_meeting_tbd.push({
                                color_id: section.color_id,
                                curriculum: section.curriculum_abbr,
                                course_number: section.course_number,
                                section_id: section.section_id,
                                section_index: section_index
                            });
                        }
                    }
                    else {
                        $.each(visual_data.courses_no_meeting, function () {
                            if (this.section_index == section_index) {
                                seen = true;
                                return false;
                            }
                        });

                        // Has no meetings, not TBD (eg individual start PCE courses)
                        if (!seen) {
                            visual_data.courses_no_meeting.push({
                                color_id: section.color_id,
                                curriculum: section.curriculum_abbr,
                                course_number: section.course_number,
                                section_id: section.section_id,
                                section_index: section_index
                            });
                        }
                    }
                });
            });
        };
        var day, day_index, i, height, top;

        if (course_data) {
            set_meeting(course_data, false);
        }

        //if (instructed_course_data && instructed_course_data.sections.length) {
        //    visual_data.is_instructor = true;
        //    set_meeting(instructed_course_data, true);
        //}

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
    _meeting_has_meetings: function(meeting){
        var has_meeting = false;
        $.each(meeting.meeting_days, function (idx, meeting) {
            if (meeting !== null){
                has_meeting = true;
            }
        });
        return has_meeting;
    },
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


        $("a.schedule-period-anchor").on("click", function(ev){
            console.log('eventy');
            var period_id = $(this).attr('data-period_id');
            VisualScheduleCard.display_schedule_for_period(period_id);
            return false;
        });
    },

    render_schedule: function(data){
        var source = $("#visual_schedule_card_content").html();
        var template = Handlebars.compile(source);
        var t = template(data);
        VisualScheduleCard.dom_target.html(t);
        VisualScheduleCard.add_events();

    },

    display_schedule_for_period: function(period_id){
        var schedule_data = WSData.visual_schedule_data('current');
        var period = schedule_data.periods[period_id];

        var processed_period = VisualScheduleCard._get_data_for_period(period, schedule_data.term);
        var period_labels = VisualScheduleCard._get_period_lables(schedule_data);
        processed_period['schedule_periods'] = period_labels;
        processed_period.active_period_id = period;

        if(period === "finals"){
            var target = $("#schedule_area").first();
            FinalExamSchedule.render(course_data, instructed_course_data, term, false, target);
        } else {
            VisualScheduleCard.render_schedule(processed_period);
        }
    }

};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.VisualScheduleCard = VisualScheduleCard;
