function AcademicCalendarEventData() {
    this.url = "/api/v1/academic_events/";
    this.data = null;
    this.error = null;
}

AcademicCalendarEventData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

function CurrentAcademicCalendarEventData() {
    this.url = "/api/v1/academic_events/current/";
    this.data = null;
    this.error = null;
}

CurrentAcademicCalendarEventData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AcademicCalendarEventData = AcademicCalendarEventData;
exports.CurrentAcademicCalendarEventData = CurrentAcademicCalendarEventData;
