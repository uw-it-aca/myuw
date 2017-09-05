var Global = require("./global.js");


describe("Future Quarter", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/future.js",
                "myuw/static/js/card/textbook.js",
                "myuw/static/js/card/schedule/load_course_cards.js",
                "myuw/static/js/card/schedule/visual.js"
            ]
        });
        window.card_display_dates = {};
    });
    it("should show VisualScheduleCard to student", function() {
        window.enabled_features = {};
        window.user.student = true;
        assert.equal(false, VisualScheduleCard.hide_card());
    });
    it("should show CourseCards to student", function() {
        window.enabled_features = {};
        window.user.student = true;
        assert.equal(false, CourseCards.hide_card());
    });
    it("should show TextbookCard to student", function() {
        window.enabled_features = {};
        window.user.student = true;
        assert.equal(false, TextbookCard.hide_card());
    });
});
