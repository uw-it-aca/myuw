function BaseData(url) {
    this.url = url;
    this.data = null;
    this.error = null;
}

BaseData.prototype.setData = function (data) {
    // non-normalizing data setter shared among data objects
    this.data = data;
}

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.BaseData = BaseData;
