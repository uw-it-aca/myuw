var Global = require("./global.js");

describe('RegStatusCard', function(){
    describe("reg status card", function() {
        before(function (done) {
            var render_id = 'RegStatusCard';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/reg_status.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/reg_status.html',
                    'myuw/templates/handlebars/card/registration/reg_holds.html',
                    'myuw/templates/handlebars/card/registration/reg_finaid_notices.html',
                    'myuw/templates/handlebars/card/registration/notice_est_reg_date.html',
                    'myuw/templates/handlebars/card/registration/in_myplan.html',
                    'myuw/templates/handlebars/card/registration/reg_resources.html',
                    'myuw/templates/handlebars/card/registration/myplan_courses.html'
                ]
            });


            Global.Environment.ajax_stub({
                '/api/v1/oquarters/': 'api/v1/oquarter/2013,spring',
                '/api/v1/notices/': 'api/v1/notices/index.json',
                '/api/v1/profile/': 'javerage.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            RegStatusCard.dom_target = $('#' + render_id);
            RegStatusCard.render_init();
        });
        it("Should render reg status card", function() {
            assert.equal(RegStatusCard.dom_target.find('#RegStatusCard').attr('data-identifier'), 'Autumn2013');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    })
});
