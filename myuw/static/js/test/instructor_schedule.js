var Global = require("./global.js");

describe('InstructorScheduleCards', function(){
    describe("Shows the instructed course cards", function() {
        before(function (done) {
            var render_id = 'instructor_course_cards';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
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

            Global.Environment.ajax_stub('api/v1/instructor_schedule/2013-summer');

            window.enabled_features = { 'instructor_schedule': true };
            window.card_display_dates = { system_date: '2017-06-25 17:59' };
            window.user.instructor = true;
            // first_day_quarter: 2013-06-24
            // grading_period_open: 2013-08-16 08:00
            // aterm_grading_period_open: 2013-07-18 08:00
            // grade_submission_deadline: 2013-08-27 17:00

            $(window).on("myuw:card_load", function () {
                done();
            });

            InstructorCourseCards.term = '2013,summer';
            InstructorCourseCards.dom_target = $('#' + render_id);
            InstructorCourseCards.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal($('div[data-type="card"]').length, 1);
            assert.equal($('div[data-identifier="TRAIN 101 A"]').length, 1);
        });
        it("before grading open date", function() {
            var data = WSData.normalized_instructed_course_data('2013,summer');
            assert.equal(data.sections[0].grading_period_is_open, false);
            assert.equal(data.sections[0].opens_in_24_hours, false);
            assert.equal(data.sections[0].deadline_in_24_hours, false);
        });
        it("immediately before grading open date", function() {
            // only change the ref moment in _normalize_instructed_data
            window.location.search = '?grading_date=2013-08-15%2018:00';
            var data = WSData.normalized_instructed_course_data('2013,summer');
            assert.equal(data.sections[0].grading_period_is_open, false);
            assert.equal(data.sections[0].opens_in_24_hours, true);
            assert.equal(data.sections[0].deadline_in_24_hours, false);
        });
        it("while grading open", function() {
            // only change the ref moment in _normalize_instructed_data
            window.location.search = '?grading_date=2013-08-17%2018:00';
            var data = WSData.normalized_instructed_course_data('2013,summer');
            assert.equal(data.sections[0].grading_period_is_open, true);
            assert.equal(data.sections[0].grading_status.all_grades_submitted, true);
        });
        it("immediately before grading deadline", function() {
            // only change the ref moment in _normalize_instructed_data
            window.location.search = '?grading_date=2013-08-26%2018:00';
            var data = WSData.normalized_instructed_course_data('2013,summer');
            assert.equal(data.sections[0].grading_period_is_open, true);
            assert.equal(data.sections[0].opens_in_24_hours, false);
            assert.equal(data.sections[0].deadline_in_24_hours, true);
        });
        it("after grading deadline", function() {
            // only change the ref moment in _normalize_instructed_data
            window.location.search = '?grading_date=2013-08-27%2018:00';
            var data = WSData.normalized_instructed_course_data('2013,summer');
            assert.equal(data.sections[0].grading_period_is_open, false);
            assert.equal(data.sections[0].opens_in_24_hours, false);
            assert.equal(data.sections[0].deadline_in_24_hours, false);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
