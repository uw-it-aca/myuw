function LibraryData() {
    BaseData.call(this, "/api/v1/library/");
}

LibraryData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.LibraryData = LibraryData;
