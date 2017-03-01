var InstructorCourseCardContent = {

    render: function (c_section, fetched_eval) {
        var eval_data = (fetched_eval? WSData.iasystem_data(): null);
        var index = c_section.index;
        var source = $("#instructor_course_card_content_panel").html();
        var template = Handlebars.compile(source);
        var card = $('#instructor_course_card_content' + index);
        var term = c_section.year + ',' + c_section.quarter.toLowerCase();
        var raw = template(c_section);

        card.html(raw);

        InstructorCourseSchePanel.render(c_section);
        InstructorCourseResourcePanel.render(c_section);

        if (c_section.grade_submission_delegates) {
            CourseInstructorPanel.render(c_section);
        }

        InstructorCourseCardContent.add_events(card, term);
    },

    add_events: function(card, term) {
        $(".show_map", card).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });
        $(".course_delegate_link", card).on("click", function(ev) {
            var width = 800;
            var height = 400;

            var left = window.screenX + 200;
            var top = window.screenY + 200;

            window.open(ev.target.href, '_blank', 'width='+width+',height='+height+',left='+left+',top='+top);

            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_delegate__"+course_id, term);
            return false;
        });
        $(".gradepage_help_link", card).on("click", function(ev) {
            var width = 800;
            var height = 400;

            var left = window.screenX + 200;
            var top = window.screenY + 200;

            window.open(ev.target.parentElement.href, '_blank', 'width='+width+',height='+height+',left='+left+',top='+top);

            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_gradepage_help_"+course_id, term);
            return false;
        });
    }
};
