function CategoryLinkData(category) {
    this.url = "/api/v1/categorylinks/" + category;
    this.data = null;
    this.error = null;
    this.accepts = {html: "application/json"};
}

CategoryLinkData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.CategoryLinkData = CategoryLinkData;
