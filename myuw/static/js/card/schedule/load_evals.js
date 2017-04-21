var LoadCourseEval = {

    render: function (course_data_resource, iasystem_data_resource) {
        var course_data = course_data_resource.data;
        var fetched_eval_data = iasystem_data_resource ? iasystem_data_resource.data : null;
        var course_sections = course_data.sections;

        $.each(course_sections, function () {
            section = this;
            section.year = course_data.year;
            section.quarter = course_data.quarter;
            section.summer_term = course_data.summer_term;

            CourseCardContentPanel.render(section, fetched_eval_data);
        });

        LoadCourseEval.add_events();
    },

    add_events: function() {
        $(".toggle_course_card_disclosure").on("click", function(ev) {
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
