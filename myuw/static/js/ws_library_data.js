function LibraryData() {
    this.url = "/api/v1/library/";
    this.data = null;
    this.error = null;
}

LibraryData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.LibraryData = LibraryData;
