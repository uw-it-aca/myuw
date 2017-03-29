var Global = require("./global.js");


describe("Always shows the visual schedule", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "../future.js",
                "../card/schedule/visual.js"
            ]
        });

        window.card_display_dates = {};
    });
    it("by default it should be hidden", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        assert.equal(false, VisualScheduleCard.should_display_card());
    });
    it("should show when force-shown", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        window.force_visual_schedule_display = true;
        assert.equal(true, VisualScheduleCard.should_display_card());
    });
    it("should show when force-shown by method", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        window.force_visual_schedule_display = false;
        VisualScheduleCard.force_visual_schedule_display();
        assert.equal(true, VisualScheduleCard.should_display_card());
    });
});
