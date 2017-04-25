var Global = require("./global.js");

describe('InstructorScheduleCards', function(){
    describe("Shows the instructed course cards", function() {
        before(function (done) {
            var render_id = 'instructor_course_cards';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/web_services/ws_course_data.js",
                    "myuw/static/js/web_services/ws_instructed_course_data.js",
                    "myuw/static/js/card/instructor_schedule/load_course_cards.js",
                    "myuw/static/js/card/instructor_schedule/course_card_content.js",
                    "myuw/static/js/card/instructor_schedule/course_sche_panel.js",
                    "myuw/static/js/card/instructor_schedule/course_resource_panel.js",
                    "myuw/static/js/card/schedule/instructor_panel.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/instructor_schedule/course_cards.html',
                    'myuw/templates/handlebars/card/instructor_schedule/course_card_content.html',
                    'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html',
                    'myuw/templates/handlebars/card/instructor_schedule/course_section.html',
                    'myuw/templates/handlebars/card/instructor_schedule/course_sche_panel.html',
                    'myuw/templates/handlebars/card/schedule/instructor_panel.html'
                ]
            });

            Global.Environment.ajax_stub('api/v1/instructor_schedule/2013-spring');

            window.enabled_features = { 'instructor_schedule': true };
            window.location.search = '?grading_date=2017-03-28 16:17';
            $(window).on("myuw:card_load", function () {
                done();
            });

            InstructorCourseCards.term = '2013-spring'
            InstructorCourseCards.dom_target = $('#' + render_id);
            InstructorCourseCards.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal($('.instructed-terms option:selected').val(), '2013,spring');
            assert.equal($('.card').length, 6);
            assert.equal($('.card .courseIDtitle').eq(1).html(), 'PHYS 121 A');
        });
        it("before grading open date", function(done) {
            window.location.search = '?grading_date=2017-03-02%2016:17';
            WebServiceData.require({inst_data: new InstructedCourseData('2013-spring')}, function (resources) {
                var data = resources['inst_data'].normalized();
                assert.equal(data.sections[1].grading_period_is_open, false);
                assert.equal(data.sections[1].opens_in_24_hours, false);
                assert.equal(data.sections[1].deadline_in_24_hours, false);
                done();
            });
        });
        it("immediately before grading open date", function(done) {
            window.location.search = '?grading_date=2017-03-26%2016:17';
            WebServiceData.require({inst_data: new InstructedCourseData('2013-spring')}, function (resources) {
                var data = resources['inst_data'].normalized();
                assert.equal(data.sections[1].grading_period_is_open, false);
                assert.equal(data.sections[1].opens_in_24_hours, true);
                assert.equal(data.sections[1].deadline_in_24_hours, false);
                done();
            });
        });
        it("while grading open", function(done) {
            window.location.search = '?grading_date=2017-03-27%2016:17';
            WebServiceData.require({inst_data: new InstructedCourseData('2013-spring')}, function (resources) {
                var data = resources['inst_data'].normalized();
                assert.equal(data.sections[0].grading_period_is_open, true);
                assert.equal(data.sections[0].grading_status.all_grades_submitted, true);
                assert.equal(data.sections[1].grading_status.all_grades_submitted, false);
                done();
            });
        });
        it("immediately before grading deadline", function(done) {
            window.location.search = '?grading_date=2017-03-28%2016:17';
            WebServiceData.require({inst_data: new InstructedCourseData('2013-spring')}, function (resources) {
                var data = resources['inst_data'].normalized();
                assert.equal(data.sections[1].grading_period_is_open, true);
                assert.equal(data.sections[1].opens_in_24_hours, false);
                assert.equal(data.sections[1].deadline_in_24_hours, true);
                done();
            });
        });
        it("after grading deadline", function(done) {
            window.location.search = '?grading_date=2017-04-02%2016:17';
            WebServiceData.require({inst_data: new InstructedCourseData('2013-spring')}, function (resources) {
                var data = resources['inst_data'].normalized();
                assert.equal(data.sections[1].grading_period_is_open, false);
                assert.equal(data.sections[1].opens_in_24_hours, false);
                assert.equal(data.sections[1].deadline_in_24_hours, false);
                done();
            });
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
