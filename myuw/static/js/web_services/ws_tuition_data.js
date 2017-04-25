function TuitionData() {
    BaseData.call(this, "/api/v1/finance/");
}

TuitionData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TuitionData = TuitionData;
