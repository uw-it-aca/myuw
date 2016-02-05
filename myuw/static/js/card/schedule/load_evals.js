var LoadCourseEval = {

    render_upon_data: function() {
        LoadCourseEval.render('current', LoadCourseEval._has_all_data());
    },

    _has_all_data: function () {
        if (WSData.iasystem_data()) {
            return true;
        }
        return false;
    },

    render: function (term, fetched_eval_data) {
        var course_data = WSData.normalized_course_data(term);
        var course_sections = course_data.sections;
        var index;
        for (index = 0; index < course_sections.length; index++) {
            section = course_sections[index];
            section.year = course_data.year;
            section.quarter = course_data.quarter;
            section.summer_term = course_data.summer_term;

            CourseCardContentPanel.render(section, fetched_eval_data);
        }
        LoadCourseEval.add_events();
    },
    
    add_events: function() {
        $(".slide-link").on("click", function(ev) {
            ev.preventDefault();
            var slide_link = this;
            var slide_link_text = this.text;
            var is_instr = (slide_link_text.match(/instructors$/i) ? true : false);
            var hidden_block = $('#' + this.getAttribute("aria-controls"));

            $(hidden_block).toggleClass("slide-show");
            var card = $(ev.target).closest("[data-type='card']");

            if ($(hidden_block).hasClass("slide-show")) {

                var text = is_instr ? "HIDE INSTRUCTORS" : "HIDE COURSE DETAILS";
                var title = is_instr ? "Hide Instructors" : "Hide course details";
                $(slide_link).text(text);
                $(slide_link).attr("title", title);
                $(hidden_block).attr("aria-hidden", "false");
                window.myuw_log.log_card(card, "expand");
            }
            else {
                var text = is_instr ? "SHOW INSTRUCTORS" : "SHOW COURSE DETAILS";
                var title = is_instr ? "Show Instructors" : "Show course details";
                $(slide_link).attr("title", title);
                $(hidden_block).attr("aria-hidden", "true");
                setTimeout(function() {
                      $(slide_link).text(text);
                }, 700);
                window.myuw_log.log_card(card, "collapse");
            }
        });
    }
};
