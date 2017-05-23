Global = require("./global.js");

describe('EventsCard', function(){
    describe('group_by_date', function(){
        before(function (done) {
            var render_id = 'events_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/events.js",
                    "myuw/static/js/web_services/ws_base.js",
                    "myuw/static/js/web_services/ws_event_data.js"
                ],
                templates: [
                    "myuw/templates/handlebars/card/events.html"
                ]
            });

            Global.Environment.ajax_stub('/api/v1/deptcal/index.json');

            $(window).on("myuw:card_load", function () {
                done();
            });

            EventsCard.dom_target = $('#' + render_id);
            EventsCard.render_init();
        });
        it ('should render card', function () {
            assert.equal($('.myuw-events').length, 1);
            assert.equal($('.myuw-events-list').length, 10);
        });
        it('should sort events', function(done){
            WebServiceData.require({event_data: new EventData()}, function (resources) {
                var event_data = resources['event_data'].data;
                var data = EventsCard.group_by_date(event_data.events);
                var shown = data[0];
                var hidden = data[1];
                assert.equal(hidden.length, 4);
                assert.equal(shown.length, 6);
                done();
            });
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
