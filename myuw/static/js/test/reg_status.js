var Global = require("./global.js");

describe('RegStatusCard', function(){
    describe("reg status card", function() {
        before(function (done) {
            var render_id = 'RegStatusCard';

            WSData.clear_cache();

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/reg_status.js",
                    "myuw/static/js/card/error.js",
                    "myuw/static/js/notices.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/reg_status.html',
                    'myuw/templates/handlebars/card/error.html',
                    'myuw/templates/handlebars/card/registration/holds.html',
                    'myuw/templates/handlebars/card/registration/finaid_notices.html',
                    'myuw/templates/handlebars/card/registration/est_reg_date.html',
                    'myuw/templates/handlebars/card/registration/in_myplan.html',
                    'myuw/templates/handlebars/card/registration/reg_resources.html',
                    'myuw/templates/handlebars/card/registration/myplan_courses.html'
                ]
            });

            window.card_display_dates = {
                "system_date": '2013-04-15 00:01',
                "is_after_start_of_registration_display_period" : true,
                "is_before_end_of_registration_display_period": true
            };


            Global.Environment.ajax_stub({
                '/api/v1/oquarters/': 'api/v1/oquarters/2013,spring/javerage,2013-04-15-00-00-01,no-reg.json',
                '/api/v1/notices/': 'api/v1/notices/index.json',
                '/api/v1/profile/': 'api/v1/profile/javerage.json',
                '/api/v1/myplan/2013/Autumn': 'api/v1/myplan/2013/Autumn/javerage,2013-04-15-00-00-01.json',
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            RegStatusCard.dom_target = $('#' + render_id);
            RegStatusCard.render_init();

            $(window).on("myuw:card_load", function () {
                done();
            });
        });
        it("Should render reg status card", function() {
            assert.equal(RegStatusCard.dom_target.find('#RegStatusCard').attr('data-identifier'), 'Autumn2013');
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    })
});
