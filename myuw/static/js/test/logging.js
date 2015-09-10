
var log = require("../myuw_log.js");
var LogUtils = log.LogUtils;
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

    });
});


