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
        $(".toggle_course_card_disclosure").on("click", function(ev) {
            ev.preventDefault();
            var card = $(ev.target).closest("[data-type='card']");
            var item_index = this.getAttribute("aria-controls");
            var div = $("#" + item_index);
            var expose = $("#show_" + item_index + "_wrapper");
            var hide = $("#hide_"  + item_index + "_wrapper");

            div.toggleClass("slide-show");
            div.css("display", div.css("display") === 'none' ? '' : 'none');

            if (div.hasClass("slide-show")) {
                window.setTimeout(function() {
                    div.show();
                    expose.attr("hidden", true);
                    expose.attr("aria-hidden", true);
                    hide.attr("hidden", false);
                    hide.attr("aria-hidden", false);
                    div.attr("aria-expanded", true);
                    div.attr("aria-hidden", true);
                    div.attr("hidden", false);
                    div.focus();
                }, 0);
                window.myuw_log.log_card(card, "expand");
            }
            else {
                window.setTimeout(function() {
                    div.hide();
                    expose.attr("hidden", false);
                    expose.attr("aria-hidden", false);
                    hide.attr("hidden", true);
                    hide.attr("aria-hidden", true);
                    div.attr("aria-expanded", false);
                    div.attr("aria-hidden", true);
                    div.attr("hidden", true);
                }, 700);
                window.myuw_log.log_card(card, "collapse");
            }
        });
    }
};
