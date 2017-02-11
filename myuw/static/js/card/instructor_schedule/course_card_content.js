var InstructorCourseCardContent = {

    render: function (c_section, fetched_eval) {
        var eval_data = (fetched_eval? WSData.iasystem_data(): null);
        var index = c_section.index;
        var source = $("#instructor_course_card_content_panel").html();
        var template = Handlebars.compile(source);
        var card = $('#instructor_course_card_content' + index);

        var raw = template(c_section);
        card.html(raw);

        InstructorCourseSchePanel.render(c_section);
        InstructorCourseResourcePanel.render(c_section);

        if (c_section.grade_submission_delegates) {
            CourseInstructorPanel.render(c_section);
        }

        InstructorCourseCardContent.add_events(card);
    },

    add_events: function(card) {
        var term = $('.instructed-terms option:selected').val();
        if (!term) {
            term = window.term.year + ',' + window.term.quarter;
        }

        $(".course_website", card).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = target.getAttribute("rel").replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".course_website_update", card).on("click", function(ev) {
            var target = ev.currentTarget;
            var course_id = target.getAttribute("rel").replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("update_course_website_"+course_id, term);
            window.open(target.getAttribute('data-href'),
                        'class_website_update',
                        'width=700,height=400');
        });

        $(".copy_course_website", card).on("click", function () {
            $("#class_website_url", card).
                focus().
                select();
            try {
                document.execCommand('copy');
            }
            catch (err) {
                // ignore failed copy
            }
        });

        $(".show_map", card).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            var building = ev.currentTarget.getAttribute("rel");
            building = building.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("show_map_from_course_list_"+building, term);
        });

        $(".course_canvas_site", card).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_canvas_website_"+course_id, term);
        });

        $(".course_website", card).on("click", function(ev) {
            var course_id = ev.currentTarget.getAttribute("rel");
            course_id = course_id.replace(/[^a-z0-9]/gi, '_');
            WSData.log_interaction("open_course_website_"+course_id, term);
        });

        $(".create_email_list", card).on("click", function(ev) {
            var course_label = ev.currentTarget.getAttribute("rel");
            label = safe_label(course_label)
            WSData.log_interaction("open_create_email_list_"+label, term);
            RequestEmailLists.render_init(course_label);
        });

        $(".manage_email_list", card).on("click", function(ev) {
            var course_label = ev.currentTarget.getAttribute("rel");
            label = safe_label(course_label)
            WSData.log_interaction("open_manage_email_list_"+label, term);
            ManageEmailLists.render_init(course_label);
        });

    }
};
