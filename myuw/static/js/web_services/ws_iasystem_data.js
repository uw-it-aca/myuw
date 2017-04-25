function IASystemData() {
    BaseData.call(this, "/api/v1/ias/");
    this.accepts = {html: "application/json"};
}

IASystemData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.IASystemData = IASystemData;
