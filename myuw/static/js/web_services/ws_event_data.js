function EventData() {
    this.url = '/api/v1/deptcal/';
    this.data = null;
    this.error = null;
}

EventData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.EventData = EventData;
