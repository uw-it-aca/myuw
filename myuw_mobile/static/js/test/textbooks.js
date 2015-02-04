TextBooks = require("../textbooks.js");

var assert = require("assert")
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

	it('should have some book data', function(){
	    var sections = [
		{
		    "course_title":"MECHANICS",
		    "curriculum_abbr":"PHYS",
		    "course_number":"121",
		    "section_id":"A",
		    "color_id":1,
		    "sln":"18529",
		},
		{
		    "course_title":"INTRO TRAIN I",
		    "curriculum_abbr":"TRAIN",
		    "course_number":"101",
		    "section_id":"A",
		    "color_id":3,
		    "sln":"13833",
		},
		{
		    "course_title":"ARCTIC RELATIONS",
		    "curriculum_abbr":"ARCTIC",
		    "course_number":"200",
		    "section_id":"A",
		    "color_id":6,
		    "sln":"11646",
		}
	    ];
	    var book_data = {
		"11646" : {
		    "isbn":"9780521600491",
		    "title":"History Of Archaeological Thought (2e 06)",
		    "authors":[{"name":"Trigger" }],
		    "price":45.00,
		    "used_price":null,
		    "required":true,
		    "notes":"required",
		    "cover_image":null
		},
		"18529" : {},
		"13833" : {}
	    };

	    var textbook_object = TextBooks.TextBooks
	    var data = textbook_object.process_book_data(book_data, { quarter: 'Spring', 'year': 2013, 'sections': sections });
	    assert.equal(data.quarter, "Spring");
	    assert.equal(data.year, 2013);
	    assert.equal(data.summer_term, null);
	    assert.equal(data.verba_link, null);
	    assert.equal(data.sections[0].sln, "18529");
	    assert.equal(data.sections[1].curriculum, "TRAIN");
	    assert.equal(data.sections[2].section_title, "ARCTIC RELATIONS");
	    assert.equal(data.sections[2].books.isbn, "9780521600491");

	    // textbook_object.term = {"year":"2013", "quarter":"spring"};
	    // var course_data = textbook_object.render_books();
	});
    });

    
});
  
