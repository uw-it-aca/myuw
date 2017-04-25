function UPassData() {
    BaseData.call(this, "/api/v1/upass/");
}

UPassData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.UPassData = UPassData;
