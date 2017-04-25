function InstructedSectionEmailListData(section_label) {
    BaseData.call(this, "/api/v1/emaillist/" + section_label);
}

InstructedSectionEmailListData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructedSectionEmailListData = InstructedSectionEmailListData;
