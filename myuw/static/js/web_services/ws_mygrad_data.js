function MyGradData() {
    BaseData.call(this, "/api/v1/grad/");
}

MyGradData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MyGradData = MyGradData;
