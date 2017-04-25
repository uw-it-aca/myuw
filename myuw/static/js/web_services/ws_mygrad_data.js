function MyGradData() {
    this.url = "/api/v1/grad/";
    this.data = null;
    this.error = null;
}

MyGradData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MyGradData = MyGradData;
