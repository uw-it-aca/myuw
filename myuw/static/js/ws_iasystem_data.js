function IASystemData(term) {
    this.url = "/api/v1/ias/";
    this.data = null;
    this.error = null;
    this.accepts = {html: "application/json"};
}

IASystemData.prototype.setData = function(data) {
    // normalize
    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.IASystemData = IASystemData;
