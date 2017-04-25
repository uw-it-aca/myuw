function TuitionData() {
    this.url = "/api/v1/finance/";
    this.data = null;
    this.error = null;
}

TuitionData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TuitionData = TuitionData;
