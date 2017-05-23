function OQuarterData() {
    BaseData.call(this, "/api/v1/oquarters/");
}

OQuarterData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.OQuarterData = OQuarterData;
