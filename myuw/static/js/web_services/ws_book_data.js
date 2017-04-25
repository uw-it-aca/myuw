function BookData(term) {
    this.url = "/api/v1/book/" + term;
    this.data = null;
    this.error = null;
}

BookData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.BookData = BookData;
