var Global = require("./global.js");

describe("TeachingPage", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/teaching.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/page/teaching.js",
                "myuw/static/js/card/teaching_resources.js",
                "myuw/static/js/card/instructor_schedule/load_course_cards.js",
                "myuw/static/js/card/instructor_schedule/course_content.js",
                "myuw/static/js/card/instructor_schedule/course_resource_panel.js",
                "myuw/static/js/card/instructor_schedule/course_sche_panel.js",
                "myuw/static/js/card/schedule/instructor_panel.js",
            ],
            templates: [
                'myuw/templates/teaching_base.html',
                'myuw/templates/teaching.html',
                'myuw/templates/handlebars/teaching.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_cards.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_content.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_section.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_class_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/class_website.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_sche_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondaries.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondary_section_panel.html',
                'myuw/templates/handlebars/card/schedule/instructor_panel.html',
                'myuw/templates/handlebars/card/quicklinks.html',
                'myuw/templates/handlebars/error.html',
            ]
        });

    });

    beforeEach(function (){
        window.page = "teaching";
        window.user.instructor = true;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
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
        window.sidebar_links_category = "pageteaching";
        Global.Environment.ajax_stub('api/v1/instructor_schedule/billsea-2013-spring');
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it('Desktop for billsea', function() {
        window.innerWidth = 800;
        Teaching.make_html();
        assert.equal(Teaching.is_desktop, true);
        assert.equal($('div[id="teaching_content_cards"]').length, 1);
        assert.equal($('div[id="teaching_content_cards"]').contents().length, 1);
        // InstructorCourseCards show
        assert.equal($('div[id="InstructorCourseCards"]').length, 1);
        assert.equal($('div[id="InstructorCourseCards"]')[0].getAttribute("style"), null);

        assert.equal($('div[id="instructor-term-spring-2013"]').length, 1);
        assert.equal($('div[data-identifier="PHYS 122 A"]').length, 1);
        assert.equal($('div[data-identifier="PHYS 122 B"]').length, 1);
        assert.equal($('div[data-identifier="PHYS 123 A"]').length, 1);
        assert.equal($('div[data-identifier="PHYS 123 B"]').length, 1);
        assert.equal($('div[data-identifier="PHYS 123 CA"]').length, 1);

        assert.equal($('div[id="teaching_accounts_cards"]').length, 1);
        assert.equal($('div[id="teaching_accounts_cards"]').contents().length, 1);
        assert.equal($('div[id="TeachingResourcesCard"]').length, 1);
        assert.equal($('div[id="TeachingResourcesCard"]')[0].getAttribute("style"), null);
    });

    it('Mobile for billsea', function() {
        window.innerWidth = 767;
        Teaching.make_html();
        assert.equal(Teaching.is_desktop, false);
        assert.equal($('h2[id="main-content-label"]').length, 1);
        assert.equal($('div[id="InstructorCourseCards"]').length, 1);
        assert.equal($('div[id="InstructorCourseCards"]')[0].getAttribute("style"), null);

        assert.equal($('div[id="TeachingResourcesCard"]').length, 1);
        assert.equal($('div[id="TeachingResourcesCard"]')[0].getAttribute("style"), null);

        assert.equal($('div[id="teaching_accounts_cards"]').length, 1);
        assert.equal($('div[id="teaching_accounts_cards"]').contents().length, 0);
    });

    it('Test resizing', function() {
        window.innerWidth = 1200;
        Teaching.make_html();
        assert.equal(Teaching.is_desktop, true);

        window.innerWidth = 700;
        $(window).trigger('resize');
        assert.equal(Teaching.is_desktop, false);
    });
});
