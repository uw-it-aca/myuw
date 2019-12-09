var Global = require("./global.js");

describe('TuitionCard', function(){
    describe("Tuition card", function() {
        before(function (done) {
            var render_id = 'render_tuition_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/notices.js",
                    "myuw/static/js/card/error.js",
                    "myuw/static/js/card/accounts/tuition.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/accounts/tuition_resources.html',
                    'myuw/templates/handlebars/card/accounts/tuition.html',
                    'myuw/templates/handlebars/card/error.html'
                ]
            });

            Global.Environment.ajax_stub({
                '/api/v1/finance/': '/api/v1/finance/javerage.json',
                '/api/v1/notices/': '/api/v1/notices/index.json',
            });

            var has_loaded = false;
            $(window).on("myuw:card_load", function () {
                if(!has_loaded){
                    done();
                    has_loaded = true;
                }
            });
            TuitionCard.dom_target = $('#' + render_id);
            window.user.student = true;
            window.user.pce = true;
            TuitionCard.render_init();
        });
        it("Should have regular and pce tuition balances for javerage", function() {
            assert.equal(TuitionCard.dom_target.find('h4').length, 4);
            assert.notEqual(TuitionCard.dom_target.find('h4')[0].innerHTML.indexOf('Student Fiscal Services'), -1);
            assert.notEqual(TuitionCard.dom_target.find('h4')[1].innerHTML.indexOf('PCE-Continuum College'), -1);
            assert.equal(TuitionCard.dom_target.find('h4')[2].innerHTML,
                         "Financial Aid");
            assert.equal(TuitionCard.dom_target.find('h4')[3].innerHTML,
                         "Related");
        });
        it('Detect a debit vs. a credit', function(){
            var data = TuitionCard.process_tuition("100.00")
            assert.equal(data.tuition, "100.00");
            assert.equal(data.is_credit, false);
            var data = TuitionCard.process_tuition("200.00 CR")
            assert.equal(data.tuition, "200.00");
            assert.equal(data.is_credit, true);

            assert.equal(Notices.get_notices_for_tag("pce_tuition_dup").length, 0);
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});
