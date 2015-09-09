
var log = require("../myuw_log.js");
var LogUtils = log.LogUtils;

var assert = require("assert");

describe("Logging", function() {
    describe("viewport_test", function() {
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
});
