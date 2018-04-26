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
        var dom_target;

        before(function () {
            var render_id = 'render_account_summary_card';

            Global.Environment.init({
                render_id: render_id,
                scripts: [
                   "myuw/static/js/ws_data.js",
                   "myuw/static/js/myuw_log.js",
                   "myuw/static/js/card/summary/accounts.js"
                 ],
                templates: [
                    'myuw/templates/handlebars/card/summary/accounts.html'
                ]
            });

            window['term_data'] = {
                break_quarter: "spring",
                break_year: "2017",
                quarter: "spring",
                year: "2017",
                is_break: false,
                is_finals: false,
                last_day: new Date(2017, 6, 9),
                today: "Monday, April 5, 2017",
                today_date: new Date(2017, 4, 5)
            };

            dom_target = $('#' + render_id);
        });


        beforeEach(function (){
            Global.Environment.ajax_stub({
                '/api/v1/library/': 'api/v1/library/javerage.json',
                '/api/v1/hfs/': 'api/v1/hfs/javerage.json'
            });
            AccountSummaryCard.render_init(dom_target);
        });

        afterEach(function(){
            Global.Environment.ajax_stub_restore();
        });

        it("all", function() {
            // test if hfs and library are both rendered
            assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries > a').length, 4);
        });

        it("only hfs", function() {
            // test if only hfs is true
            var lib_data = WSData._library_data;
            WSData._library_data = {};
            $(window).one("myuw:card_load", function () {
                assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries > a').length, 3);
            });
            AccountSummaryCard.render_init(dom_target);
            WSData._library_data = lib_data;
        });

        it("only library", function() {
            // test if only library is true
            var hfs_data = WSData._hfs_data;
            WSData._hfs_data = {};
            $(window).one("myuw:card_load", function () {
                assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries > a').length, 1);
            });
            AccountSummaryCard.render_init(dom_target);
            WSData._hfs_data = hfs_data;
        });

        it("NO render", function() {
            WSData._library_data = {};
            WSData._hfs_data = {};
            // test if hfs and library are both rendered
            $(window).one("myuw:card_load", function () {
                assert.equal(AccountSummaryCard.dom_target.find('.myuw-account-summaries > a').length, 0);
            });
            AccountSummaryCard.render_init(dom_target);
        });
    });
});
