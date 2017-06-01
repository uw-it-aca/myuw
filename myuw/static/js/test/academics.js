var Global = require("./global.js");


describe("Academics page course cards", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/academics.js",
                "myuw/static/js/card/schedule/load_course_cards.js"
            ]
        });

        window.card_display_dates = {};
    });
    it("show if is student", function() {
        window.user.student = true;
        assert.equal(false, CourseCards.hide_card());
    });
    it("hide if not student", function() {
        window.user.student = false;
        assert.equal(true, CourseCards.hide_card());
    });
});
