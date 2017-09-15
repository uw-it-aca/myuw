var Global = require("./global.js");

describe('SummaryScheduleCard', function(){
    before(function (done) {
        var render_id = 'instructor_summary_card';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/summary/schedule.js",
            ],
            templates: [
                'myuw/templates/handlebars/card/summary/section_panel.html',
                'myuw/templates/handlebars/card/summary/schedule.html',
            ]
        });

        Global.Environment.ajax_stub({
            '/api/v1/instructor_schedule/2013,spring': 'api/v1/instructor_schedule/2013-spring'
        });

        $(window).on("myuw:card_load", function () {
            done();
        });

        window.user.instructor = true;
        window.enabled_features = {};
        window.card_display_dates = { system_date: '2017-03-28 16:17' };
        SummaryScheduleCard.dom_target = $('#' + render_id);
        SummaryScheduleCard.term = '2013,spring';
        SummaryScheduleCard.render_init();
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
    describe("shows summary schedule", function() {
        it("Should render summary card", function() {
            assert.equal(SummaryScheduleCard.dom_target.find('.myuw-card-section').length, 6);
        });
    });
});

describe('SummaryScheduleCard', function(){
    before(function (done) {
        var render_id = 'instructor_summary_card';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/summary/schedule.js",
            ],
            templates: [
                'myuw/templates/handlebars/card/summary/section_panel.html',
                'myuw/templates/handlebars/card/summary/schedule.html'
            ]
        });

        Global.Environment.ajax_stub({
            '/api/v1/instructor_schedule/2012,autumn': 'api/v1/instructor_schedule/2012-autumn'
        });

        $(window).on("myuw:card_load", function () {
            done();
        });

        window.user.instructor = true;
        window.enabled_features = {};
        window.card_display_dates = { system_date: '2017-03-28 16:17' };
        SummaryScheduleCard.dom_target = $('#' + render_id);
        SummaryScheduleCard.term = '2012,autumn';
        SummaryScheduleCard.render_init();
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
    describe("shows non-teaching current term summary", function() {
        it("Should render non-teaching summary card", function() {
            assert.equal(SummaryScheduleCard.dom_target.find('.myuw-card-section').length, 0);
        });
    });
});
