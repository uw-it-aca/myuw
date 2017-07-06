var Global = require("./global.js");
var assert = require("assert");

describe('AccountSummaryCard', function() {

    describe("week counter info", function() {

        it('should count weeks properly', function() {
            Global.Environment.init({
                scripts: [
                    "myuw/static/js/card/summary/accounts.js"
                ],
            });

            d1 = new Date(2017, 4, 31);
            d2 = new Date(2017, 4, 30);

            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);

            // Testing some middle of week starts
            d1 = new Date(2013, 0, 9);
            for (var i = 9; i < 14; i++) {
                d2 = new Date(2013, 0, i);
                assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);
            }
            for (var i = 14; i < 21; i++) {
                d2 = new Date(2013, 0, i);
                assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);
            }

            d1 = new Date(2017, 4, 31);
            d2 = new Date(2017, 5, 12);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 3);

            d2 = new Date(2018, 4, 31);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 53);

            // Test starting on Monday
            d1 = new Date(2013, 0, 7);
            for (var i = 7; i < 14; i++) {
                d2 = new Date(2013, 0, i);
                assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);
            }

            d2 = new Date(2013, 0, 14);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);

            // Test a week ending on Monday
            d2 = new Date(2013, 0, 14);
            for (var i = 7; i < 14; i++) {
                d1 = new Date(2013, 0, i);
                assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);
            }
        });
    });

    describe("account summaries info", function() {

        before(function () {

            var render_id = 'account_summary_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                    "myuw/static/js/card/summary/accounts.js"
                ],
                templates: [
                    'myuw/templates/handlebars/card/summary/accounts.html'
                ]
            });

            window['term_data'] = {break_year:2017};
            console.log(window.term_data);

            AccountSummaryCard.dom_target = $('#' + render_id);

        });

        beforeEach(function () {
            // reset hfs and library to null
            WSData._hfs_data = null;
            WSData._library_data = null;
        });


        it("should NOT render", function() {
            // test if hfs and library are both null
            AccountSummaryCard.render_init();
            assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries').length, 0);
        });

        it("should render if only hfs", function() {
            // test if only hfs is true
            WSData._hfs_data = true;
            AccountSummaryCard.render_init();
            assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries').length, 1);
        });

        it("should render if only library", function() {
            // test if only library is true
            WSData._library_data = true;
            AccountSummaryCard.render_init();
            assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries').length, 1);
        });

        /**
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
        **/

    });

});
