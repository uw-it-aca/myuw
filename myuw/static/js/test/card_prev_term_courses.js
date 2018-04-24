var Global = require("./global.js");


describe("Home page course cards", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/landing.js",
                "myuw/static/js/card/schedule/prev_course_cards.js"
            ]
        });

        window.user = {};
    });
    it("show if is pce student", function() {
        window.user.pce = true;
        assert.equal(false, PrevTermCourseCards.hide_card());
    });
    it("hide if not pce student", function() {
        window.user.pce = false;
        assert.equal(true, PrevTermCourseCards.hide_card());
    });
});
