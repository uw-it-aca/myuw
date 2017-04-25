function InstructedSectionData(section_label) {
    this.url = "/api/v1/instructor_section/" + section_label;
    this.data = null;
    this.error = null;
}

InstructedSectionData.prototype.setData = CourseData.prototype.setData;

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
