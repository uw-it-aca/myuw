var Future = require("../future.js");
var Card = require("../card/schedule/visual.js");
var jsdom = require('jsdom');
var Handlebars = require("../../vendor/js/handlebars-v2.0.0.js");

var doc = jsdom.jsdom('<html></html>'),
    window = doc.parentWindow;

var $ = require('jquery')(window);
var assert = require("assert");

describe("Always shows the visual schedule", function() {
    global.$ = $;
    global.window = window;
    global.Handlebars = Handlebars;
    global.VisualScheduleCard = Card.VisualScheduleCard;
    window.user = {};
    window.user.student = true;

    window.card_display_dates = {};

    it("by default it should be hidden", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        assert.equal(false, Card.VisualScheduleCard.should_display_card());
    });
    it("should show when force-shown", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        window.force_visual_schedule_display = true;
        assert.equal(true, Card.VisualScheduleCard.should_display_card());
    });
    it("should show when force-shown by method", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        window.force_visual_schedule_display = false;
        Card.VisualScheduleCard.force_visual_schedule_display();
        assert.equal(true, Card.VisualScheduleCard.should_display_card());
    });
});
