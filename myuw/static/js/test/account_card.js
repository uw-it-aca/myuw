var Global = require("./global.js");

describe('AccountsCard', function(){
    describe("Shows HR/Payroll card", function() {
        before(function () {
            var render_id = 'hr_payroll_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/accounts/account_card.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/account_card.html'
                ]
            });

            AccountsCard.dom_target = $('#' + render_id);
        });
        it("Should render instructor card", function() {
            window.user.faculty = true;
            AccountsCard.render_init();
            assert.equal($('a[href="http://ap.washington.edu/ahr/"]').length, 1);
        });
    });
});
