var Global = require("./global.js");

describe("HomePage", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/landing.js",
                "myuw/static/js/banner/notice.js",
                "myuw/static/js/textbooks.js",
                "myuw/static/js/notices.js",
                "myuw/static/js/visual_schedule.js",
                "myuw/static/js/resources.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/resources.js",
                "myuw/static/js/card/resources_explore.js",
                "myuw/static/js/card/alumni.js",
                "myuw/static/js/card/calendars/acad_cal_sp.js",
                "myuw/static/js/card/calendars/events.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/card/husky_experience.js",
                "myuw/static/js/card/future_quarter.js",
                "myuw/static/js/card/grade.js",
                "myuw/static/js/card/new_student/ns_thank_you.js",
                "myuw/static/js/card/new_student/ns_to_register.js",
                "myuw/static/js/card/new_student/ns_critical_info.js",
                "myuw/static/js/card/new_student/ns_international_stu.js",
                "myuw/static/js/card/new_student/ns_summer_efs.js",
                "myuw/static/js/card/outage.js",
                "myuw/static/js/card/quicklinks.js",
                "myuw/static/js/card/reg_status.js",
                "myuw/static/js/card/schedule/visual.js",
                "myuw/static/js/card/summary/accounts.js",
                "myuw/static/js/card/summary/future_schedule.js",
                "myuw/static/js/card/summary/schedule.js",
                "myuw/static/js/card/textbook.js",
                "myuw/static/js/card/thrive.js",
                "myuw/static/js/card/summer_reg_status.js",
                "myuw/static/js/card/seattle_application.js",
                "myuw/static/js/card/bothell_application.js",
                "myuw/static/js/card/tacoma_application.js",
                "myuw/static/js/card/former_student/transcripts.js",
                "myuw/static/js/card/former_student/ctnu_edu.js",
                "myuw/static/js/card/accounts/uwnetid.js",
                "myuw/static/js/card/accounts/hr_payroll_card.js",
                "myuw/static/js/card/former_employee/retiree.js",
            ],
            templates: [
                'myuw/templates/index.html',
            ]
        });

    });

    beforeEach(function (){
        window.page = "home";
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

        window.card_display_dates = { "system_date": '2013-04-15 00:01' };
        Global.Environment.ajax_stub({
            '/api/v1/hfs/': 'api/v1/hfs/javerage.json',
            '/api/v1/library/': 'api/v1/library/javerage.json',
            '/api/v1/notices/': 'api/v1/notices/index.json',
            '/api/v1/profile/': 'api/v1/profile/javerage.json',
            '/api/v1/oquarters/': 'api/v1/oquarters/2013,spring',
            '/api/v1/deptcal/': 'api/v1/deptcal/index.json',
            '/api/v1/visual_schedule/current': 'api/v1/schedule/visual.json',
            '/api/v1/schedule/current': 'api/v1/schedule/2013,spring',
            '/api/v1/instructor_schedule/2013,spring': 'api/v1/instructor_schedule/billsea-2013-spring'
        });
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });


    it('Desktop cards for applicants/students/instructors', function() {
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.deepEqual(desktop_body_cards,
                         [HuskyExperienceCard,
                          ThriveCard,
                          OutageCard,
                          GradeCard,
                          FutureQuarterCardA,
                          ThankYouCard,
                          ToRegisterCard,
                          RegStatusCard,
                          SummerEFSCard,
                          SummerRegStatusCardA,
                          CriticalInfoCard,
                          InternationalStuCard,
                          SummaryScheduleCard,
                          VisualScheduleCard,
                          TextbookCard,
                          FutureSummaryScheduleCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          SeattleApplicationCard,
                          BothellApplicationCard,
                          TacomaApplicationCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
    });

    it('Mobile cards for applicants/students/instructors', function() {
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [HuskyExperienceCard,
                          SeattleApplicationCard,
                          BothellApplicationCard,
                          TacomaApplicationCard,
                          QuickLinksCard,
                          ThriveCard,
                          OutageCard,
                          GradeCard,
                          FutureQuarterCardA,
                          ThankYouCard,
                          ToRegisterCard,
                          RegStatusCard,
                          SummerEFSCard,
                          SummerRegStatusCardA,
                          CriticalInfoCard,
                          InternationalStuCard,
                          SummaryScheduleCard,
                          FutureSummaryScheduleCard,
                          VisualScheduleCard,
                          TextbookCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Desktop for alumni should have', function() {
        window.innerWidth = 800;
        window.user.netid = "jalum";
        window.user.student = false;
        window.user.no_1st_class_affi = true,
        window.user.alumni = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, true);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="AlumniCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });

    it('Mobile for alumni should have', function() {
        window.innerWidth = 767;

        window.user.netid = "jalum";
        window.user.student = false;
        window.user.no_1st_class_affi = true,
        window.user.alumni = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, false);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="AlumniCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });

    it('Desktop for past student should have', function() {
        window.innerWidth = 800;

        window.user.netid = "javerage";
        window.user.student = false;
        window.user.no_1st_class_affi = true,
        window.user.past_stud = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, true);
        assert.equal($('div[id="TranscriptsCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });

    it('Mobile for past student should have', function() {
        window.innerWidth = 767;

        window.user.netid = "javerage";
        window.user.student = false;
        window.user.no_1st_class_affi = true,
        window.user.past_stud = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, false);
        assert.equal($('div[id="TranscriptsCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });

    it('Desktop for past employee should have', function() {
        window.innerWidth = 800;

        window.user.netid = "javerage";
        window.user.student = false;
        window.user.retiree = true;
        window.user.past_employee = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, true);
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="RetireAssoCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });

    it('Mobile for past employee should have', function() {
        window.innerWidth = 767;

        window.user.netid = "javerage";
        window.user.is_hxt_viewer = false;
        window.user.student = false;
        window.user.retiree = true;
        window.user.past_employee = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, false);
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="RetireAssoCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);
    });
});
