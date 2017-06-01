var Global = require("./global.js");
var assert = require("assert");

describe('AccountSummaryCard', function() {
    it('should count weeks properly', function() {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/card/summary/accounts.js"
            ],
        });

        // Testing some middle of week starts
        d1 = new Date(2017, 4, 31);
        d2 = new Date(2017, 4, 30);

        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 0);

        d2 = new Date(2017, 4, 31);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);

        d2 = new Date(2017, 5, 4);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);

        d2 = new Date(2017, 5, 5);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);

        d2 = new Date(2017, 5, 11);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);

        d2 = new Date(2017, 5, 12);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 3);

        d2 = new Date(2018, 4, 31);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 53);

        // Test starting on Monday
        console.log("---------------------------------------");
        d1 = new Date(2013, 0, 7);
        d2 = new Date(2013, 0, 7);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);

        d2 = new Date(2013, 0, 8);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 1);
        d2 = new Date(2013, 0, 14);
        assert.equal(AccountSummaryCard.get_weeks_apart(d1, d2), 2);
    });
});

