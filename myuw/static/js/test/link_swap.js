var assert = require("assert");
var Global = require("./global.js");


describe('LinkToFormSubmit', function() {
    describe('link_clicks', function() {
        before(function (done) {
            Global.Environment.init({
                scripts: []
            });
            done();
        });
        it('should swap http/https links', function() {
            var content = "<div><a id='l1' href='http://example.com'>Link 1</a><a id='l2' target='new_window' href='https://example.com'>Link 2</a></div>";

            $('body').append($(content));

            $('body').off('click', "A");
            register_link_recorder();

            global.csrf_token = 'fake_token';

            $("#l1").click();
            $("#l2").click();
            $("#l1").click();

            assert.equal($("#l1").attr('myuw-data-href'), 'http://example.com');
            assert.equal($("#l1").attr('href'), '/out?u='+encodeURIComponent('http://example.com')+'&l='+encodeURIComponent('Link 1'));

            assert.equal($("#l2").attr('myuw-data-href'), 'https://example.com');
            assert.equal($("#l2").attr('href'), '/out?u='+encodeURIComponent('https://example.com')+'&l='+encodeURIComponent('Link 2'));

        });
        it('should not swap local/hash/javascript/data links', function() {
            var content = "<div><a id='l1' href='javascript:void'>Link 1</a><a id='l2' href='/some_url'>Link 2</a><a id='l3' href='data:,Hello%2C%20World!'>L3</a><a href='#' id='l4'>L 4</a></div>";

            $('body').html('');
            $('body').append($(content));

            $('body').off('click', "A");
            register_link_recorder();

            global.csrf_token = 'fake_token';
            $("#l1").click();
            $("#l2").click();
            $("#l3").click();
            $("#l4").click();

            assert.equal($("#l1").attr('myuw-data-href'), undefined);
            assert.equal($("#l1").attr('href'), 'javascript:void');
            assert.equal($("#l2").attr('myuw-data-href'), undefined);
            assert.equal($("#l2").attr('href'), '/some_url');
            assert.equal($("#l3").attr('myuw-data-href'), undefined);
            assert.equal($("#l3").attr('href'), 'data:,Hello%2C%20World!');
            assert.equal($("#l4").attr('myuw-data-href'), undefined);
            assert.equal($("#l4").attr('href'), '#');

        });
        it('should read a data-linklabel attr if it exists', function() {
            var content = "<div><a id='dl1' href='http://example.com' data-linklabel='Link for TRAIN 101'>Link 1</a></div>";

            $('body').append($(content));

            $('body').off('click', "A");
            register_link_recorder();

            global.csrf_token = 'fake_token';

            $("#dl1").click();

            assert.equal($("#dl1").attr('myuw-data-href'), 'http://example.com');
            assert.equal($("#dl1").attr('href'), '/out?u='+encodeURIComponent('http://example.com')+'&l='+encodeURIComponent('Link for TRAIN 101'));


        });
        it('should work with search results', function() {
            var content = "<div><a id='s1' href='http://uw.edu?u=something' data-ctorig='http://example.com'>Link 1</a></div>";
            $('body').append($(content));

            $('body').off('click', "A");
            register_link_recorder();

            global.csrf_token = 'fake_token';

            $("#s1").click();
            assert.equal($("#s1").attr('myuw-data-href'), 'http://example.com');
            assert.equal($("#s1").attr('href'), '/out?u='+encodeURIComponent('http://example.com')+'&l='+encodeURIComponent('Link 1'));
        });
        after(function () {
            Global.Environment.ajax_stub_restore();
        });
    });
});

