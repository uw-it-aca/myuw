var Global = require("./global.js");

describe('DirectoryInfoCard', function(){
    describe("instructor/employee profile card default", function() {
        before(function () {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/directory_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/directory_info.html'
                ]
            });

            window.enabled_features = { 'employee_profile': false };
            window.user.faculty = false;
            window.user.employee = false;
            window.user.stud_employee = false;

            DirectoryInfoCard.dom_target = $('#' + render_id);
            DirectoryInfoCard.render_init();
        });
        it("Should NOT render instructor card", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('span[property="telephone"]').length, 0);
        });
    });
    describe("instructor/employee profile card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/directory_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/directory_info.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/directory/': 'api/v1/directory/index-bill.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.enabled_features = { 'employee_profile': true };
            window.user.faculty = true;

            DirectoryInfoCard.dom_target = $('#' + render_id);
            DirectoryInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('span[property="telephone"]').first().html(),
                         '(206) 555-1235');
        });
        it("UW Seattle instructor", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('div.card-related-messages a').attr('href'),
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
                    "myuw/static/js/card/profile/directory_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/directory_info.html'
                ]
            });

            WSData._directory_data = null;
            Global.Environment.ajax_stub({
                '/api/v1/directory/': 'api/v1/directory/index-billtac.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.enabled_features = { 'employee_profile': true };
            window.user.faculty = true;
            window.user.tacoma = true;

            DirectoryInfoCard.dom_target = $('#' + render_id);
            DirectoryInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('span[property="telephone"]').first().html(),
                         '(253) 867-5309');
        });
        it("UW Tacoma instructor", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('div.card-related-messages a').attr('href'),
                         'http://directory.tacoma.uw.edu/');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
