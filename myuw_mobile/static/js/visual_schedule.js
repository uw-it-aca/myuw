var VisualSchedule = {
    show_visual_schedule: function() {
        WSData.fetch_course_data(VisualSchedule.render);
    },

    render: function() {
        Handlebars.registerHelper('time_percentage', function(time, start, end) {
            return parseInt(((time - start) / (end - start)) * 10000, 10) / 100;
        });

        Handlebars.registerHelper('show_days_meetings', function(list, start_time, end_time) {
            if (!VisualSchedule.day_template) {
                var day_source = $("#visual_schedule_day").html();
                var _day_template = Handlebars.compile(day_source);

                VisualSchedule.day_template = _day_template;
            }

            return new Handlebars.SafeString(VisualSchedule.day_template({ meetings: list, start_time: start_time, end_time: end_time }));
        });

        var source   = $("#visual_schedule").html();
        var template = Handlebars.compile(source);

        var course_data = WSData.course_data();

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
            has_6_days: false
        };

        for (var index in course_data.sections) {
            var section = course_data.sections[index];

            for (var meeting_index in section.meetings) {
                var meeting = section.meetings[meeting_index];
                if (meeting.days_tbd) {
                    continue;
                }

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
                    course_number: section.course_number
                };

                var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
                for (var day_index in days) {
                    var day = days[day_index];

                    if (meeting.meeting_days[day]) {
                        if (day == "saturday") {
                            visual_data.has_6_days = true;
                        }
                        visual_data[day].push(meeting_info);
                    }
                }
            }
        }

        // Make it so the start and end times are always on the hour:
        var start_hour = parseInt(visual_data.earliest_start / 60)
        if ((start_hour * 60) == visual_data.earliest_start) {
            visual_data.start_time = (start_hour * 60) - 60;
        }
        else {
            visual_data.start_time = (start_hour * 60);
        }

        var end_hour = parseInt(visual_data.latest_ending / 60) + 1;
        if ((end_hour * 60) == visual_data.latest_ending) {
            visual_data.end_time = (end_hour * 60) - 60;
        }
        else {
            visual_data.end_time = (end_hour * 60);
        }

        for (var i = visual_data.start_time; i <= visual_data.end_time; i += 60) {
            visual_data.display_hours.push({
                hour: (i / 60),
                position: i
            });
        }

        $("#courselist").html(template(visual_data));

        source = $("#quarter-visual").html();
        template = Handlebars.compile(source);
        $("#quarter-info").html(template({year: course_data.year, quarter: course_data.quarter}));

        $(".display_list_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "course_list",
            },  "", "/my/");
        });


        $(".instructor").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "instructor",
                instructor: ev.target.rel
            },  "", "/my/instructor/"+ev.target.rel);
        });

    }
};
