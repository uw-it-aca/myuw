var VisualSchedule = {
    // This is the height of the days bar... needed for positioning math below
    day_label_offset: 0,

    show_visual_schedule: function(course_index) {
        showLoading();
        WSData.fetch_course_data(VisualSchedule.render, [course_index]);
    },

    get_scaled_percentage: function(pos, min, max) {
        var base_percentage = (pos - min) / (max - min);
        var offset_percentage = (VisualSchedule.day_label_offset * 2) + (base_percentage * (100 - (VisualSchedule.day_label_offset * 2)));

        // The second one is for positioning the last hour label.
        return offset_percentage - VisualSchedule.day_label_offset;
    },

    // The course_index will be given when a modal is shown.
    render: function(course_index) {
        $('html,body').animate({scrollTop: 0}, 'fast');
        VisualSchedule.shown_am_marker = false;
        Handlebars.registerHelper('format_schedule_hour', function(hour) {
            if (parseInt(hour, 10) === 12) {
                VisualSchedule.shown_am_marker = true;
                return hour + "p";
            }
            else if (hour > 12) {
                var shown_hour = hour - 12;
                if (!VisualSchedule.shown_am_marker) {
                    VisualSchedule.shown_am_marker = true;
                    return shown_hour + "p";
                }
                return shown_hour;
            }
            else if (hour < 12) {
                if (!VisualSchedule.shown_am_marker) {
                    VisualSchedule.shown_am_marker = true;
                    return hour + "a";
                }
            }
            return hour;
        });

        Handlebars.registerHelper('time_percentage', function(time, start, end) {
            return VisualSchedule.get_scaled_percentage(time, start, end);
        });

        Handlebars.registerHelper('time_percentage_height', function(start, end, min, max) {
            var top = VisualSchedule.get_scaled_percentage(start, min, max);
            var bottom = VisualSchedule.get_scaled_percentage(end, min, max);

            return bottom-top;
        });

        Handlebars.registerHelper('show_days_meetings', function(list, start_time, end_time) {
            if (!VisualSchedule.day_template) {
                var day_source = $("#visual_schedule_day").html();
                var _day_template = Handlebars.compile(day_source);

                VisualSchedule.day_template = _day_template;
            }

            return new Handlebars.SafeString(VisualSchedule.day_template({ meetings: list, start_time: start_time, end_time: end_time }));
        });

        var course_data = WSData.course_data();

        var source = $("#quarter-visual").html();
        var template = Handlebars.compile(source);
        $("#page-header").html(template({year: course_data.year, quarter: course_data.quarter}));

        var visual_data = {
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
            courses_meeting_tbd: []
        };

        // Handle the case of no courses
        if (course_data.sections.length == 0) {
            var source   = $("#no-courses").html();
            var template = Handlebars.compile(source);
            $("#courselist").html(template(course_data));
            return;
        }

        source   = $("#visual_schedule").html();
        template = Handlebars.compile(source);

        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            var section = course_data.sections[index];

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
                        start: start_minutes,
                        end: end_minutes,
                        color_id: section.color_id,
                        curriculum: section.curriculum_abbr,
                        course_number: section.course_number,
                        section_id: section.section_id,
                        section_index: index
                    };

                    var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
                    var day_index = 0;
                    for (day_index = 0; day_index < days.length; day_index++) {
                        var day = days[day_index];

                        if (meeting.meeting_days[day]) {
                            if (day === "saturday") {
                                visual_data.has_6_days = true;
                            }
                            visual_data[day].push(meeting_info);
                        }
                    }
                }
                else {
                    visual_data["courses_meeting_tbd"].push({
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

        $("#courselist").html(template(visual_data));

        $(".display_list_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "course_list"
            },  "", "/mobile/");

            return false;
        });

        if (!course_index) {
            Modal.hide();
        }
        else {
            if (course_index < course_data.sections.length) {
                CourseModal.show_course_modal(course_index);
            }
        }


        $(".show_section_details").bind("click", function(ev) {
            var course_id = this.rel;
            var hist = window.History;
            hist.pushState({
                state: "visual",
                course_index: course_id
            },  "", "/mobile/visual/"+course_id);

            CourseModal.show_course_modal(course_id);

            return false;
        });

        $(".show_textbooks").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "textbooks"
            },  "", "/mobile/textbooks");

            return false;
        });




    },

    _get_meeting_info: function(meeting) {
    }
};
