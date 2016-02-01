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
            section.index = index;
            section.year = course_data.year;
            section.quarter = course_data.quarter;
            section.summer_term = course_data.summer_term;

            CourseEvalPanel.render(section, fetched_eval_data);
        }
        LoadCourseEval.add_events();
    },
    
    add_events: function() {
        $(".slide-link").on("click", function(ev) {
            ev.preventDefault();
            var hidden_block = $(ev.target).parent().siblings(".slide-hide")[0];
            var slide_link = this;
                        
            $(hidden_block).toggleClass("slide-show");
            var card = $(ev.target).closest("[data-type='card']");

            if ($(hidden_block).hasClass("slide-show")) {
                $(slide_link).text("HIDE COURSE DETAILS");
                $(slide_link).attr("title", "Hide course information");
                $(hidden_block).attr("aria-hidden", "false");
                 window.myuw_log.log_card(card, "expand");
            }
            else {
                $(slide_link).attr("title", "Show course information");
                $(hidden_block).attr("aria-hidden", "true");
                setTimeout(function() {
                      $(slide_link).text("SHOW COURSE DETAILS");
                }, 700);
                window.myuw_log.log_card(card, "collapse");
            }
        });
    }
};
