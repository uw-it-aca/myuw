var Global = require("./global.js");


describe("Always shows the visual schedule", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "myuw/static/js/future.js",
                "myuw/static/js/card/schedule/visual.js"
            ]
        });

        window.card_display_dates = {};
    });
    it("should show ", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        assert.equal(true, VisualScheduleCard.should_display_card());
    });

});
