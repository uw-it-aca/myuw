function MyGradData() {
    this.url = "/api/v1/grad/";
    this.data = null;
    this.error = null;
}

MyGradData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MyGradData = MyGradData;
