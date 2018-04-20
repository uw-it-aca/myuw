var Global = require("./global.js");

describe("WSData", function() {
    before(function (done) {
        Global.Environment.ajax_stub({
            '/api/v1/schedule/2013,summer,a-term': '/api/v1/schedule/2013,summer,a-term',
            '/api/v1/book/2013,summer,a-term': '/api/v1/book/2013,summer,a-term'
        });

        WSData.fetch_book_data('2013,summer,a-term', function(status){done()}, function(){});

    });

    it('clear cache', function(done) {

        var cached_book_data = WSData._book_data['2013,summer,a-term'];
        assert.notEqual(cached_book_data, undefined);

        Global.Environment.ajax_stub_restore();
        Global.Environment.ajax_stub({
            '/api/v1/book/2013,summer,a-term': '/api/v1/book/malformed_data'
        });

        WSData.fetch_book_data('2013,summer,a-term', function(){
            assert.equal(cached_book_data, WSData._book_data['2013,summer,a-term']);

            WSData.clear_cache();

            assert.equal(Object.keys(WSData._book_data).length, 0);

            console.log("But this is called")
            WSData.fetch_book_data('2013,summer,a-term', function(){
            WSData.fetch_book_data('2013,summer,a-term', function(){
                assert.equal(Object.keys(WSData._book_data['2013,summer,a-term']).length, 0);
                done()
            }, function(){});
        }, function(){});


    });

    after(function(){
        WSData.clear_cache();
        Global.Environment.ajax_stub_restore();
    });
});
