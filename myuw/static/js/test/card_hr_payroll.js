var Global = require("./global.js");

describe('HRPayrollCard', function(){
    describe("Shows HR/Payroll card", function() {
        before(function () {
            var render_id = 'rendre_hr_payroll_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/accounts/hr_payroll_card.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/workday_link.html',
                    'myuw/templates/handlebars/card/accounts/hr_payroll_card.html'
                ]
            });

            HRPayrollCard.dom_target = $('#' + render_id);
        });
        beforeEach(function () {
            window.user.student = false;
            window.user.faculty = false;
            window.user.employee = false;
            window.user.stud_employee = false;
            window.user.past_employee = false;
            window.user.retiree = false;
            window.enabled_features = {};
            HRPayrollCard.dom_target.html('');
        });
        it("Should render for instructor", function() {
            window.user.employee = true;
            window.user.faculty = true;
            HRPayrollCard.render_init();
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://hr.uw.edu/"]').length, 0);
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://ap.washington.edu/ahr/"]').length, 1);
        });
        it("Should render for employee", function() {
            window.user.employee = true;
            HRPayrollCard.render_init();
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://hr.uw.edu/"]').length, 1);
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://ap.washington.edu/ahr/"]').length, 0);
        });
        it("Should render for student employee", function() {
            window.user.stud_employee = true;
            HRPayrollCard.render_init();
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://hr.uw.edu/"]').length, 1);
            assert.equal(HRPayrollCard.dom_target.find('a[href="https://isc.uw.edu/"]').length, 1);
        });
        it("Should render truncated view for past_employee", function() {
            window.user.past_employee = true;
            window.page = "home";

            HRPayrollCard.render_init();
            assert.equal(HRPayrollCard.dom_target.find('a[href="https://isc.uw.edu"]').length, 1);

            // not faculty
            assert.equal(HRPayrollCard.dom_target.find('a[href="http://ap.washington.edu/ahr/"]').length, 0);
            // truncated
            assert.equal(HRPayrollCard.dom_target.find('a[href="https://isc.uw.edu/your-time-absence/time-off/"]').length, 0);
            assert.equal(HRPayrollCard.dom_target.find('a[href="https://www.washington.edu/wholeu/"]').length, 0);
        });
    });
});
