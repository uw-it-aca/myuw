var VisualScheduleCard = {
    name: 'VisualScheduleCard',
    dom_target: undefined,
    term: 'current',
    ck_student_schedule: false,
    ck_instructor_schedule: false,

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
        if (VisualScheduleCard.hide_card()) {
            $("#VisualScheduleCard").hide();
            return;
        }
        WSData.fetch_course_data_for_term(VisualScheduleCard.term,
                                          VisualScheduleCard.render_handler,
                                          VisualScheduleCard.render_handler);
        if(myuwFeatureEnabled('instructor_schedule')) {
            WSData.fetch_instructed_course_data_for_term(VisualScheduleCard.term,
                                                         VisualScheduleCard.render_handler,
                                                         VisualScheduleCard.render_handler);
        }
    },

    render_handler: function() {
        // returns true when both schedule API calls have returned, successful or otherwise
        var course_data = WSData._course_data[VisualScheduleCard.term];
        var course_err = WSData.course_data_error_code(VisualScheduleCard.term);
        var instructed_course_data = WSData._instructed_course_data[VisualScheduleCard.term];
        var instructed_course_err = WSData.instructed_course_data_error_code(VisualScheduleCard.term);

        if (VisualScheduleCard.ck_student_schedule &&
            !course_data &&
            !course_err ||
            (VisualScheduleCard.ck_instructor_schedule &&
             !instructed_course_data &&
             !instructed_course_err)) {
            return;
        }
        if (course_data && course_data.sections.length ||
            instructed_course_data && instructed_course_data.sections.length){
            VisualScheduleCard._render();
            return;
        }
        VisualScheduleCard._render_error();
    },

    _render_error: function() {
        $("#VisualScheduleCard").hide();
    },

    // The course_index will be given when a modal is shown.
    _render: function() {
        var term = VisualScheduleCard.term;
        var course_data = WSData.normalized_course_data(term);
        var instructed_course_data = WSData.normalized_instructed_course_data(term);
        window.term.summer_term = course_data ? course_data.summer_term : instructed_course_data.summer_term;
        if (course_data) {
            course_data.schedule_periods = VisualScheduleCard._get_schedule_periods(course_data);
        }
        if (instructed_course_data && instructed_course_data.sections.length) {
            instructed_course_data.schedule_periods = VisualScheduleCard._get_schedule_periods(instructed_course_data);
        }

        if(window.future_term === undefined){
            if(course_data && course_data.summer_term === ""){
                $.extend(course_data.schedule_periods, VisualScheduleCard._get_finals(course_data.sections));
            }
            if(instructed_course_data && instructed_course_data.sections.length && instructed_course_data.summer_term === ""){
                $.extend(instructed_course_data.schedule_periods, VisualScheduleCard._get_finals(instructed_course_data.sections));
            }
        } else if(window.future_term.indexOf("summer") === -1){
            if (course_data) {
                $.extend(course_data.schedule_periods, VisualScheduleCard._get_finals(course_data.sections));
            }
            if (instructed_course_data && instructed_course_data.sections.length) {
                $.extend(instructed_course_data.schedule_periods, VisualScheduleCard._get_finals(instructed_course_data.sections));
            }
        }
        var default_period = VisualScheduleCard._get_default_period(course_data ? course_data.schedule_periods : null,
                                                                    instructed_course_data ? instructed_course_data.schedule_periods: null);
        VisualScheduleCard.display_schedule_for_period(default_period);

        LogUtils.cardLoaded(VisualScheduleCard.name, VisualScheduleCard.dom_target);
    },

    _get_default_period: function(course_periods, instructed_course_periods){
        var today = moment.utc(window.card_display_dates.comparison_date, "YYYY-MM-DD"),
            default_section, i;

        $.each([course_periods, instructed_course_periods], function (i, periods) {
            if (periods) {
                $.each(periods, function(idx, period){
                    if (moment.utc(period.start_date, "YYYY-MM-DD").isSameOrBefore(today) &&
                            moment.utc(period.end_date, "YYYY-MM-DD").isSameOrAfter(today)) {
                        default_section = idx;
                    }
                });
            }
        });

        // Handle case where period cannot be determined
        $.each([course_periods, instructed_course_periods], function (i, periods) {
            if(periods && default_section === undefined){
                default_section = Object.keys(periods)[0];
            }
        });

        return default_section;
    },

    _get_schedule_periods: function(course_data) {
        var schedule_periods = {};
        $.each(course_data.sections, function(idx, section){
            // get start and end dates for section
            var section_dates = VisualScheduleCard._get_dates_for_section(section);
            schedule_periods = VisualScheduleCard._add_to_periods(section_dates,
                                                                  section,
                                                                  schedule_periods);
        });
        var range = VisualScheduleCard._get_schedule_range(course_data);
        var weeks = VisualScheduleCard._get_weeks_from_range(range);
        weeks = VisualScheduleCard._add_sections_to_weeks(weeks, course_data.sections);
        weeks = VisualScheduleCard._consolidate_weeks(weeks);
        return VisualScheduleCard._format_dates(weeks);
    },

    _consolidate_weeks: function(weeks){
        var consolidated_weeks = {},
            first_week = parseInt(Object.keys(weeks)[0]),
            num_weeks = first_week + Object.keys(weeks).length - 1;

        for(var i=first_week; i <= num_weeks; i++){
            //Add the first week
            var consolidated_week = weeks[i];

            //Loop through all weeks after this one checking for same sections
            for(var k = i+1; k <= num_weeks; k++){

                if(VisualScheduleCard._sections_are_same(weeks[i], weeks[k])){
                    //Change end date
                    consolidated_week.end_date = weeks[k].end_date;
                    //increment counter
                    i += 1;
                }
                else {
                    break;
                }
            }
            consolidated_weeks[i] = consolidated_week;

        }
        return consolidated_weeks;

    },


    _sections_are_same: function(list1, list2){
        if (list1 === undefined || list2 === undefined) {
            return false;
        }

        var lists_are_same = true,
            l1_sections = list1.sections.slice(),
            l2_sections = list2.sections.slice();

        $.each(l1_sections, function(idx, section){
            var in_list = VisualScheduleCard._section_list_has_section(section, l2_sections);
            if(!in_list){
                lists_are_same = false;
            }
        });

        $.each(l2_sections, function(idx, section){
            var in_list = VisualScheduleCard._section_list_has_section(section, l1_sections);
            if(!in_list){
                lists_are_same = false;
            }
        });

        return lists_are_same;
    },

    _section_list_has_section: function(section, list){
        var in_section = false;
        $.each(list, function(idx, l2_section){
            if(section.course_number === l2_section.course_number &&
                section.curriculum_abbr === l2_section.curriculum_abbr){
                in_section = true;
            }
        });
        return in_section;
    },

    _add_sections_to_weeks: function(weeks, sections){
        $.each(weeks, function(idx, week){
            $.each(sections, function(idx, section){
                var dates = VisualScheduleCard._get_dates_for_section(section);
                if(dates[0].isSameOrBefore(week.end_date) && dates[1].isSameOrAfter(week.start_date)){
                    week.sections.push(section);
                }

            });
        });

        return weeks;
    },

    _get_weeks_from_range: function(range){
        var start = range[0].week(),
            end = range[1].week(),
            weeks = {};
        if(start > end){
            end += 52;
        }

        for (var i = start; i <=end; i++){
            var year = range[0].year();
            var week = moment.utc().year(year).week(i);
            var start_date = week.clone().startOf('week');
            start_date.add(1, 'days');
            var end_date = week.clone().endOf('week');
            end_date.add(1, 'days');

            weeks[i] = {
                "start_date": start_date,
                "end_date": end_date,
                "sections": []
            };
        }
        return weeks;

    },


    _get_schedule_range: function(course_data){
        var earliest,
            latest;
        if (course_data) {
            $.each(course_data.sections, function(idx, section){
                var dates = VisualScheduleCard._get_dates_for_section(section);
                if (earliest === undefined){
                    earliest = dates[0];
                } else if(dates[0].isBefore(earliest)){
                    earliest = dates[0];
                }

                if (latest === undefined){
                    latest = dates[1];
                } else if(dates[1].isAfter(latest)){
                    latest = dates[1];
                }
            });
        }

        return [earliest, latest];
    },

    _format_dates: function(schedule_periods){
        //Formats dates so handlebars helper can parse
        for (var period_id in schedule_periods){
            schedule_periods[period_id].start_date = schedule_periods[period_id].start_date.format("YYYY-MM-DD");
            schedule_periods[period_id].end_date = schedule_periods[period_id].end_date.format("YYYY-MM-DD");
        }
        return schedule_periods;
    },

    _get_finals: function(sections){
        var finals_periods = {};
        $.each(sections, function(idx, section){
            if(section.final_exam !== undefined &&
                section.final_exam.start_date !== undefined) {
                VisualScheduleCard._add_to_finals(section, finals_periods);
            }
        });
        return finals_periods;
    },

    _add_to_finals: function(section, schedule_periods){
        var week_range = VisualScheduleCard._get_week_range_from_date(section.final_exam.start_date);
        if ("finals" in schedule_periods){
            schedule_periods.finals.sections.push(section);
        } else {
            schedule_periods.finals =
            {"start_date": week_range[0].format("YYYY-MM-DD"),
                "end_date" : week_range[1].format("YYYY-MM-DD"),
                "sections": [section]
            };
        }
        return schedule_periods;
    },


    _add_to_periods: function(dates, section, periods){
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
        return periods;
    },

    _get_dates_for_section: function(section){
        var start_date = section.start_date,
            end_date = section.end_date;
        if(start_date === "None"){
            // Regular courses don't have start/end dates
            if(window.future_term !== undefined){
                if(window.future_term.indexOf("a-term") !== -1){
                    start_date = window.future_term_data.first_day_quarter;
                    end_date = window.future_term_data.aterm_last_date;
                } else if(window.future_term.indexOf("b-term") !== -1){
                    start_date = window.future_term_data.bterm_first_date;
                    end_date = window.future_term_data.last_day_instruction;
                } else {
                    start_date = window.future_term_data.first_day_quarter;
                    end_date = window.future_term_data.last_day_instruction;
                }
            } else {
                // use current term dates
                // handle summer term for current quarter
                if(window.term.summer_term.toLowerCase().indexOf("a-term") !== -1){
                    start_date = window.term.first_day_quarter;
                    end_date = window.term.aterm_last_date;
                } else if(window.term.summer_term.toLowerCase().indexOf("b-term") !== -1){
                    start_date = window.term.bterm_first_date;
                    end_date = window.term.last_day_instruction;
                } else {
                    start_date = window.term.first_day_quarter;
                    end_date = window.term.last_day_instruction;
                }
            }
        }
        return [moment.utc(new Date(start_date)), moment.utc(new Date(end_date))];
    },

    _get_week_range_from_date: function(date){
        var exam_date = moment.utc(date);
        var start = exam_date.startOf('week');
        start.add(1, 'days');
        var end = exam_date.clone().endOf('week');
        end.add(1, 'days');

        return [start, end];
    },

    display_schedule_for_period: function(period){
        var term = VisualScheduleCard.term;
        var course_data = WSData.normalized_course_data(term);
        var instructed_course_data = WSData.normalized_instructed_course_data(term);
        var data = VisualScheduleCard._get_data_for_period(course_data, instructed_course_data, term, period);
        data.active_period_id = period;
        VisualScheduleCard.render_schedule(data, term);
        if(period === "finals"){
            var target = $("#schedule_area").first();
            FinalExamSchedule.render(course_data, instructed_course_data, term, false, target);
        }
    },

    _get_data_for_period: function(course_data, instructed_course_data, term, period){
        var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
        var visual_data = {
            has_early_fall_start: ((course_data && course_data.has_early_fall_start) ||
                                   (instructed_course_data &&
                                    instructed_course_data.has_early_fall_start)),
            is_pce: window.user.pce,
            total_sections: course_data ? course_data.schedule_periods[period].sections.length : 0,
            year: course_data ? course_data.year : instructed_course_data.year,
            quarter: course_data ? course_data.quarter : instructed_course_data.quarter,
            term: term,
            summer_term: course_data ? course_data.summer_term : instructed_course_data.summer_term,
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
            schedule_periods: (course_data && course_data.schedule_periods) ? course_data.schedule_periods
                : (instructed_course_data && instructed_course_data.schedule_periods) ? instructed_course_data.schedule_periods
                : {},
            is_instructor: false
        };

        if (instructed_course_data && instructed_course_data.schedule_periods) {
            if (period in instructed_course_data.schedule_periods) {
                visual_data.total_sections +=
                    instructed_course_data.schedule_periods[period].sections.length;
            }
        }

        var set_meeting = function(course_data, is_instructor) {
            if (!(period in course_data.schedule_periods)) {
                return;
            }

            $.each(course_data.schedule_periods[period].sections, function(section_index) {
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
                            term: term,
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

        if (instructed_course_data && instructed_course_data.sections.length) {
            visual_data.is_instructor = true;
            set_meeting(instructed_course_data, true);
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

    _meeting_has_meetings: function(meeting){
        var has_meeting = false;
        $.each(meeting.meeting_days, function (idx, meeting) {
            if (meeting !== null){
                has_meeting = true;
            }
        });
        return has_meeting;
    },

    _section_has_meetings: function(section){
        var has_meeting = false;
        $.each(section.meetings, function (idx, meeting) {
            $.each(meeting.meeting_days, function (idx, meeting_days) {
                if (meeting_days !== null) {
                    has_meeting = true;
                }
            });
        });
        return has_meeting;
    },

    render_schedule: function(visual_data, term) {
        VisualScheduleCard.shown_am_marker = false;

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


        $("a.schedule-period-anchor").on("click", function(ev){
            var period_id = $(this).attr('data-period_id');
            VisualScheduleCard.display_schedule_for_period(period_id);
            return false;
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.VisualScheduleCard = VisualScheduleCard;
