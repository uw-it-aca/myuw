function OQuarterData() {
    this.url = "/api/v1/oquarters/";
    this.data = null;
    this.error = null;
}

OQuarterData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.OQuarterData = OQuarterData;
