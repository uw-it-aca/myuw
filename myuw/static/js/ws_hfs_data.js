function HFSData() {
    this.url = "/api/v1/hfs/";
    this.data = null;
    this.error = null;
}

HFSData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.HFSData = HFSData;
