Handlebars = require("../../vendor/js/handlebars-v2.0.0.js");
moment = require("../../vendor/js/moment.2.8.3.min.js");

require("../handlebars-helpers.js");

var assert = require("assert")
describe('Handlebar-helpers', function() {
    describe('phonenumber', function() {
        it('should replace 10 digits with a formatted phone number', function() {
            var template = Handlebars.compile("{{formatPhoneNumber '5035551234'}}");
            var output = template();
            assert.equal(output, "503-555-1234");
        });
        it('should return the original string', function() {
            var template = Handlebars.compile("{{formatPhoneNumber '5551234'}}");
            var output = template();
            assert.equal(output, "5551234");
            var template = Handlebars.compile("{{formatPhoneNumber 'abcdefghij'}}");
            var output = template();
            assert.equal(output, "abcdefghij");
        });

    });

    describe('toFromNowDate', function() {
        it('should say in an hour', function() {
            var date = new Date();
            date.setHours(date.getHours()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in an hour");
        });
        it('should say tomorrow', function() {
            var date = new Date();
            date.setDate(date.getDate()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in a day");
        });

    });

    describe('toFriendlyDate', function() {
	it('should return date in friendly format', function() {
	    var template = Handlebars.compile("{{toFriendlyDate '2014-11-26'}}");
	    var output = template();

	    assert.equal(output, "Wed, Nov 26");
	});
    });
	    

    describe("toUrlSafe", function() {
        it ("should replace spaces", function() {
            var template = Handlebars.compile("{{toUrlSafe ' '}}");
            var output = template();
            assert.equal(output, "%20");
            var template = Handlebars.compile("{{toUrlSafe '_   _'}}");
            var output = template();
            assert.equal(output, "_%20%20%20_");
        });
    });

    describe("toLowerCase", function() {
        it ("should replace unicode", function() {
            var template = Handlebars.compile("{{toLowerCase 'OK!'}}");
            var output = template();
            assert.equal(output, "ok!");

            var template = Handlebars.compile("{{toLowerCase 'È'}}");
            var output = template();
            assert.equal(output, "è");
        });
        it ("should be ok with blank values", function() {
            var template = Handlebars.compile("{{toLowerCase ''}}");
            var output = template();
            assert.equal(output, "");
        });

    });

    describe("termNoYear", function() {
        it ("should work on non-summer terms", function() {
            var template = Handlebars.compile("{{termNoYear '2013,spring' }}");
            var output = template();

            assert.equal(output, 'spring');
        });
        it ("should work on summer terms", function() {
            var template = Handlebars.compile("{{termNoYear '2013,summer,b-term' }}");
            var output = template();

            assert.equal(output, 'summer b-term');
        });

    });

    describe("capitalizeString", function() {
	it ("should return capitalized string", function() {
	    var template = Handlebars.compile("{{capitalizeString 'this is a Sentence.' }}");
	    var output = template();

	    assert.equal(output, 'This Is A Sentence.');
	});	
    });

    describe("titleFormatTerm", function() {
	it ("should return formatted term title", function() {
	    var template = Handlebars.compile("{{titleFormatTerm '2013,summer,b-term'}}");
	    var output = template();

	    assert.equal(output, 'Summer 2013 B-Term')
	});	
    });  

    describe("formatTime", function() {
	it ("should return time in 12 hour format", function() {
	    var template = Handlebars.compile("{{formatTime '15:45' }}");
	    var output = template();

	    assert.equal(output, '3:45')
	});
	it ("should return time in 12 hour format with PM", function() {
	    var template = Handlebars.compile("{{formatTimeAMPM '15:45' }}");
	    var output = template();
	    
	    assert.equal(output, '3:45PM');
	});
	it ("should return time in 12 hour format with AM", function() {
	    var template = Handlebars.compile("{{formatTimeAMPM '4:45' }}");
	    var output = template();

	    assert.equal(output, '4:45AM');
	});   	     
    });

    describe("formatDateAsTime", function() {
	it ("should return time from date in 12 hour format", function() {
	    var template = Handlebars.compile("{{formatDateAsTime '2014-11-26 13:05:44' }}");
	    var output = template();

	    assert.equal(output, '1:05');
	});
	it ("should return time from date in 12 hour format with am", function() {
	    var template = Handlebars.compile("{{formatDateAsTimeAMPM '2014-11-26 11:03:45' }}");
	    var output = template();

	    assert.equal(output, '11:03AM');
	});
	it ("should return time from date in 12 hour format with pm", function() {
	    var template = Handlebars.compile("{{formatDateAsTimeAMPM '2014-11-26 13:22:21' }}");
	    var output = template();

	    assert.equal(output, '1:22PM');
	});
    });

    describe("formatDate", function() {
	it ("should return formatted date", function() {
	    var template = Handlebars.compile("{{formatDateAsDate '2014-11-26'}}");
	    var output = template();

	    assert.equal(output, 'Wed, Nov 26');
	});
	it ("should return formatted date for final exam schedule", function() {
	    var template = Handlebars.compile("{{formatDateAsFinalsDay '2014-11-26' '3'}}");
	    var output = template();

	    assert.equal(output, 'Nov 23');
	});
    });

    describe("ucfirst", function() {
	it ("should capitalize first letter", function() {
	    var template = Handlebars.compile("{{ucfirst 'this is a Sentence.' }}");
	    var output = template();

	    assert.equal(output, 'This is a Sentence.')
	});
    });

    describe("formatPrice", function() {
	it ("should append 0 to price", function() {
	    var template = Handlebars.compile("{{formatPrice '$4.5'}}");
	    var output = template();

	    assert.equal(output, '$4.50');
	});
	it ("should append 00 to price", function() {
	    var template = Handlebars.compile("{{formatPrice '$4.'}}");
	    var output = template();

	    assert.equal(output, '$4.00');
	});
    });
    
    // describe("testNameHere", function() {
    // 	it ("should do something", function() {
    // 	    var template = Handlebars.compile("{{ 'template_name' }}");
    // 	    var output = template();

    // 	    assert.somethings
    // 	});	
    // });
});
