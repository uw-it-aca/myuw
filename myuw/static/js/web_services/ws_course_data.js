function CourseData(term) {
    BaseData.call(this, "/api/v1/schedule/" + term);
}

CourseData.prototype = Object.create(BaseData.prototype);

CourseData.prototype.setData = function(data) {
    // MUWM-549 and MUWM-552
    var sections = data.sections;
    var section_count = sections.length;
    $.each(sections, function () {
        section = this;
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
    });

    this.data = data;
};

CourseData.prototype.normalize_instructors = function() {
    if (!this.data.sections.length ||
        this.data.sections[0].instructors !== undefined) {
        return;
    }

    $.each(this.data.sections, function () {
        var section = this;
        section.instructors = [];
        var instructors = {};
        $.each(section.meetings, function () {
            var meeting = this;
            $.each(meeting.instructors, function () {
                var instructor = this;
                if (instructors[instructor.uwregid] === undefined) {
                    section.instructors.push(instructor);
                }
                instructors[instructor.uwregid] = true;
            });
        });

        section.instructors = section.instructors
            .sort(this.sort_instructors_by_last_name);
    });
};

CourseData.prototype.sort_instructors_by_last_name = function(a, b) {
    if (a.surname < b.surname) return -1;
    if (a.surname > b.surname) return 1;
    return 0;
};


/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.CourseData = CourseData;
