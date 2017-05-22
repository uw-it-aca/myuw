var Global = require("./global.js");

describe('DirectoryInfoCard', function(){
    describe("directory info instructor card default", function() {
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
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
    describe("directory info instructor card", function() {
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

            Global.Environment.ajax_stub('api/v1/directory/index.json');

            $(window).on("myuw:card_load", function () {
                done();
            });

            window.enabled_features = { 'employee_profile': true };
            window.user.faculty = true;

            DirectoryInfoCard.dom_target = $('#' + render_id);
            DirectoryInfoCard.render_init();
        });
        it("Should render instructor card", function() {
            assert.equal(DirectoryInfoCard.dom_target.find('span[property="telephone"]').html(),
                         '(206) 555-1235');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
