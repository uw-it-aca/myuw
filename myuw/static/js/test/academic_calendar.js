var Global = require("./global.js");

describe("AcademicCalendarPage", function() {
    before(function () {
        Global.Environment.init({
                                    scripts: [
                                        "myuw/static/js/academic_calendar.js"
                                    ]
                                });
    });

    describe('group_events_by_term', function() {
        it('should group events out of order', function() {
            var events = [{
                "category": "Dates of Instruction",
                "start": "2017-08-25",
                "event_url": "http://www.washington.edu/calendar/academic/?trumbaEmbed=view%3Devent%26eventid%3D106271674",
                "end": "2017-08-25",
                "year": "2017",
                "is_all_day": true,
                "myuw_categories": {
                    "all": true,
                    "classes": true
                },
                "quarter": "Summer",
                "summary": "Last Day of Instruction for Summer B-term 2017"
            }, {
                "category": "Dates of Instruction",
                "start": "2017-07-19",
                "event_url": "http://www.washington.edu/calendar/academic/?trumbaEmbed=view%3Devent%26eventid%3D108218075",
                "end": "2017-07-19",
                "year": 2017,
                "is_all_day": true,
                "myuw_categories": {
                    "all": true,
                    "classes": true
                },
                "quarter": "Spring",
                "summary": "Last Day of Instruction for Summer A-term 2017"
            }, {
                "category": "Dates of Instruction",
                "start": "2017-07-20",
                "event_url": "http://www.washington.edu/calendar/academic/?trumbaEmbed=view%3Devent%26eventid%3D108218068",
                "end": "2017-07-20",
                "year": 2017,
                "is_all_day": true,
                "myuw_categories": {
                    "all": true,
                    "classes": true
                },
                "quarter": "Summer",
                "summary": "Instruction Begins for Summer Quarter B-term 2017"
            }];
            var grouped_events = AcademicCalendar.group_events_by_term(events);

            assert.equal(grouped_events.length, 2);
            assert.equal(grouped_events[0].events.length, 2);
            assert.equal(grouped_events[1].events.length, 1);
        });

    });
});

