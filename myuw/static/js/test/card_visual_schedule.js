var Global = require("./global.js");

describe("VisualScheduleCard", function() {
    before(function (done) {
        var render_id = 'test_visual_schedule';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/visual_schedule.js",
                "myuw/static/js/card/schedule/visual.js",
                "myuw/static/js/card/schedule/final_panel.js",
                "myuw/static/js/card/schedule/sp_final.js"
            ],
            templates: [
                'myuw/templates/handlebars/visual_schedule.html',
                'myuw/templates/handlebars/card/schedule/visual.html',
                'myuw/templates/handlebars/card/schedule/visual_day.html',
                'myuw/templates/handlebars/card/schedule/final_day.html',
                'myuw/templates/handlebars/card/schedule/final_panel.html'
            ]
        });

        window.card_display_dates = {};
        VisualScheduleCard.dom_target = $('#' + render_id);
        done();
    });

    describe('card renders', function() {
        before(function (done) {
            Global.Environment.ajax_stub({
                '/api/v1/visual_schedule/current': 'api/v1/schedule/visual.json'
            });

            window.enabled_features = { 'instructor_schedule': true };

            //handle the two card load events the VS fires for inst+stu schedules
            var has_loaded = false;
            $(window).on("myuw:card_load", function () {
                if(!has_loaded){
                    done();
                    has_loaded = true;
                }
            });

            VisualScheduleCard.term = 'current';
            VisualScheduleCard.render_init();
        });

        it('for netid eight', function () {
            var $schedule = VisualScheduleCard.dom_target.find('.visual-schedule');
            //console.log($schedule.html());
            assert.equal($schedule.length, 1);
            assert.equal($schedule.find('> .five-day').length, 5);
            assert.equal($schedule.find('> .five-day').eq(0).find('.visual-course').length, 1);
            assert.equal($schedule.find('> .five-day').eq(4).find('.visual-course').length, 1);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });

    //describe('_get_default_period', function() {
    //    it('should get the default period', function() {
    //        window.card_display_dates.comparison_date = "2017-06-05";
    //        var start = moment.utc("2017-06-01");
    //        var end = moment.utc("2017-06-12");
    //        var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
    //
    //        var default_period = VisualScheduleCard._get_default_period(null, weeks);
    //        assert.equal(default_period, "23")
    //    });
    //
    //    it('should default to first if today is outside of the schedule range', function() {
    //        window.card_display_dates.comparison_date = "2017-09-05";
    //        var start = moment.utc("2017-06-01");
    //        var end = moment.utc("2017-06-12");
    //        var weeks = VisualScheduleCard._get_weeks_from_range([start, end]);
    //
    //        var default_period = VisualScheduleCard._get_default_period(weeks, null);
    //        assert.equal(default_period, "22")
    //    });
    //});
});

