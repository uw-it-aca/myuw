function CourseData(term) {
    this.name = 'course_data';
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
