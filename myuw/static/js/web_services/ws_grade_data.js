function GradeData(term) {
    BaseData.call(this, "/api/v1/grades/" + term);
}

GradeData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.GradeData = GradeData;
