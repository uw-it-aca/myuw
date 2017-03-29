var Global = require("./global.js");

describe("Logging", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "../myuw_log.js"
            ]
        });
    });
    describe("Viewport Test", function() {
        // Newly on-screen tests
        it('should say an element fully on-screen is in the viewport', function() {
            assert.equal(LogUtils.isInViewport(0, 50, 10, 20), true);
        });

        it('should say an element above, but 50% on is on-screen', function() {
            assert.equal(LogUtils.isInViewport(100, 1000, 50, 150), true);
        });

        it('should say an element below, but 50% on is on-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 1000, 950, 1050), true);
        });

        it('should say an element mostly below-screen, but taking 50% of the screen, is on-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 100, 50, 1000000), true);
        });

        it('should say an element mostly below-screen, but taking 40% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isInViewport(0, 100, 60, 1000000), false);
        });

        it('should say an element mostly above-screen, but taking 50% of the screen, is on-screen', function() {
            assert.equal(LogUtils.isInViewport(10000, 10100, 0, 10050), true);
        });

        it('should say an element mostly above-screen, but taking 40% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isInViewport(10000, 10100, 0, 10040), false);
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

        // Newly off-screen tests
        it('should not say an element fully on-screen is off the viewport', function() {
            assert.equal(LogUtils.isOffViewport(0, 50, 10, 20), false);
        });

        it('should say an element above, but 10% on not off-screen', function() {
            assert.equal(LogUtils.isOffViewport(100, 1000, 10, 110), false);
        });

        it('should say an element below, but 10% on is not off-screen', function() {
            assert.equal(LogUtils.isOffViewport(0, 1000, 990, 1090), false);
        });

        it('should say an element mostly below-screen, but taking 10% of the screen, is not off-screen', function() {
            assert.equal(LogUtils.isOffViewport(0, 100, 90, 1000000), false);
        });

        it('should say an element mostly below-screen, but taking 5% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isOffViewport(0, 100, 95, 1000000), true);
        });

        it('should say an element mostly above-screen, but taking 10% of the screen, is not off-screen', function() {
            assert.equal(LogUtils.isOffViewport(10000, 10100, 0, 10010), false);
        });

        it('should say an element mostly above-screen, but taking 5% of the screen, is off-screen', function() {
            assert.equal(LogUtils.isOffViewport(10000, 10100, 0, 10005), true);
        });

        it('should say an element completely above the viewport is off-screen', function() {
            assert.equal(LogUtils.isOffViewport(10000, 10100, 0, 100), true);
        });
        it('should say an element completely below the viewport is off-screen', function() {
            assert.equal(LogUtils.isOffViewport(0, 100, 101, 120), true);
        });

        it('should say an element bigger than the screen is not off-screen', function() {
            assert.equal(LogUtils.isOffViewport(100, 110, 20, 200), false);
        });
    });

    describe("Visible Cards", function() {
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

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);
            assert.equal(values.scrolled_out.length, 0);
            assert.equal(values.scrolled_in.length, 2);
        });

        it ('should return right number of cards as being currently visible when none of the cards pass the off-screen threshold', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tca1'></div>");
            var el2 = $("<div data-name='tca2'></div>");

            var c1 = { element: el1, pos: 1};
            var c2 = { element: el2, pos: 2};

            LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);

            var visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c1], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c2], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);
        });
        it ('should return right number of cards as being currently visible when cards do pass the off-screen threshold', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tca1'></div>");
            var el2 = $("<div data-name='tca2'></div>");

            var c1 = { element: el1, pos: 1};
            var c2 = { element: el2, pos: 2};

            LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);

            var visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c1], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([c2], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([], []);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 2);

            LogUtils.evaluateCurrentlyVisibleCards([], [c1]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 1);

            LogUtils.evaluateCurrentlyVisibleCards([], [c1]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 1);

            LogUtils.evaluateCurrentlyVisibleCards([], [c2]);
            visible = LogUtils.getCurrentlyVisibleCards();
            assert.equal(visible.length, 0);


        });

        it ('should have a different random identifier for each scroll onto the screen', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tca1'></div>");
            var c1 = { element: el1, pos: 1};

            LogUtils.evaluateCurrentlyVisibleCards([c1], []);
            var visible = LogUtils.getCurrentlyVisibleCards()[0];

            var initial_id = visible.rand;

            LogUtils.evaluateCurrentlyVisibleCards([], [c1]);
            LogUtils.evaluateCurrentlyVisibleCards([c1], []);

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

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);
            assert.equal(values.scrolled_out.length, 0);
            assert.equal(values.scrolled_in.length, 2);

            values = LogUtils.evaluateCurrentlyVisibleCards([], [c2, c1]);
            assert.equal(values.scrolled_out.length, 2);
            assert.equal(values.scrolled_in.length, 0);
        });

        it('should report a card as "read" after one second, but only once', function() {
            LogUtils._resetVisibleCards();
            var el1 = $("<div data-name='tcc1'></div>");

            var c1 = { element: el1, pos: 1};

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1], []);

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
            LogUtils.evaluateCurrentlyVisibleCards([], [c1]);
            LogUtils.evaluateCurrentlyVisibleCards([c1], []);

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

            var original_height = $.prototype.height;
            var original_width = $.prototype.width;

            $.prototype.height = function() { return 200; };
            $.prototype.width = function() { return 500; };

            window.myuw_log.log_card(c1, "view");

            $.prototype.height = function() { return 300; };
            $.prototype.width = function() { return 600; };

            window.myuw_log.log_card(c1, "woot");
            window.myuw_log.log_card(c1, "view");

            var log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "view");
            assert.equal(log1.screen_width, 500);
            assert.equal(log1.screen_height, 200);

            log1 = JSON.parse(log_entries[1]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "woot");
            assert.equal(log1.screen_width, 600);
            assert.equal(log1.screen_height, 300);

            log1 = JSON.parse(log_entries[2]["0"]);
            assert.equal(log1.card_name, "tcd1");
            assert.equal(log1.card_position, "1");
            assert.equal(log1.action, "view");

            $.prototype.height = original_height;
            $.prototype.width = original_width;
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

            var values = LogUtils.evaluateCurrentlyVisibleCards([c1, c2], []);
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

            values = LogUtils.evaluateCurrentlyVisibleCards([c1], [c2]);
            LogUtils.logCardOnscreenChanges(values);

            log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "tce2");
            assert.equal(log1.card_position, "2");
            assert.equal(log1.final, true);
            assert.ok(log1.time_visible >= 0.0);
            assert.equal(log1.action, "time_viewed");

        });
        it ("should log cards when they load", function() {

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

            var original_height = $.prototype.height;
            var original_offset = $.prototype.offset;

            // Monkey-patch jquery so all elements are 100px tall
            $.prototype.height = function() { return 100; };

            // Monkey-patch jquery so all elements are at 10px
            $.prototype.offset = function() { return { top: 10 }; };

            LogUtils.registerCardLoadEvents();
            LogUtils.cardLoaded("TestCard", $("<div></div>"));

            log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "TestCard");
            assert.equal(log1.on_screen, true);
            assert.equal(log1.action, "loaded");

            log_entries = [];
            // Monkey-patch jquery so all elements are at 10px
            $.prototype.offset = function() { return { top: 200 }; };
            LogUtils.cardLoaded("TestCard2", $("<div></div>"));

            log1 = JSON.parse(log_entries[0]["0"]);
            assert.equal(log1.card_name, "TestCard2");
            assert.equal(log1.on_screen, false);
            assert.equal(log1.action, "loaded");

            $.prototype.offset = original_offset;
            $.prototype.height = original_height;
        });
    });
});


describe("Visible Links", function() {
    before(function () {
        Global.Environment.init({
            scripts: [
                "../myuw_log.js"
            ]
        });
    });
    it('should return tue right disclosed state for a links parent', function() {
        var undisclosed = $("<div aria-hidden='true'>")[0];
        var link1 = $("<a href='http://www.google.com'>Google</a>")[0];

        undisclosed = $(undisclosed).append(link1)[0];
        var undis_link = $(undisclosed).children('a')[0];
        assert.equal(LogUtils.is_link_disclosed(undis_link), false);

        var disclosed = $("<div aria-hidden='false'>")[0];
        disclosed = $(disclosed).append(link1)[0];
        var dis_link = $(disclosed).children('a')[0];
        assert.equal(LogUtils.is_link_disclosed(dis_link), true);

    });
});

