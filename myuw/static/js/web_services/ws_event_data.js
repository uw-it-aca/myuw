function EventData() {
    this.url = '/api/v1/deptcal/';
    this.data = null;
    this.error = null;
}

EventData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.EventData = EventData;
