function InstructorData(instructor_regid) {
    BaseData.call(this, "/api/v1/person/" + instructor_regid);
}

InstructorData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructorData = InstructorData;
