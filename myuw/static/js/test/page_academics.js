var Global = require("./global.js");

describe("AcademicsPage", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/academics.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/page/academics.js",
                "myuw/static/js/visual_schedule.js",
                "myuw/static/js/textbooks.js",
                "myuw/static/js/future.js",
                "myuw/static/js/grades.js",
                "myuw/static/js/card/grad_committee.js",
                "myuw/static/js/card/grad_status.js",
                "myuw/static/js/card/alumni.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/card/future_quarter.js",
                "myuw/static/js/card/grade.js",
                "myuw/static/js/card/outage.js",
                "myuw/static/js/card/schedule/load_course_cards.js",
                "myuw/static/js/card/schedule/prev_course_cards.js",
                "myuw/static/js/card/schedule/load_evals.js",
                "myuw/static/js/card/schedule/course_content.js",
                "myuw/static/js/card/schedule/course_sche_panel.js",
                "myuw/static/js/card/schedule/course_resource_panel.js",
                "myuw/static/js/card/schedule/instructor_panel.js",
                "myuw/static/js/card/schedule/visual.js",
                "myuw/static/js/card/schedule/final_panel.js",
                "myuw/static/js/card/reg_status.js",
                "myuw/static/js/card/sidebar_links.js",
                "myuw/static/js/card/textbook.js",
                "myuw/static/js/card/summer_reg_status.js",
                "myuw/static/js/card/former_student/transcripts.js",
                "myuw/static/js/card/former_student/ctnu_edu.js",
            ],
            templates: [
                'myuw/templates/academics.html',
                'myuw/templates/handlebars/academics.html',
                'myuw/templates/handlebars/error.html',
                'myuw/templates/handlebars/future_410_error.html',
                'myuw/templates/handlebars/grades.html',
                'myuw/templates/handlebars/loading.html',
                'myuw/templates/handlebars/quarter_books.html',
                'myuw/templates/handlebars/future.html',
                'myuw/templates/handlebars/visual_schedule.html',
                'myuw/templates/handlebars/card/sidebar_links.html',
                'myuw/templates/handlebars/card/future_quarter.html',
                'myuw/templates/handlebars/card/schedule/course_cards.html',
                'myuw/templates/handlebars/card/schedule/course_content.html',
                'myuw/templates/handlebars/card/schedule/course_sche_panel.html',
                'myuw/templates/handlebars/card/schedule/eval_panel.html',
                'myuw/templates/handlebars/card/schedule/course_resource_panel.html',
                'myuw/templates/handlebars/card/schedule/instructor_panel.html',
                'myuw/templates/handlebars/card/schedule/final_panel.html',
                'myuw/templates/handlebars/card/schedule/sp_final.html',
                'myuw/templates/handlebars/card/schedule/final_day.html',
                'myuw/templates/handlebars/card/schedule/visual.html',
                'myuw/templates/handlebars/card/schedule/visual_day.html',
                'myuw/templates/handlebars/card/textbook.html',
                'myuw/templates/handlebars/card/grade.html',
                'myuw/templates/handlebars/card/grad_status.html',
                'myuw/templates/handlebars/card/grad_committee.html',
                'myuw/templates/handlebars/card/no_course.html',
                'myuw/templates/handlebars/card/loading.html',
                'myuw/templates/handlebars/card/error.html',
                'myuw/templates/handlebars/card/outage.html',
            ]
        });

    });

    beforeEach(function (){
        window.page = "academics";
        window.user.student = true;
        window.user.grad = false;
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
        window.sidebar_links_category = "pageacademics";
        window.card_display_dates = { "system_date": '2013-04-15 00:01' };
        window.card_display_dates.is_after_last_day_of_classes = false;
        window.card_display_dates.is_summer = false;
        window.card_display_dates.is_before_first_day_of_term = false;
        Global.Environment.ajax_stub({
            '/api/v1/schedule/current': 'api/v1/schedule/javerage_2013_spring.json',
            '/api/v1/oquarters/': 'api/v1/oquarters/javerage_2013_spring.json',
            '/api/v1/visual_schedule/current': 'api/v1/visual_schedule/javerage_2013_spring.json',
            '/api/v1/book/current': 'api/v1/book/javerage_2013_spring.json',
            '/api/v1/categorylinks/pageacademics': 'api/v1/categorylinks/pageacademics/javerage.json',
            '/api/v1/grad/': 'api/v1/grad/seagrad.json',
        });

    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });


    it('Test body cards', function() {
        var body_cards = Academics.body_cards();
        assert.deepEqual(body_cards,
                         [OutageCard,
                          GradeCard,
                          CourseCards,
                          VisualScheduleCard,
                          TextbookCard,
                          PrevTermCourseCards,
                          PrevTermCourseCards1,
                          GradStatusCard,
                          GradCommitteeCard,
                          FutureQuarterCardA,
                          FutureQuarterCard1]);
    });

    it('Desktop cards for javerage', function() {
        window.innerWidth = 800;
        Academics.make_html();
        assert.equal(Academics.is_desktop, true);

        assert.equal($('div[id="academics_content_cards"]').length, 1);
        assert.equal($('div[id="academics_content_cards"]').contents().length, 11);
        // OutageCard hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[0].getAttribute("id"), "OutageCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[0].getAttribute("style"), "display: none;");

        // GradeCard hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[1].getAttribute("id"), "GradeCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[1].getAttribute("style"), "display: none;");

        // CourseCards show
        assert.equal($('div[id="academics_content_cards"]').contents()[2].getAttribute("id"), "CourseCards");
        assert.equal($('div[id="academics_content_cards"]').contents()[2].getAttribute("style"), null);

        // VisualScheduleCard show
        assert.equal($('div[id="academics_content_cards"]').contents()[3].getAttribute("id"), "VisualScheduleCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[3].getAttribute("style"), null);

        // TextbookCard hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[4].getAttribute("id"), "TextbookCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[4].getAttribute("style"), "display: none;");

        // PrevTermCourseCards hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[5].getAttribute("id"), "PrevTermCourseCards");
        assert.equal($('div[id="academics_content_cards"]').contents()[5].getAttribute("style"), "display: none;");

        // PrevTermCourseCards1 hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[6].getAttribute("id"), "PrevTermCourseCards1");
        assert.equal($('div[id="academics_content_cards"]').contents()[6].getAttribute("style"), "display: none;");

        // GradStatusCard hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[7].getAttribute("id"), "GradStatusCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[7].getAttribute("style"), "display: none;");

        // GradCommitteeCard hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[8].getAttribute("id"), "GradCommitteeCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[8].getAttribute("style"), "display: none;");

        // FutureQuarterCardA show
        assert.equal($('div[id="academics_content_cards"]').contents()[9].getAttribute("id"), "FutureQuarterCardA");
        assert.equal($('div[id="academics_content_cards"]').contents()[9].getAttribute("style"), null);

        // FutureQuarterCard1 hidden
        assert.equal($('div[id="academics_content_cards"]').contents()[10].getAttribute("id"), "FutureQuarterCard1");
        assert.equal($('div[id="academics_content_cards"]').contents()[10].getAttribute("style"), 'display: none;');

        assert.equal($('div[id="academics_sidebar_cards"]').length, 1);
        assert.equal($('div[id="academics_sidebar_cards"]').contents().length, 1);
        // SidebarLinks show
        assert.equal($('div[id="academics_sidebar_cards"]').contents()[0].getAttribute("id"), "SidebarLinks");
        assert.equal($('div[id="academics_sidebar_cards"]').contents()[0].getAttribute("style"), null);
    });

    it('Test mobile plus grad cards', function() {
        window.innerWidth = 767;
        window.user.grad = true;

        Academics.make_html();
        assert.equal(Academics.is_desktop, false);

        assert.equal($('div[id="academics_content_cards"]').length, 1);
        assert.equal($('div[id="academics_content_cards"]').contents().length, 12);

        // GradStatusCard show
        assert.equal($('div[id="academics_content_cards"]').contents()[7].getAttribute("id"), "GradStatusCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[7].getAttribute("style"), null);

        // GradCommitteeCard show
        assert.equal($('div[id="academics_content_cards"]').contents()[8].getAttribute("id"), "GradCommitteeCard");
        assert.equal($('div[id="academics_content_cards"]').contents()[8].getAttribute("style"), null);

        // SidebarLinks show at the end of content column
        assert.equal($('div[id="academics_content_cards"]').contents()[11].getAttribute("id"), "SidebarLinks");
        assert.equal($('div[id="academics_content_cards"]').contents()[11].getAttribute("style"), null);

        assert.equal($('div[id="academics_sidebar_cards"]').length, 1);
        assert.equal($('div[id="academics_sidebar_cards"]').contents().length, 0);
    });
});
