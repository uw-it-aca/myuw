function ThriveHistoryData() {
    BaseData.call(this, "/api/v1/thrive/?history=1");
}

ThriveHistoryData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ThriveHistoryData = ThriveHistoryData;
