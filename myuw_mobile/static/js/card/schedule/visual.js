var VisualScheduleCard = {

    render_init: function(term, course_index) {
        var course_data =  WSData.normalized_course_data(term);
        if (course_data === undefined) {
            $("#visual_schedule_card_row").html(CardLoading.render("Course Schedule"));
            return;
        } 
        VisualScheduleCard.render(course_data, term, course_index);
    },

    render_upon_data: function(term, course_index) {
        var course_data =  WSData.normalized_course_data(term);
        if (course_data === undefined) {
            $("#visual_schedule_card_row").html(CardWithError.render());
            return;
        } 
        VisualScheduleCard.render(course_data, term, course_index);
    },

    // The course_index will be given when a modal is shown.
    render: function(course_data, term, course_index) {
        if (course_data.sections.length == 0) {
            $("#visual_schedule_card_row").html(CardWithNoCourse.render("this quarter"));
            return;
        }
        CourseCard.render(course_data, term, course_index);
        VisualScheduleCard.shown_am_marker = false;

        Modal.hide();
        var days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];

        var visual_data = {
            total_sections: course_data.sections.length,
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
            courses_meeting_tbd: []
        };

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
                        longitude: meeting.longitude
                    };

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

        var day_index;
        var weekends = days.length;
        if (!visual_data.has_6_days) {
            weekends = 5
        }
        for (day_index = 0; day_index < weekends; day_index++) {
            var day = days[day_index];
            var i = 0;
            while (i < visual_data[day].length) {
                var top = VisualScheduleCard.get_scaled_percentage(visual_data[day][i].start, visual_data.start_time, visual_data.end_time);
                var height =  VisualScheduleCard.get_scaled_percentage(visual_data[day][i].end, visual_data.start_time, visual_data.end_time) - top;
                visual_data[day][i].top=top;
                visual_data[day][i].height=height;
                i += 1;
            }

            var start_at_hr = true;
            var position_start = visual_data.start_time;
            while (position_start < visual_data.end_time) {
                var position_end = position_start + 30;
                var top = VisualScheduleCard.get_scaled_percentage(position_start, visual_data.start_time, visual_data.end_time);
                var height =  VisualScheduleCard.get_scaled_percentage(position_end, visual_data.start_time, visual_data.end_time) - top;
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
        $("#visual_schedule_card_row").html(template(visual_data));
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
        $(".show_section_details").bind("click", function(ev) {
            var course_id = this.rel;
            var log_course_id = ev.currentTarget.getAttribute("class").replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_modal_"+log_course_id, term);
            var hist = window.History;
            if (term) {
                hist.pushState({
                    state: "visual",
                    course_index: course_id,
                    term: term
                },  "", "/mobile/visual/"+term+"/"+course_id);
            }
            else {
                hist.pushState({
                    state: "visual",
                    course_index: course_id,
                },  "", "/mobile/visual/"+course_id);
            }
            CourseModal.show_course_modal(term, course_id);

            return false;
        });
        
        $(".show_map").on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_visual_card_"+building, term);
        });
        
        // TODO: this is testing... just ignore
        $("#show_today_schedule").on("click", function(ev) {
            ev.preventDefault();
            console.log("click click");
            $("#today_schedule").toggleClass("slide-show");
            
        });
        
        $("#show_exam_schedule").on("click", function(ev) {
            ev.preventDefault();
            $("#exam_schedule").toggleClass("slide-show");
            if ($("#exam_schedule").hasClass("slide-show")) {
                $("#show_exam_schedule").text("Hide Final Exam Schedule")
                $("#exam_schedule").attr('aria-hidden', 'false');
            }
            else {
                $("#show_exam_schedule").text("Show Final Exam Schedule");
                $("#exam_schedule").attr('aria-hidden', 'true');
            }
        });
    },
};
