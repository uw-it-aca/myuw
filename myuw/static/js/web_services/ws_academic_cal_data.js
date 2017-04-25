function AcademicCalendarEventData() {
    this.url = "/api/v1/academic_events/";
    this.data = null;
    this.error = null;
}

AcademicCalendarEventData.prototype.setData = WebServiceData.setData;

function CurrentAcademicCalendarEventData() {
    this.url = "/api/v1/academic_events/current/";
    this.data = null;
    this.error = null;
}

CurrentAcademicCalendarEventData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AcademicCalendarEventData = AcademicCalendarEventData;
exports.CurrentAcademicCalendarEventData = CurrentAcademicCalendarEventData;
