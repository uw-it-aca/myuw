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
            ]
        });
        Global.Environment.ajax_stub('api/v1/instructor_schedule/billsea-2013-spring');

    });

    beforeEach(function (){
        window.page = "teaching";
        window.user.instructor = true;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
    });

    describe('load teaching page cards', function() {
        
        it('Desktop should have course card and resource card', function() {
            window.innerWidth = 800;
            Teaching.make_html();
            assert.equal(Teaching.is_desktop, true);
            assert.equal($('h2[id="main-content-label"]').length, 1);
            assert.equal($('div[id="InstructorCourseCards"]').length, 1);
            assert.equal($('div[data-name="CourseCard"]').length, 7);
            assert.equal($('div[id="TeachingResourcesCard"]').length, 1);
        });

        it('Mobile should have course card and resource card', function() {
            window.innerWidth = 767;
            Teaching.make_html();
            assert.equal(Teaching.is_desktop, false);
            assert.equal($('h2[id="main-content-label"]').length, 1);
            assert.equal($('div[id="InstructorCourseCards"]').length, 1);
            assert.equal($('div[id="TeachingResourcesCard"]').length, 1);
        });

    });
});

