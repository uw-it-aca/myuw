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
        LoadCourseEval.add_events(course_data.quarter);
    },
    
    add_events: function(quarter) {
        $(".toggle_course_card_disclosure_" + quarter).on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            var item_index = this.getAttribute("aria-controls");
            var div = $("#" + item_index);
            var expose = $("#show_" + item_index + "_wrapper");
            var hide = $("#hide_"  + item_index + "_wrapper");
            toggle_card_disclosure(card, div, expose, hide, item_index);
        });
    }
};
