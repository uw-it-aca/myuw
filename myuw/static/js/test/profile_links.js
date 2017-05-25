var Global = require("./global.js");

describe('ProfileHelpLinksCard', function(){
    describe("Profile help links card", function() {
        before(function () {
            var render_id = 'render_links_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/help_links.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/profile/help_links_card.html'
                ]
            });

            ProfileHelpLinksCard.dom_target = $('#' + render_id);
        });
        it("render student links", function() {
            window.user.student = true;
            window.user.employee = false;
            window.user.stud_employee = false;

            ProfileHelpLinksCard.render_init();
            assert.equal(ProfileHelpLinksCard.dom_target.find('#student_legal_name').length, 1);
            assert.equal(ProfileHelpLinksCard.dom_target.find('#employee_workday_info').length, 0);
        });
        it("render employee links", function() {
            window.user.student = false;
            window.user.employee = true;
            window.user.stud_employee = false;

            ProfileHelpLinksCard.render_init();
            assert.equal(ProfileHelpLinksCard.dom_target.find('#student_legal_name').length, 0);
            assert.equal(ProfileHelpLinksCard.dom_target.find('#employee_workday_info').length, 1);
        });
        it("render student/employee links", function() {
            window.user.student = false;
            window.user.employee = false
            window.user.stud_employee = true;

            ProfileHelpLinksCard.render_init();
            assert.equal(ProfileHelpLinksCard.dom_target.find('#student_legal_name').length, 1);
            assert.equal(ProfileHelpLinksCard.dom_target.find('#employee_workday_info').length, 1);
        });
    });
});
