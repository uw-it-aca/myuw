function ThriveData() {
    BaseData.call(this, "/api/v1/thrive/");
}

ThriveData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ThriveData = ThriveData;
