
var log = require("../myuw_log.js");
var LogUtils = log.LogUtils;
var MyuwLog = log.MyuwLog;
var jsdom = require('jsdom');

var doc = jsdom.jsdom("<html></html>"),
    window = doc.parentWindow;

var $ = require('jquery')(window);

var assert = require("assert");

describe("Logging", function() {
    describe("Viewport Test", function() {
        it('should say an element fully on-screen is in the viewport', function() {
            assert.equal(LogUtils.isInViewport(0, 50, 10, 20), true);
        });

        it('should say an element above, but 80% on is on-screen', function() {
            assert.equal(LogUtils.isInViewport(100, 1000, 80, 180), true);
        });

        it('should say an element below, but 80% on is on-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 1000, 920, 1020), true);
        });

        it('should say an element mostly below-screen, but taking 80% of the screen, is on-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 100, 20, 1000000), true);
        });

        it('should say an element mostly below-screen, but taking 50% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 100, 50, 1000000), false);
        });

        it('should say an element mostly above-screen, but taking 80% of the screen, is on-screen', function() {
            assert.equal(LogUtils.isInViewport(10000, 10100, 0, 10080), true);
        });

        it('should say an element mostly above-screen, but taking 50% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isInViewport(10000, 10100, 0, 10050), false);
        });

        it('should say an element completely above the viewport is off-screen', function() {
            assert.equal(LogUtils.isInViewport(10000, 10100, 0, 100), false);
        });
        it('should say an element completely below the viewport is off-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 100, 101, 120), false);
        });

        it('should say an element bigger than the screen is on-screen', function() {
            assert.equal(LogUtils.isInViewport(100, 110, 20, 200), true);
        });
    });

    describe("Visible Cards", function() {
        global.$ = $;
        it('should return the name of the card', function() {
            var el = $("<div data-name='test-card-name'></div>");
            var card = { element: el, pos: 1 };
            assert.equal(LogUtils.get_card_name(card), "test-card-name");
        });
        it('should return both cards as being "viewed"', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tc1'></div>");
            var el2 = $("<div data-name='tc2'></div>");

            var c1 = { element: el1, pos: 1};
            var c2 = { element: el2, pos: 2};

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2]);
            assert.equal(values.scrolled_out.length, 0);
            assert.equal(values.scrolled_in.length, 2);
        });

        it ('should return right number of cards as being currently visible', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tca1'></div>");
            var el2 = $("<div data-name='tca2'></div>");

            var c1 = { element: el1, pos: 1};
            var c2 = { element: el2, pos: 2};

            LogUtils.evaluateCurrentlyVisibleCards([c1, c2]);

            var visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c1, c2]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c1]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 1);

            LogUtils.evaluateCurrentlyVisibleCards([c2]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 1);

            LogUtils.evaluateCurrentlyVisibleCards([]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 0);
        });

        it ('should have a different random identifier for each scroll onto the screen', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tca1'></div>");
            var c1 = { element: el1, pos: 1};

            LogUtils.evaluateCurrentlyVisibleCards([c1]);
            var visible = LogUtils.getCurrentlyVisibleCards()[0];

            var initial_id = visible.rand;

            LogUtils.evaluateCurrentlyVisibleCards([]);
            LogUtils.evaluateCurrentlyVisibleCards([c1]);

            visible = LogUtils.getCurrentlyVisibleCards()[0];
            var id2 = visible.rand;

            assert.notEqual(id2, initial_id);
        });

        it('should return both cards as being scrolled off the screen', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tcb1'></div>");
            var el2 = $("<div data-name='tcb2'></div>");

            var c1 = { element: el1, pos: 1};
            var c2 = { element: el2, pos: 2};

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2]);
            assert.equal(values.scrolled_out.length, 0);
            assert.equal(values.scrolled_in.length, 2);

            values = LogUtils.evaluateCurrentlyVisibleCards([]);
            assert.equal(values.scrolled_out.length, 2);
            assert.equal(values.scrolled_in.length, 0);
        });

        it('should report a card as "read" after one second, but only once', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tcc1'></div>");

            var c1 = { element: el1, pos: 1};

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1]);

            visible = LogUtils.getCurrentlyVisibleCards()[0];
            assert.equal(visible.is_newly_read, false);
            assert.ok(visible.time_visible < 1.0);

            // Hacking some direct access...
            visible.first_onscreen -= 1000;

            visible = LogUtils.getCurrentlyVisibleCards()[0];

            assert.ok(visible.time_visible >= 1.0);
            assert.equal(visible.is_newly_read, true);

            // Make sure is_newly_read is only true once:
            visible = LogUtils.getCurrentlyVisibleCards()[0];

            assert.ok(visible.time_visible >= 1.0);
            assert.equal(visible.is_newly_read, false);

            // Scroll off, then back on, make sure everything behaves like it's new:
            LogUtils.evaluateCurrentlyVisibleCards([]);
            LogUtils.evaluateCurrentlyVisibleCards([c1]);

            visible = LogUtils.getCurrentlyVisibleCards()[0];
            assert.equal(visible.is_newly_read, false);
            assert.ok(visible.time_visible < 1.0);

            // Hacking some direct access...
            visible.first_onscreen -= 1000;

            visible = LogUtils.getCurrentlyVisibleCards()[0];

            assert.ok(visible.time_visible >= 1.0);
            assert.equal(visible.is_newly_read, true);

            // Make sure is_newly_read is only true once:
            visible = LogUtils.getCurrentlyVisibleCards()[0];

            assert.ok(visible.time_visible >= 1.0);
            assert.equal(visible.is_newly_read, false);


        });
    });

    describe("the actual logging", function() {
        it("should handle the basics", function() {
            LogUtils._resetVisibleCards();

            var log_entries = [];
            var my_log = new MyuwLog();
            my_log.card_logger = {
                info: function() {
                    log_entries.push(arguments);
                }
            };

            window = window || {};
            window.myuw_log = my_log;
            global.window = window;

            var el1 = $("<div data-name='tcd1'></div>");
            var c1 = { element: el1, pos: 1};

            window.myuw_log.log_card(c1, "view");
            window.myuw_log.log_card(c1, "woot");
            window.myuw_log.log_card(c1, "view");

            var log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "view");

            log1 = JSON.parse(log_entries[1]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "woot");

            log1 = JSON.parse(log_entries[2]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "view");
        });
        it("should log new cards that scroll onto the page", function() {
            LogUtils._resetVisibleCards();

            var log_entries = [];
            var my_log = new MyuwLog();
            my_log.card_logger = {
                info: function() {
                    log_entries.push(arguments);
                }
            };

            window = window || {};
            window.myuw_log = my_log;
            global.window = window;

            var el1 = $("<div data-name='tce1'></div>");
            var c1 = { element: el1, pos: 1};

            var el2 = $("<div data-name='tce2'></div>");
            var c2 = { element: el2, pos: 2};

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2]);
            LogUtils.logCardOnscreenChanges(values);

            log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "tce1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "view");

            log1 = JSON.parse(log_entries[1]["0"]);
            assert.equal(log1.card_name, "tce2");
            assert.equal(log1.card_position, "2");
            assert.equal(log1.action, "view");

            log_entries = [];

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1]);
            LogUtils.logCardOnscreenChanges(values);

            log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "tce2");
            assert.equal(log1.card_position, "2");
            assert.equal(log1.final, true);
            assert.ok(log1.time_visible >= 0.0);
            assert.equal(log1.action, "time_viewed");

        });
    });
});


