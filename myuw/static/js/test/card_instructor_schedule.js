var Global = require("./global.js");

describe('InstructorScheduleCards for 2013 summer', function(){

    before(function () {
        var render_id = 'instructor_course_cards';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/instructor_schedule/load_course_cards.js",
                "myuw/static/js/card/instructor_schedule/course_content.js",
                "myuw/static/js/card/instructor_schedule/course_sche_panel.js",
                "myuw/static/js/card/instructor_schedule/course_resource_panel.js",
                "myuw/static/js/card/schedule/instructor_panel.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/instructor_schedule/course_grading.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_cards.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_content.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_grading.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_eval.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_class_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_stats.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/class_website.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/email_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/online_tools.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/textbooks.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_section.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_sche_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondaries.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondary_section_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/term_panel.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
                'myuw/templates/handlebars/card/schedule/instructor_panel.html'
            ]
        });
    });

    beforeEach(function (){
        Global.Environment.ajax_stub('api/v1/instructor_schedule/2013-summer');

        window.card_display_dates = { system_date: '2017-06-25 17:59' };
        window.user.instructor = true;
        window.term_data = {
            break_quarter: "summer",
            break_year: "2013",
            first_day: new Date(2013, 6, 24),
            is_break: false,
            is_finals: false,
            last_day: new Date(2013, 8, 23),
            quarter: "spring",
            today: "Monday, April 15, 2013",
            today_date: new Date(2013, 5, 25),
            year: "2013"
        };

        // grading_period_open: 2013-08-16 08:00
        // aterm_grading_period_open: 2013-07-18 08:00
        // grade_submission_deadline: 2013-08-27 17:00

        InstructorCourseCards.term = '2013,summer';
        InstructorCourseCards.dom_target = $('#' + 'instructor_course_cards');
        InstructorCourseCards.render_init();
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it("Should render instructor card", function() {
        assert.equal($('div[data-type="card"]').length, 1);
        assert.equal($('div[data-identifier="TRAIN 101 A"]').length, 1);
    });
    it("before grading open date", function() {
        var data = WSData.instructed_course_data('2013,summer', true);
        assert.equal(data.sections[0].grading_period_is_open, false);
        assert.equal(data.sections[0].opens_in_24_hours, false);
        assert.equal(data.sections[0].deadline_in_24_hours, false);
    });
    it("immediately before grading open date", function() {
        // only change the ref moment in _normalize_instructed_data
        dom.reconfigure({url: "http://www.foo.com?grading_date=2013-08-15%2018:00"});
        var data = WSData.instructed_course_data('2013,summer', true);
        assert.equal(data.sections[0].grading_period_is_open, false);
        assert.equal(data.sections[0].opens_in_24_hours, true);
        assert.equal(data.sections[0].deadline_in_24_hours, false);
    });
    it("while grading open", function() {
        // only change the ref moment in _normalize_instructed_data
        dom.reconfigure({url: "http://www.foo.com?grading_date=2013-08-17%2018:00"});
        var data = WSData.instructed_course_data('2013,summer', true);
        assert.equal(data.sections[0].grading_period_is_open, true);
        assert.equal(data.sections[0].grading_status.all_grades_submitted, true);
    });
    it("immediately before grading deadline", function() {
        // only change the ref moment in _normalize_instructed_data
        dom.reconfigure({url: "http://www.foo.com?grading_date=2013-08-26%2018:00"});
        var data = WSData.instructed_course_data('2013,summer', true);
        assert.equal(data.sections[0].grading_period_is_open, true);
        assert.equal(data.sections[0].opens_in_24_hours, false);
        assert.equal(data.sections[0].deadline_in_24_hours, true);
    });
    it("after grading deadline", function() {
        // only change the ref moment in _normalize_instructed_data
        dom.reconfigure({url: "http://www.foo.com?grading_date=2013-08-27%2018:00"});
        var data = WSData.instructed_course_data('2013,summer', true);
        assert.equal(data.sections[0].grading_period_is_open, false);
        assert.equal(data.sections[0].opens_in_24_hours, false);
        assert.equal(data.sections[0].deadline_in_24_hours, false);
    });
});

describe('InstructorScheduleCards for billpce 2013 spring', function(){

    before(function () {
        var render_id = 'instructor_course_cards';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/instructor_schedule/load_course_cards.js",
                "myuw/static/js/card/instructor_schedule/course_content.js",
                "myuw/static/js/card/instructor_schedule/course_sche_panel.js",
                "myuw/static/js/card/instructor_schedule/course_resource_panel.js",
                "myuw/static/js/card/schedule/instructor_panel.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/instructor_schedule/course_cards.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_content.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_grading.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_eval.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_class_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_stats.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/class_website.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/email_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/online_tools.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/textbooks.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_section.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_sche_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondaries.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondary_section_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/term_panel.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
                'myuw/templates/handlebars/card/schedule/instructor_panel.html'
            ]
        });
    });

    beforeEach(function (){
        Global.Environment.ajax_stub('api/v1/instructor_schedule/billpce-2013-spring');

        window.card_display_dates = { system_date: '2017-06-25 17:59' };
        window.user.instructor = true;
        window.term_data = {
            break_quarter: "spring",
            break_year: "2013",
            first_day: new Date(2013, 4, 1),
            is_break: false,
            is_finals: false,
            last_day: new Date(2013, 6, 7),
            quarter: "spring",
            today: "Monday, April 15, 2013",
            today_date: new Date(2013, 4, 15),
            year: "2013"
        };

        InstructorCourseCards.term = '2013,spring';
        InstructorCourseCards.dom_target = $('#' + 'instructor_course_cards');
        InstructorCourseCards.render_init();
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it("Should render instructor card", function() {
        assert.equal($('div[class="myuw-card instructor-course-card"]').length, 5);
        assert.equal($('div[data-identifier="AAES 150 A"]').length, 1);
        assert.equal($('div[id="instructor_course_card_content0"]').length, 1);
        assert.equal($('div[id="instructor_sche_on_course_card0"]').length, 1);
        assert.equal($('div[id="instructor_course_resource0"]').length, 1);
        assert.equal($('a[class="course_class_list"]').length, 5);
        assert.equal($('a[class="myuw-iconlink course-classlist-download download_classlist_csv"]').length, 5);
        assert.equal($('a[class="myuwclass"]').length, 3);
        assert.equal($('a[class="myuwclass"]')[0].getAttribute("rel"), "AAES 150 A");
    });
});
