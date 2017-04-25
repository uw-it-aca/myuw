function CategoryLinkData(category) {
    BaseData.call(this, "/api/v1/categorylinks/" + category);
    this.accepts = {html: "application/json"};
}

CategoryLinkData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.CategoryLinkData = CategoryLinkData;
