var Global = require("./global.js");

describe("OutageCard", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/card/outage.js",
            ],
            templates: [
                'myuw/templates/handlebars/card/outage.html'
            ]
        });
        window.card_display_dates = {};
        window.enabled_features = {};
    });
    it("not show OutageCard to none", function() {
        window.user.student = false;
        window.user.employee = false;
        window.user.instructor = false;
        assert.equal(true, OutageCard.hide_card());
    });
    it("may show OutageCard to student", function() {
        window.user.student = true;
        assert.equal(false, OutageCard.hide_card());
    });
    it("may show OutageCard to employee", function() {
        window.user.employee = true;
        assert.equal(false, OutageCard.hide_card());
    });
    it("may show OutageCard to instructor", function() {
        window.user.instructor = true;
        assert.equal(false, OutageCard.hide_card());
    });
});
