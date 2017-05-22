var Global = require("./global.js");

describe('MedicineAccountsCard', function(){
    describe("UW NetID card", function() {
        before(function (done) {
            var render_id = 'render_acount_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/accounts/account_medicine.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/account_medicine.html'
                ]
            });

            Global.Environment.ajax_stub('/api/v1/profile/index.json');

            $(window).on("myuw:card_load", function () {
                done();
            });

            MedicineAccountsCard.dom_target = $('#' + render_id);
            MedicineAccountsCard.render_init();
        });
        it("Should render card", function() {
            assert.equal(MedicineAccountsCard.dom_target.find('span.pw-exp-date').length, 1);
        });
        it("Should NOT render card", function() {
            var profile = WSData.profile_data();
            profile.password.has_active_med_pw = false;
            MedicineAccountsCard.dom_target.html('');
            MedicineAccountsCard.render_upon_data();
            assert.equal(MedicineAccountsCard.dom_target.find('span.pw-exp-date').length, 0);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
