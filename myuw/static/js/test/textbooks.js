TextBooks = require("../textbooks.js");
myuwFeatureEnabled = function () {
    return true;
};

var assert = require("assert");
describe('TextBooks', function(){
    describe('process_book_data', function(){
        it('should have no book data', function(){
            var data = TextBooks.TextBooks.process_book_data({}, { quarter: 'Spring', 'year': 2013, 'sections': [] });
            assert.deepEqual(data.sections, []);
            assert.equal(data.quarter, "Spring");
            assert.equal(data.year, 2013);
            assert.equal(data.summer_term, null);
            assert.equal(data.verba_link, null);
        });
    });
});
  
