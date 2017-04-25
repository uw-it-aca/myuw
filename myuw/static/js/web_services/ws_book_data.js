function BookData(term) {
    BaseData.call(this, "/api/v1/book/" + term);
}

BookData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.BookData = BookData;
