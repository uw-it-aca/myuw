var CourseSchePanel = {

    render: function (c_section) {
        var source = $("#course_sche_panel").html();
        var template = Handlebars.compile(source);
         c_section.netid = window.user.netid;
        for (i = 0; i < c_section.meetings.length; i++) {
            if (c_section.meetings[i].type !== c_section.section_type) {
                c_section.meetings[i].display_type = true;
            }
        }
        var raw = template(c_section);
        $('#sche_on_course_card' + c_section.index).html(raw);
    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}

exports.CourseSchePanel = CourseSchePanel;
