var Global = require("./global.js");

describe('UwnetidCard', function(){
    describe("UW NetID card", function() {
        before(function (done) {
            var render_id = 'render_acount_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/accounts/uwnetid.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/uwnetid.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/profile/': '/api/v1/profile/index.json',
            });

            var has_loaded = false;
            $(window).on("myuw:card_load", function () {
                if(!has_loaded){
                    done();
                    has_loaded = true;
                }
            });
            UwnetidCard.dom_target = $('#' + render_id);
            UwnetidCard.render_init();
        });

        it("Should render card", function() {
            assert.equal(UwnetidCard.dom_target.find('a').length, 3);
            assert.equal(UwnetidCard.dom_target.find('a')[0].href,
                         "https://uwnetid.washington.edu/manage/");
            assert.equal(UwnetidCard.dom_target.find('a')[1].href,
                         "https://uwnetid.washington.edu/manage/?password");
            assert.equal(UwnetidCard.dom_target.find('a')[2].href,
                         "https://identity.uw.edu/account/recovery/");
        });
        it("Render 2fa link for emp", function() {
            UwnetidCard.dom_target.html('');
            window.user.employee = true;
            UwnetidCard.render();
            assert.equal(UwnetidCard.dom_target.find('a').length, 4);
            assert.equal(UwnetidCard.dom_target.find('a')[3].href,
                         "https://identity.uw.edu/2fa/");
        });
        it("Render 2fa link for stud_emp", function() {
            UwnetidCard.dom_target.html('');
            window.user.employee = false;
            window.user.stud_employee = true;
            UwnetidCard.render();
            assert.equal(UwnetidCard.dom_target.find('a').length, 4);
            assert.equal(UwnetidCard.dom_target.find('a')[3].href,
                         "https://identity.uw.edu/2fa/");
        });

        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
