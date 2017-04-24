function ThriveData() {
    this.url = "/api/v1/thrive/";
    this.data = null;
    this.error = null;
}

ThriveData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ThriveData = ThriveData;
