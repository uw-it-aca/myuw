var Global = require("./global.js");

describe("ProfilePage", function() {
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
        Global.Environment.ajax_stub({
            '/api/v1/profile/': 'api/v1/profile/seagrad.json',
            '/api/v1/directory/': 'api/v1/directory/seagrad.json'
            }
        );
        
    });

    beforeEach(function (){
        window.page = "profile";
        window.user.employee = true;
        window.user.student = true;
        window.user.seattle = true;
        window.card_display_dates = { system_date: '2013-04-15 00:01' };
    });

    describe('load profile page for seagrad (stud, staff)', function() {
        it('Desktop should have cards', function() {
            window.innerWidth = 800;
            ProfilePage.make_html();
            assert.equal(ProfilePage.is_desktop, true);
            assert.equal($('div[id="CommonProfileCard"]').length, 1);
            assert.equal($('div[id="EmployeeInfoCard"]').length, 1);
            assert.equal($('div[id="StudentInfoCard"]').length, 1);
            assert.equal($('div[id="HelpLinksCard"]').length, 1);
        });

        it('Mobile should have cards', function() {
            window.innerWidth = 767;
            ProfilePage.make_html();
            assert.equal(ProfilePage.is_desktop, false);
            assert.equal($('div[id="CommonProfileCard"]').length, 1);
            assert.equal($('div[id="EmployeeInfoCard"]').length, 1);
            assert.equal($('div[id="StudentInfoCard"]').length, 1);
            assert.equal($('div[id="HelpLinksCard"]').length, 0);
        });

    });
});

