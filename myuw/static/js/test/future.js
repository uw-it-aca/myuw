var Future = require("../future.js");
var Card = require("../card/schedule/visual.js");
var jsdom = require('jsdom');
var Handlebars = require("../../vendor/js/handlebars-v2.0.0.js");

var doc = jsdom.jsdom('<html><head></head><body><script type="text/x-handlebars-template" id="future"><div class="container future-quarter-container"></div></script></body></html>'),
    window = doc.parentWindow;

var $ = require('jquery')(window);


var assert = require("assert");

describe("Always shows the visual schedule", function() {
    global.$ = $;
    global.window = window;
    global.Handlebars = Handlebars;
    global.VisualScheduleCard = Card.VisualScheduleCard;
    // Just mocked out - otherwise it calls WSData
    global.NoticeBanner = { render_init: function() { } };
    global.CourseCards = {};
    global.TextbookCard = {};
    global.Cards = { load_cards_in_order: function() { } };
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

    it("should be set after the future quarter page renders", function() {
        window.card_display_dates.is_before_last_day_of_classes = false;
        window.force_visual_schedule_display = false;
        Future.FutureQuarter.make_html();
        assert.equal(true, Card.VisualScheduleCard.should_display_card());
    });

});
