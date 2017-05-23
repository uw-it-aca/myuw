var Global = require("./global.js");

describe('MedicineAccountsCard', function(){
    describe("Render UW NetID card", function() {
        before(function (done) {
            var render_id = 'render_acount_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/web_services/ws_base.js",
                    "myuw/static/js/web_services/ws_profile_data.js",
                    "myuw/static/js/card/accounts/account_medicine.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/account_medicine.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/profile/': '/api/v1/profile/index.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            MedicineAccountsCard.dom_target = $('#' + render_id);
            MedicineAccountsCard.render_init();
        });
        it("Rendered", function() {
            assert.equal(MedicineAccountsCard.dom_target.find('span.pw-exp-date').length, 1);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
    describe("Do NOT render UW NetID card", function() {
        before(function (done) {
            var render_id = 'render_acount_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/web_services/ws_base.js",
                    "myuw/static/js/web_services/ws_profile_data.js",
                    "myuw/static/js/card/accounts/account_medicine.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/account_medicine.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/profile/': '/api/v1/profile/index-non-med.json'
            });

            $(window).on("myuw:card_load", function () {
                done();
            });

            // hidden card not rendered, so no event
            setTimeout(function () {
                done();
            }, 500);

            MedicineAccountsCard.dom_target = $('#' + render_id);
            MedicineAccountsCard.render_init();
        });
        it("NOT rendered", function() {
            assert.equal(MedicineAccountsCard.dom_target.find('span.pw-exp-date').length, 0);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
