var Global = require("./global.js");

describe("ThriveCard", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/card/thrive.js",
            ],
            templates: [
                'myuw/templates/handlebars/card/thrive.html'
            ]
        });
        window.card_display_dates = {};
        window.enabled_features = {};
    });
    it("not show", function() {
        window.user.fyp = false;
        window.user.aut_transfer = false;
        window.user.win_transfer = false;
        assert.equal(true, ThriveCard.hide_card());
    });
    it("may show fyp student", function() {
        window.user.fyp = true;
        assert.equal(false, ThriveCard.hide_card());
    });
    it("may show to autumn transfer", function() {
        window.user.aut_transfer = true;
        assert.equal(false, ThriveCard.hide_card());
    });
    it("may show to winter transfer", function() {
        window.user.win_transfer = true;
        assert.equal(false, ThriveCard.hide_card());
    });
});
