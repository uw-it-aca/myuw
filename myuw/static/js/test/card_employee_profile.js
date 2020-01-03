var Global = require("./global.js");

describe('EmployeeInfoCard', function(){
    describe("instructor/employee profile card default", function() {
        before(function () {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/employee_profile.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/workday_link.html',
                    'myuw/templates/handlebars/card/profile/employee_profile.html'
                ]
            });

            EmployeeInfoCard.dom_target = $('#' + render_id);

        });
        it("Should NOT render instructor card", function() {
            window.user.employee = false;
            assert.equal(true, EmployeeInfoCard.hide_card());
        });
    });
    describe("instructor/employee profile card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    'myuw/static/js/card/profile/employee_profile.js'
                ],
                templates: [
                    'myuw/templates/handlebars/card/workday_link.html',
                    'myuw/templates/handlebars/card/profile/employee_profile.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/directory/': 'api/v1/directory/bill.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.user.employee = true;
            EmployeeInfoCard.dom_target = $('#' + render_id);
            EmployeeInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal(EmployeeInfoCard.dom_target.find('span[property="telephone"]').first().html(),
                         '(206) 333-3333');
        });
        it("UW Seattle instructor", function() {
            assert.equal(EmployeeInfoCard.dom_target.find('.card-related-messages a').attr('href'),
                         'https://www.washington.edu/home/peopledir/');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
    describe("instructor/employee profile card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/employee_profile.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/workday_link.html',
                    'myuw/templates/handlebars/card/profile/employee_profile.html'
                ]
            });

            WSData._directory_data = null;
            Global.Environment.ajax_stub({
                '/api/v1/directory/': 'api/v1/directory/billtac.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.user.employee = true;
            window.user.tacoma = true;

            EmployeeInfoCard.dom_target = $('#' + render_id);
            EmployeeInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal(EmployeeInfoCard.dom_target.find('span[property="telephone"]').first().html(),
                         '(253) 867-5309');
        });
        it("UW Tacoma instructor", function() {
            assert.equal(EmployeeInfoCard.dom_target.find('.card-related-messages a').attr('href'),
                         'http://directory.tacoma.uw.edu/');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
