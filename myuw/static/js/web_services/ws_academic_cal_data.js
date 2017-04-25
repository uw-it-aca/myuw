function AcademicCalendarEventData() {
    BaseData.call(this, "/api/v1/academic_events/");
}

AcademicCalendarEventData.prototype = Object.create(BaseData.prototype);


function CurrentAcademicCalendarEventData() {
    BaseData.call(this, "/api/v1/academic_events/current/");
}

CurrentAcademicCalendarEventData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.AcademicCalendarEventData = AcademicCalendarEventData;
exports.CurrentAcademicCalendarEventData = CurrentAcademicCalendarEventData;
