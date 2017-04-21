function CourseData(term) {
    this.url = "/api/v1/schedule/" + term;
    this.data = null;
    this.error = null;
}

CourseData.prototype.setData = function(data) {
    // MUWM-549 and MUWM-552
    var sections = data.sections;
    var section_count = sections.length;
    for (var index = 0; index < section_count; index++) {
        section = sections[index];

        var canvas_url = section.canvas_url;
        if (canvas_url) {
            if (section.class_website_url == canvas_url) {
                section.class_website_url = null;
            }
            var matches = canvas_url.match(/\/([0-9]+)$/);
            var canvas_id = matches[1];
            var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

            if (section.class_website_url == alternate_url) {
                section.class_website_url = null;
            }
        }
    }

    this.data = data;
};

CourseData.prototype.normalize_instructors = function() {
    var data = this.data;

    if (!data.sections.length) {
        return;
    }
    if (data.sections[0].instructors !== undefined) {
        return;
    }

    var section_index = 0;
    for (section_index = 0; section_index < data.sections.length; section_index++) {
        var section = data.sections[section_index];
        section.instructors = [];

        var instructors = {};
        var meeting_index = 0;
        for (meeting_index = 0; meeting_index < section.meetings.length; meeting_index++) {
            var meeting = section.meetings[meeting_index];
            var instructor_index = 0;
            for (instructor_index = 0; instructor_index < meeting.instructors.length; instructor_index++) {
                var instructor = meeting.instructors[instructor_index];

                if (instructors[instructor.uwregid] === undefined) {
                    section.instructors.push(instructor);
                }
                instructors[instructor.uwregid] = true;
            }
        }
        section.instructors = section.instructors.sort(WebServiceData.sort_instructors_by_last_name);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.CourseData = CourseData;
