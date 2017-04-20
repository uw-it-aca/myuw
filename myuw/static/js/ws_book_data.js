function BookData(term) {
    this.name = 'book_data';
    this.url = "/api/v1/book/" + term;
    this.data = null;
    this.error = null;
}

BookData.prototype.setData = function(data) {
    // no normlized data
    this.data = data;
};
