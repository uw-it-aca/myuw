var Global = require("./global.js");
var Summary = require("../card/summary/schedule.js");

describe('SummaryScheduleCard', function(){
    before(function (done) {
        var render_id = 'instructor_summary_card';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/summary/schedule.js",
            ],
            templates: [
                'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
                'myuw/templates/handlebars/card/summary/section_panel.html',
                'myuw/templates/handlebars/card/summary/schedule.html',
                'myuw/templates/handlebars/card/summary/schedule_section.html'
            ]
        });

        Global.Environment.ajax_stub({
            '/api/v1/instructor_schedule/2013,spring': 'api/v1/instructor_schedule/2013-spring',
            '/api/v1/instructor_schedule/2013,summer': 'api/v1/instructor_schedule/2013-summer'
        });

        $(window).on("myuw:card_load", function () {
            done();
        });

        window.user.instructor = true;
        window.enabled_features = {};
        window.card_display_dates = { system_date: '2013-06-28 16:17' };
        SummaryScheduleCard.dom_target = $('#' + render_id);
        SummaryScheduleCard.term = '2013,summer';
        SummaryScheduleCard.render_init();
    });
    after(function () {
        Global.Environment.ajax_stub_restore();
    });
    describe("shows summary schedule", function() {
        it("Should render summary card", function() {
            assert.equal(SummaryScheduleCard.dom_target.find('.myuw-card-section-fulldivider').length, 1);
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
                'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
                'myuw/templates/handlebars/card/summary/section_panel.html',
                'myuw/templates/handlebars/card/summary/schedule.html',
                'myuw/templates/handlebars/card/summary/schedule_section.html'
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

describe('SortBySummerSubTerm', function(){
    var render_id = 'sub_term_unittest';

    Global.Environment.init({
        render_id: render_id,
        scripts: [
            "myuw/static/js/card/summary/schedule.js",
        ],
        templates: [
            'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
            'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
            'myuw/templates/handlebars/card/summary/section_panel.html',
            'myuw/templates/handlebars/card/summary/schedule.html',
            'myuw/templates/handlebars/card/summary/schedule_section.html'
        ]
    });
    var data = {};
    var instructed_course_data = {};
    instructed_course_data.sections = [];

    for(var i = 0; i < 3; i++) {
        instructed_course_data.sections.push({
            'summer_term': 'A-term'
        })
    }

    for(var i = 0; i < 5; i++){
        instructed_course_data.sections.push({
            'summer_term': 'B-term'
        })
    }

    for(var i = 0; i < 1; i++){
        instructed_course_data.sections.push({
            'summer_term': 'Full-term'
        })
    }

    Summary.SummaryScheduleCard.sort_sections_by_sub_term(data, instructed_course_data);

    assert.equal(typeof data.a_term, typeof []);
    assert.equal(typeof data.b_term, typeof []);
    assert.equal(typeof data.full_term, typeof []);

    assert.equal(data.a_term.length, 3);
    assert.equal(data.b_term.length, 5);
    assert.equal(data.full_term.length, 1);
});
