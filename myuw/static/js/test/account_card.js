var Global = require("./global.js");

describe('AccountsCard', function(){
    describe("UW NetID card", function() {
        before(function (done) {
            var render_id = 'render_acount_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/accounts/account_card.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/account_card.html'
                ]
            });

            Global.Environment.ajax_stub('/api/v1/profile/index.json');

            $(window).on("myuw:card_load", function () {
                done();
            });

            AccountsCard.dom_target = $('#' + render_id);
            AccountsCard.render_init();
        });
        it("Should render card", function() {
            assert.equal(AccountsCard.dom_target.find('span.pw-exp-date').length, 1);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
