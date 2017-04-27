var Global = require("./global.js");

describe('TextBooks', function(){
    describe('process_book_data', function(){
        before(function () {
            Global.Environment.init({
                scripts: [
                    "myuw/static/js/textbooks.js"
                ]
            });

            window.enabled_features = { 'instructor_schedule': true };

        });
        it('should have no book data', function(){
            var data = TextBooks.process_book_data({}, { quarter: 'Spring', 'year': 2013, 'sections': [] });
            assert.deepEqual(data.sections, []);
            assert.equal(data.quarter, "Spring");
            assert.equal(data.year, 2013);
            assert.equal(data.summer_term, null);
            assert.equal(data.verba_link, null);
        });
    });
});
  
