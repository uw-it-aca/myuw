function ThriveHistoryData() {
    this.url = "/api/v1/thrive/?history=1";
    this.data = null;
    this.error = null;
}

ThriveHistoryData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ThriveHistoryData = ThriveHistoryData;
