function EventData() {
    BaseData.call(this, "/api/v1/deptcal/");
}

EventData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.EventData = EventData;
