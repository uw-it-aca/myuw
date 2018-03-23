var Global = require("./global.js");

describe("TeachingPage", function() {
    before(function () {
        var render_id = 'render_teaching_resources_card';

        Global.Environment.init({
            render_id: render_id,
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
                "myuw/static/js/card/instructor_schedule/load_section_card.js",
            ],
            templates: [
                'myuw/templates/teaching_base.html',
                'myuw/templates/teaching.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_cards.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_content.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_eval.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_grading.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_sche_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_section.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondaries.html',
                'myuw/templates/handlebars/card/instructor_schedule/secondary_section_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/term_panel.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/class_website.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_class_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/course_stats.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/email_list.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/online_tools.html',
                'myuw/templates/handlebars/card/instructor_schedule/course_resource/textbooks.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_bldg.html',
                'myuw/templates/handlebars/card/schedule/course_sche_col_days.html',
            ]
        });
        
        Global.Environment.ajax_stub('api/v1/instructor_schedule/billsea-2013-spring');

        window.card_display_dates = { system_date: '2013-04-15 00:01' };
        window.innerWidth = 800;
        Teaching.is_desktop = true;
        Teaching.make_html();

    });

    beforeEach(function (){
        window.page = "teaching";
        window.user.instructor = true;
        window.user.seattle = true;
    });

    describe('load desktop cards', function() {
        
        it('Should have teaching content card and resource card', function() {
            assert.equal($('h2[id="main-content-label"]').length, 1);
            assert.equal($('div[id="InstructorCourseCards"]').length, 1);
            assert.equal($('div[id="TeachingResourcesCard"]').length, 1);
            // assert.equal($('div[data-name="CourseCard"]').length, 7);
        });

    });
});

