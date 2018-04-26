var Global = require("./global.js");

describe("ProfilePage for student and employee", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/profile.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/card/profile/profile.js",
                "myuw/static/js/card/profile/employee_profile.js",
                "myuw/static/js/card/profile/student_info.js",
                "myuw/static/js/card/profile/help_links.js",
                "myuw/static/js/card/profile/applicant_profile.js",
            ],
            templates: [
                'myuw/templates/profile.html',
                'myuw/templates/handlebars/profile.html',
            ]
        });
        
    });

    beforeEach(function (){
        window.page = "profile";
        window.user.employee = true;
        window.user.student = true;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
        Global.Environment.ajax_stub({
            '/api/v1/profile/': 'api/v1/profile/seagrad.json',
            '/api/v1/directory/': 'api/v1/directory/seagrad.json'
            }
        );
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it('Desktop profile page for seagrad (stud, staff)', function() {
        window.innerWidth = 800;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, true);

        assert.equal($('div[id="profile_content_cards"]').length, 1);
        assert.equal($('div[id="profile_content_cards"]').contents().length, 4);
        // CommonProfileCard
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("id"), "CommonProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("style"), null);

        // EmployeeInfoCard
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("id"), "EmployeeInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("style"), null);

        // StudentInfoCard
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("id"), "StudentInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("style"), null);

        // ApplicantProfileCard hidden
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("id"), "ApplicantProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("style"), "display: none;");

        assert.equal($('div[id="profile_sidebar_cards"]').length, 1);
        assert.equal($('div[id="profile_sidebar_cards"]').contents().length, 1);
        // HelpLinksCard
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("id"), "HelpLinksCard");
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("style"), null);
    });

    it('Mobile profile page for seagrad', function() {
        window.innerWidth = 767;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, false);
        assert.equal($('div[id="CommonProfileCard"]').length, 1);
        assert.equal($('div[id="EmployeeInfoCard"]').length, 1);
        assert.equal($('div[id="StudentInfoCard"]').length, 1);
        assert.equal($('div[id="HelpLinksCard"]').length, 0);
    });
});

describe("ProfilePage for applicant and employee", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/profile.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/card/profile/profile.js",
                "myuw/static/js/card/profile/employee_profile.js",
                "myuw/static/js/card/profile/student_info.js",
                "myuw/static/js/card/profile/help_links.js",
                "myuw/static/js/card/profile/applicant_profile.js",
            ],
            templates: [
                'myuw/templates/profile.html',
                'myuw/templates/handlebars/profile.html',
            ]
        });
    });

    beforeEach(function (){
        window.page = "profile";
        window.user.employee = true;
        window.user.applicant = true;
        window.user.student = false;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
        Global.Environment.ajax_stub({
            '/api/v1/profile/': 'api/v1/profile/japplicant.json',
            '/api/v1/directory/': 'api/v1/directory/japplicant.json'
            }
        );
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it('Desktop profile page for japplicant (japplicant, staff)', function() {
        window.innerWidth = 800;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, true);
        assert.equal($('div[id="profile_content_cards"]').length, 1);
        assert.equal($('div[id="profile_content_cards"]').contents().length, 4);
        // CommonProfileCard
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("id"), "CommonProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("style"), null);

        // EmployeeInfoCard
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("id"), "EmployeeInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("style"), null);

        // StudentInfoCard hidden
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("id"), "StudentInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("style"), 'display: none;');

        // ApplicantProfileCard show
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("id"), "ApplicantProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("style"), null);

        assert.equal($('div[id="profile_sidebar_cards"]').length, 1);
        assert.equal($('div[id="profile_sidebar_cards"]').contents().length, 1); 
        // HelpLinksCard show
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("id"), "HelpLinksCard");
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("style"), null);
    });

    it('Mobile profile page for japplicant', function() {
        window.innerWidth = 767;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, false);
        assert.equal($('div[id="CommonProfileCard"]').length, 1);
        assert.equal($('div[id="EmployeeInfoCard"]').length, 1);
        assert.equal($('div[id="ApplicantProfileCard"]').length, 1);
        assert.equal($('div[id="HelpLinksCard"]').length, 0);
    });
});

describe("ProfilePage for student and student employee", function() {
    before(function () {

        Global.Environment.init({
            scripts: [
                "myuw/static/js/profile.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/cards.js",
                "myuw/static/js/card/loading.js",
                "myuw/static/js/page/profile.js",
                "myuw/static/js/card/profile/profile.js",
                "myuw/static/js/card/profile/employee_profile.js",
                "myuw/static/js/card/profile/student_info.js",
                "myuw/static/js/card/profile/help_links.js",
                "myuw/static/js/card/profile/applicant_profile.js",
            ],
            templates: [
                'myuw/templates/profile.html',
                'myuw/templates/handlebars/profile.html',
            ]
        });
        
    });

    beforeEach(function (){
        window.page = "profile";
        window.user.stud_employee = true;
        window.user.student = true;
        window.user.applicant = false;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
        Global.Environment.ajax_stub({
            '/api/v1/profile/': 'api/v1/profile/javerage.json',
            '/api/v1/directory/': 'api/v1/directory/javerage.json'
            }
        );
    });

    afterEach(function(){
        Global.Environment.ajax_stub_restore();
    });

    it('Desktop profile page for javerage (stud, stud_employee)', function() {
        window.innerWidth = 800;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, true);
        assert.equal($('div[id="profile_content_cards"]').length, 1);
        assert.equal($('div[id="profile_content_cards"]').contents().length, 4);
        // CommonProfileCard
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("id"), "CommonProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[0].getAttribute("style"), null);

        // EmployeeInfoCard
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("id"), "EmployeeInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[1].getAttribute("style"), null);

        // StudentInfoCard show
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("id"), "StudentInfoCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[2].getAttribute("style"), null);

        // ApplicantProfileCard hidden
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("id"), "ApplicantProfileCard");
        assert.equal($('div[id="profile_content_cards"]').contents()[3].getAttribute("style"), 'display: none;');

        assert.equal($('div[id="profile_sidebar_cards"]').length, 1);
        assert.equal($('div[id="profile_sidebar_cards"]').contents().length, 1); 
        // HelpLinksCard show
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("id"), "HelpLinksCard");
        assert.equal($('div[id="profile_sidebar_cards"]').contents()[0].getAttribute("style"), null);
    });

    it('Mobile profile page for javerage', function() {
        window.innerWidth = 767;
        ProfilePage.make_html();
        assert.equal(ProfilePage.is_desktop, false);
        assert.equal($('div[id="CommonProfileCard"]').length, 1);
        assert.equal($('div[id="EmployeeInfoCard"]').length, 1);
        assert.equal($('div[id="StudentInfoCard"]').length, 1);
        assert.equal($('div[id="HelpLinksCard"]').length, 0);
    });
});
