var CourseSchePanel = {

    render: function (c_section) {
        Handlebars.registerPartial('course_sche_col_days', $("#course_sche_col_days").html());
        Handlebars.registerPartial('course_sche_col_bldg', $("#course_sche_col_bldg").html());

        var source = $("#course_sche_panel").html();
        var template = Handlebars.compile(source);

        c_section.netid = window.user.netid;
        if (c_section.meetings.length > 0) {
            for (var i = 0; i < c_section.meetings.length; i++) {
                if (!c_section.wont_meet &&
                    !c_section.no_meeting &&
                    c_section.meetings[i].type !== c_section.section_type &&
                    c_section.meetings[i].type !== 'NON'
                   ) {
                    c_section.meetings[i].display_type = true;
                }
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
