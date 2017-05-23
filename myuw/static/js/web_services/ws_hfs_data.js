function HFSData() {
    BaseData.call(this, "/api/v1/hfs/");
}

HFSData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.HFSData = HFSData;
