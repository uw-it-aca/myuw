function InstructedSectionData(section_label) {
    this.url = "/api/v1/instructor_section/" + section_label;
    this.data = null;
    this.error = null;
}

InstructedSectionData.prototype.setData = function(data) {
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
            var alternate_url = "https://canvas.uw.edu/courses/"+canvas_id;

            if (section.class_website_url == alternate_url) {
                section.class_website_url = null;
            }
        }
    }

    this.data = data;
};

function InstructedSectionDetailData(section_label) {
    this.url = "/api/v1/instructor_section_details/" + section_label;
    this.data = null;
    this.error = null;
}

InstructedSectionDetailData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructedSectionData = InstructedSectionData;
exports.InstructedSectionDetailData = InstructedSectionDetailData;
