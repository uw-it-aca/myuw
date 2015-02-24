var ec = require("../card/events.js"),
    assert = require("assert");

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

   

});

