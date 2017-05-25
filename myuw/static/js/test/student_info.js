var Global = require("./global.js");

describe('StudentInfoCard', function(){
    describe("student profile card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/student_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/student_info.html'
                ]
            });

            WSData._profile_data = null;
            Global.Environment.ajax_stub({
                '/api/v1/profile/': 'api/v1/profile/index-jbothell.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            StudentInfoCard.dom_target = $('#' + render_id);
            StudentInfoCard.render_init();
        });
        it("Should render student only card", function() {
            assert.equal(StudentInfoCard.dom_target.find('div.profile-student-info span').text(), '1233334');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
    describe("student/employee profile card", function() {
        before(function (done) {
            var render_id = 'dir_info';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/profile/student_info.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/student_info.html'
                ]
            });

            WSData._profile_data = null;
            Global.Environment.ajax_stub({
                '/api/v1/profile/': 'api/v1/profile/index-javerage.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            StudentInfoCard.dom_target = $('#' + render_id);
            StudentInfoCard.render_init();
        });
        it("Should render student only card", function() {
            assert.equal(StudentInfoCard.dom_target.find('div.profile-student-info span').text(), '1033334');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
