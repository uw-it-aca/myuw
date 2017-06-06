var Global = require("./global.js");
var assert = require("assert");

describe('AccountSummaryCard', function() {
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
