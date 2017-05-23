function InstructedSectionData(section_label) {
    BaseData.call(this, "/api/v1/instructor_section/" + section_label);
}

InstructedSectionData.prototype = Object.create(BaseData.prototype);

function InstructedSectionDetailData(section_label) {
    BaseData.call(this, "/api/v1/instructor_section_details/" + section_label);
}

InstructedSectionDetailData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructedSectionData = InstructedSectionData;
exports.InstructedSectionDetailData = InstructedSectionDetailData;
