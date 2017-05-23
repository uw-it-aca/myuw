function DirectoryData() {
    BaseData.call(this, "/api/v1/directory/");
}

DirectoryData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.DirectoryData = DirectoryData;
