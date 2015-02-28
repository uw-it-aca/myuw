var ec = require("../card/events.js"),
    assert = require("assert");
moment = require("../../vendor/js/moment.2.8.3.min.js");

describe('EventsCard', function(){
    describe('fix_event_time', function(){
        it('should strip range from timestamp', function(){
            var data = ec.EventsCard.fix_event_time('2013-04-16 10:00:00-07:00');
            assert.equal(data, '2013-04-16 10:00:00');
        });
        it('should handle timestamp without range', function(){
            var data = ec.EventsCard.fix_event_time('2013-04-16 10:00:00');
            assert.equal(data, '2013-04-16 10:00:00');
        });
        it('should handle a date', function(){
            var data = ec.EventsCard.fix_event_time('2013-04-16');
            assert.equal(data, '2013-04-16');
        });
    });

    describe('group_by_date', function(){
        var events = JSON.parse("[{\"start\": \"2013-04-16 10:00:00-07:00\", \"event_url\": \"http://www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110608069\", \"event_location\": \"Chemistry Building (CHB)\", \"summary\": \"Organic Chemistry Seminar: Asst. Prof. Alexander Statsyuk\"}, {\"start\": \"2013-04-16 18:00:00-07:00\", \"event_url\": \"http://www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110608069\", \"event_location\": \"Chemistry Building (CHB)\", \"summary\": \"Organic Chemistry Seminar: Steve\"}, {\"start\": \"2013-04-17 16:00:00-07:00\", \"event_url\": \"http://www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110741160\", \"event_location\": \"Chemistry Building (CHB)\", \"summary\": \"Organic Chemistry Seminar: Prof. Matthew Becker\"}, {\"start\": \"2013-04-19 16:00:00-07:00\", \"event_url\": \"http://www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\", \"event_location\": \"Chemistry Building (CHB)\", \"summary\": \"Organic Chemistry Seminar: Assoc. Prof. Ryan Shenvi\"}]");
        it('should sort events', function(){
            var data = ec.EventsCard.group_by_date(events);
            var shown = data[0];
            var hidden = data[1];
            assert.equal(hidden.length, '0');
            assert.equal(shown.length, '3');
            assert.equal(shown[0].date_string, 'Tuesday, April 16');
            assert.equal(shown[1].date_string, 'Wednesday, April 17');
            assert.equal(shown[2].date_string, 'Friday, April 19');
            assert.equal(shown[0].events.length, 2);
            assert.equal(shown[1].events.length, 1);
            assert.equal(shown[2].events.length, 1);
        });
    });

});

