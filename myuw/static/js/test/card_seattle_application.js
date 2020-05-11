var Global = require("./global.js");

describe("Seattle Applicant card", function() {
    before(function (done) {
        var render_id = 'seattle_application';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/seattle_application.js"
            ],
            templates: [
                'myuw/templates/handlebars/card/seattle_application.html'
            ]
        });

        SeattleApplicationCard.dom_target = $('#' + render_id);
        done();
    });

    describe('Has application', function() {
        before(function (done) {
            Global.Environment.ajax_stub({
                '/api/v1/applications/': '/api/v1/applications/sea_2020_aut'
            });
            var has_loaded = false;
            $(window).on("myuw:card_load", function () {
                if(!has_loaded){
                    done();
                    has_loaded = true;
                }
            });
            window.user.applicant = true;
            SeattleApplicationCard.render_init();
        });
        it("render card", function() {
            assert.equal(SeattleApplicationCard.dom_target.find('h3').text().includes("Your Seattle Application for Autumn 2020"), true);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
            SeattleApplicationCard.dom_target.html("");
            WSData._applicant_data = null;
        });
    });

    describe("No Applicant data", function() {
        before(function (done) {
            Global.Environment.ajax_stub({
                '/api/v1/applications/': '/api/v1/applications/no_app'
            });
            window.user.applicant = true;
            SeattleApplicationCard.render_init();
            window.setTimeout(function(){
                done();
            }, 1000)
        });

        it("Should hide card", function() {
        console.log($('#seattle_application_card'));
            assert.equal(SeattleApplicationCard.dom_target.find('#seattle_application_card').length, 0);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
            SeattleApplicationCard.dom_target.html("");
            WSData._applicant_data = null;
        });
    });
});
