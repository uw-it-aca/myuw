function GradeData(term) {
    this.url = "/api/v1/grades/" + term;
    this.data = null;
    this.error = null;
}

GradeData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.GradeData = GradeData;
