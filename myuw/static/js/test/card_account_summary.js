var Global = require("./global.js");

describe('AccountSummaryCard.get_weeks_apart', function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/card/summary/accounts.js"
            ]
        });
    });

    it('should count weeks properly', function() {
        // The week starts on Sundays
        // Winter quarter starts on Tuesday
        var d1 = new Date(2017, 0, 3);
        for (var i = 25; i <= 31; i++) {
            var d2 = new Date(2016, 11, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);
        }

        for (var i = 1; i <= 7; i++) {
            d2 = new Date(2017, 0, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);
        }

        for (var i = 8; i <= 14; i++) {
            d2 = new Date(2017, 0, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);
        }

        for (var i = 12; i <= 18; i++) {
            d2 = new Date(2017, 2, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 11);
        }

        d2 = new Date(2017, 2, 21);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 12);

        // Spring quarter starts on Monday
        d1 = new Date(2017, 2, 27);
        d2 = new Date(2017, 2, 22);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);

        d2 = new Date(2017, 2, 26);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);

        d1 = new Date(2017, 2, 27);
        d2 = new Date(2017, 3, 1);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);

        // Aut quarter starts on Wedesnday
        d1 = new Date(2017, 8, 27);
        d2 = new Date(2017, 8, 23);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);

        for (var i = 24; i <= 30; i++) {
            d2 = new Date(2017, 8, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);
        }
        for (var i = 10; i <= 23; i++) {
            d2 = new Date(2017, 8, i);
            assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);
        }
    });
});

describe('AccountSummaryCard', function() {
    var dom_target;
    before(function () {
        var render_id = 'render_acount_summery_card';

        Global.Environment.init({
            render_id: render_id,
            scripts: [
                "myuw/static/js/card/summary/accounts.js",
                "myuw/static/js/ws_data.js",
                "myuw/static/js/myuw_log.js",
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
            first_day: new Date(2017, 0, 3),
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
        console.log(AccountSummaryCard.dom_target.find('.myuw-week-counter').length);
        console.log(AccountSummaryCard.dom_target.find('.myuw-account-summaries').length);
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
