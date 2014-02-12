var Weekly = {
    show_current_week: function() {
        showLoading();
        WSData.fetch_current_week_data(Weekly.render_week);
    },

    render_week: function(data) {

        var current_week = data["current_week"];
        var template;

        if (current_week > 0 && current_week < 11) {
            var name = "#week"+current_week+"_outline";

            if ($(name).length) {
                var source = $(name).html();
                template = Handlebars.compile(source);
            }
        }

        if (!template) {
            var source = $("#week_other_outline").html();
            template = Handlebars.compile(source);
        }

        var visual_schedule = VisualSchedule.get_html(data.schedule);

        // XXX - get this into course_list.js
        var course_data = data.schedule;
        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            course_data.sections[index].index = index;
            if (course_data.sections[index].class_website_url || course_data.sections[index].canvas_url) {
                course_data.sections[index].has_resources = true;
            }
        }


        var source = $("#courses").html();
        var courses_template = Handlebars.compile(source);
        var course_list = courses_template(course_data);

        $("#courselist").html(template({
            visual_schedule: visual_schedule,
            course_list: course_list
        }));

        //Collapse events
        for (index = 0; index < course_data.sections.length; index++) {
            var section = $("#course" + index);
            var label = $("#course"+index+"_label");

            $(section).on('shown.bs.collapse',
                function () {
                    $(this).parent().find("div.accordion-footer > a > span.show_more").hide();
                    $(this).parent().find("div.accordion-footer > a > span.show_less").show();
            });
            $(section).on('hidden.bs.collapse',
                function () {
                    $(this).parent().find("div.accordion-footer > a > span.show_more").show();
                    $(this).parent().find("div.accordion-footer > a > span.show_less").hide();
            });
        }

    }
};
