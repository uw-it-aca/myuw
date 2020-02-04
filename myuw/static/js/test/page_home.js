var Global = require("./global.js");

describe("HomePage", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/landing.js",
                "myuw/static/js/banner/notice.js",
                "myuw/static/js/textbooks.js",
                "myuw/static/js/notices.js",
                "myuw/static/js/resources.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/resources.js",
                "myuw/static/js/card/resources_explore.js",
                "myuw/static/js/card/alumni.js",
                "myuw/static/js/card/calendars/acad_cal_sp.js",
                "myuw/static/js/card/calendars/events.js",
                "myuw/static/js/card/international_student.js",
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
        window.user.student = false;
        window.user.registered_stud = false;
        window.user.instructor = false;
        window.user.applicant = false;
        window.user.is_hxt_viewer = false;
        window.user.intl_stud = false;
        window.user.fyp = false;
        window.user.aut_transfer = false;
        window.user.win_transfer = false;
        window.user.employee = false;
        window.user.retiree = false;
        window.innerWidth = 767;
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


    it('Desktop cards for students', function() {
        window.innerWidth = 800;
        window.user.netid = "eight";
        window.user.student = true;
        window.user.registered_stud = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.deepEqual(desktop_body_cards,
                         [OutageCard,
                          GradeCard,
                          FutureQuarterCardA,
                          ThankYouCard,
                          ToRegisterCard,
                          RegStatusCard,
                          SummerEFSCard,
                          SummerRegStatusCardA,
                          CriticalInfoCard,
                          InternationalStuCard,
                          VisualScheduleCard,
                          TextbookCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          ResourcesCard,
                          ResourcesExploreCard]);
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
    });

    it('Desktop cards for instructor', function() {
        window.innerWidth = 800;
        window.user.netid = "billpce";
        window.user.instructor = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 6);
        assert.equal(desktop_body_cards[0].name, 'OutageCard');
        assert.equal(desktop_body_cards[1].name, 'SummaryScheduleCard');
        assert.equal(desktop_body_cards[2].name, 'VisualScheduleCard');
        assert.equal(desktop_body_cards[3].name, 'FutureSummaryScheduleCard');
        assert.equal(desktop_body_cards[4].name, 'ResourcesCard');
        assert.equal(desktop_body_cards[5].name, 'ResourcesExploreCard');
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
    });

    it('Desktop cards for applicants', function() {
        window.innerWidth = 800;
        window.user.netid = "japplicant";
        window.user.applicant = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 5);
        assert.equal(desktop_body_cards[0].name, 'SeattleApplicationCard');
        assert.equal(desktop_body_cards[1].name, 'BothellApplicationCard');
        assert.equal(desktop_body_cards[2].name, 'TacomaApplicationCard');
        assert.equal(desktop_body_cards[3].name, 'ResourcesCard');
        assert.equal(desktop_body_cards[4].name, 'ResourcesExploreCard');
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
        window.user.registered_stud = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 3);
    });

    it('Desktop cards for hxt_viewer', function() {
        window.innerWidth = 800;
        window.user.netid = "javerage";
        window.user.is_hxt_viewer = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 3);
        assert.equal(desktop_body_cards[0].name, 'HuskyExperienceCard');
        assert.equal(desktop_body_cards[1].name, 'ResourcesCard');
        assert.equal(desktop_body_cards[2].name, 'ResourcesExploreCard');
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
    });

    it('Desktop cards for fyp', function() {
        window.innerWidth = 800;
        window.user.netid = "jnew";
        window.user.fyp = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 3);
        assert.equal(desktop_body_cards[0].name, 'ThriveCard');
        assert.equal(desktop_body_cards[1].name, 'ResourcesCard');
        assert.equal(desktop_body_cards[2].name, 'ResourcesExploreCard');
        var desktop_sidebar_cards = Landing._get_desktop_sidebar_cards();
        assert.deepEqual(desktop_sidebar_cards,
                         [QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard]);
    });

    it('Desktop cards for aut_transfer', function() {
        window.innerWidth = 800;
        window.user.netid = "jnew";
        window.user.aut_transfer = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 3);
        assert.equal(desktop_body_cards[0].name, 'ThriveCard');
    });

    it('Desktop cards for win_transfer', function() {
        window.innerWidth = 800;
        window.user.netid = "jnew";
        window.user.win_transfer = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.equal(desktop_body_cards.length, 3);
        assert.equal(desktop_body_cards[0].name, 'ThriveCard');
    });

    it('Desktop for international student should have', function() {
        window.innerWidth = 800;
        window.user.netid = "jinter";
        window.user.student = true;
        window.user.registered_stud = true;
        window.user.intl_stud = true;
        var desktop_body_cards = Landing._get_desktop_body_cards();
        assert.deepEqual(desktop_body_cards,
                         [OutageCard,
                          GradeCard,
                          FutureQuarterCardA,
                          ThankYouCard,
                          ToRegisterCard,
                          RegStatusCard,
                          SummerEFSCard,
                          SummerRegStatusCardA,
                          CriticalInfoCard,
                          InternationalStuCard,
                          VisualScheduleCard,
                          TextbookCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          IntlStudCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Mobile cards for applicants', function() {
        window.user.netid = "japplicant";
        window.user.applicant = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [SeattleApplicationCard,
                          BothellApplicationCard,
                          TacomaApplicationCard,
                          QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);

        window.user.registered_stud = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.equal(mobile_cards.length, 6);
    });

    it('Mobile cards for instructor', function() {
        window.user.netid = "billpce";
        window.user.instructor = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [QuickLinksCard,
                          OutageCard,
                          SummaryScheduleCard,
                          FutureSummaryScheduleCard,
                          VisualScheduleCard,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Mobile cards for students', function() {
        window.user.netid = "eight";
        window.user.student = true;
        window.user.registered_stud = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [QuickLinksCard,
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
                          VisualScheduleCard,
                          TextbookCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Mobile cards for fyp', function() {
        window.user.netid = "jnew";
        window.user.fyp = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [QuickLinksCard,
                          ThriveCard,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Mobile cards for hxt_viewer', function() {
        window.user.netid = "jnew";
        window.user.is_hxt_viewer = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [HuskyExperienceCard,
                          QuickLinksCard,
                          AcadCalSnippet,
                          EventsCard,
                          ResourcesCard,
                          ResourcesExploreCard]);
    });

    it('Mobile for international student', function() {
        window.user.netid = "jinter";
        window.user.student = true;
        window.user.registered_stud = true;
        window.user.intl_stud = true;
        var mobile_cards = Landing._get_mobile_cards();
        assert.deepEqual(mobile_cards,
                         [QuickLinksCard,
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
                          VisualScheduleCard,
                          TextbookCard,
                          FutureQuarterCard1,
                          SummerRegStatusCard1,
                          AcadCalSnippet,
                          EventsCard,
                          IntlStudCard,
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
        window.user.past_employee = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, true);
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);

        window.user.past_employee = false;
        window.user.retiree = true;
        Landing.make_html();
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="RetireAssoCard"]').length, 1);
    });

    it('Mobile for past employee should have', function() {
        window.innerWidth = 767;

        window.user.netid = "retiree";
        window.user.is_hxt_viewer = false;
        window.user.student = false;
        window.user.past_employee = true;

        Landing.make_html();
        assert.equal(Landing.is_desktop, false);
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="ContinuingEducationCard"]').length, 1);
        assert.equal($('div[id="UwnetidCard"]').length, 1);
        assert.equal($('div[id="QuickLinksCard"]').length, 1);
        assert.equal($('div[id="AcadCalSnippet"]').length, 1);
        assert.equal($('div[id="EventsCard"]').length, 1);

        window.user.retiree = true;
        window.user.past_employee = false;
        Landing.make_html();
        assert.equal($('div[id="HRPayrollCard"]').length, 1);
        assert.equal($('div[id="RetireAssoCard"]').length, 1);
    });

    it('Test resizing', function() {
        window.innerWidth = 1200;
        Landing.make_html();
        assert.equal(Landing.is_desktop, true);

        window.innerWidth = 700;
        $(window).trigger('resize');
        assert.equal(Landing.is_desktop, false);
    });

});
