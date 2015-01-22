Handlebars = require("../../vendor/js/handlebars-v2.0.0.js");
moment = require("../../vendor/js/moment.2.8.3.min.js");

require("../handlebars-helpers.js");

var assert = require("assert")
describe('Handlebar-helpers', function(){
    describe('phonenumber', function(){
        it('should replace 10 digits with a formatted phone number', function(){
            var template = Handlebars.compile("{{formatPhoneNumber '5035551234'}}");
            var output = template();
            assert.equal(output, "503-555-1234");
        });
        it('should return the original string', function(){
            var template = Handlebars.compile("{{formatPhoneNumber '5551234'}}");
            var output = template();
            assert.equal(output, "5551234");
            var template = Handlebars.compile("{{formatPhoneNumber 'abcdefghij'}}");
            var output = template();
            assert.equal(output, "abcdefghij");
        });

    });

    describe('toFromNowDate', function(){
        it('should say in an hour', function(){
            var date = new Date();
            date.setHours(date.getHours()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in an hour");
        });
        it('should say tomorrow', function(){
            var date = new Date();
            date.setDate(date.getDate()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in a day");
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
            var template = Handlebars.compile("{{termNoYear '2013,spring,b-term' }}");
            var output = template();

            assert.equal(output, 'spring b-term');
        });

    });

    describe('acal_banner_date_format', function() {
        it("should give sunday (one date)", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-25'}}");
            var output = template();
            assert.equal(output, 'Jan 25 (sunday)');
        });

        it("should give sunday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-25' '2015-01-25' }}");
            var output = template();
            assert.equal(output, 'Jan 25 (sunday)');
        });
        it("should give monday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-26' '2015-01-26' }}");
            var output = template();
            assert.equal(output, 'Jan 26 (monday)');
        });
        it("should give tuesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-27' '2015-01-27' }}");
            var output = template();
            assert.equal(output, 'Jan 27 (tuesday)');
        });
        it("should give wednesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-28' '2015-01-28' }}");
            var output = template();
            assert.equal(output, 'Jan 28 (wednesday)');
        });
        it("should give thursday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-29' '2015-01-29' }}");
            var output = template();
            assert.equal(output, 'Jan 29 (thursday)');
        });
        it("should give friday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-30' '2015-01-30' }}");
            var output = template();
            assert.equal(output, 'Jan 30 (friday)');
        });
        it("should give saturday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-31' '2015-01-31' }}");
            var output = template();
            assert.equal(output, 'Jan 31 (saturday)');
        });
        it("should give Jan", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-01' '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1 (thursday)');
        });
        it("should give Feb", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-02-01' '2015-02-01' }}");
            var output = template();
            assert.equal(output, 'Feb 1 (sunday)');
        });
        it("should give Mar", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-03-01' '2015-03-01' }}");
            var output = template();
            assert.equal(output, 'Mar 1 (sunday)');
        });
        it("should give Apr", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-04-01' '2015-04-01' }}");
            var output = template();
            assert.equal(output, 'Apr 1 (wednesday)');
        });
        it("should give May", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-05-01' '2015-05-01' }}");
            var output = template();
            assert.equal(output, 'May 1 (friday)');
        });
        it("should give June", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-06-01' '2015-06-01' }}");
            var output = template();
            assert.equal(output, 'June 1 (monday)');
        });
        it("should give July", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-07-01' '2015-07-01' }}");
            var output = template();
            assert.equal(output, 'July 1 (wednesday)');
        });
        it("should give Aug", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-08-01' '2015-08-01' }}");
            var output = template();
            assert.equal(output, 'Aug 1 (saturday)');
        });
        it("should give Sept", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-09-01' '2015-09-01' }}");
            var output = template();
            assert.equal(output, 'Sept 1 (tuesday)');
        });
        it("should give Oct", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-10-01' '2015-10-01' }}");
            var output = template();
            assert.equal(output, 'Oct 1 (thursday)');
        });
        it("should give Nov", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-11-01' '2015-11-01' }}");
            var output = template();
            assert.equal(output, 'Nov 1 (sunday)');
        });
        it("should give Dec", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-12-01' '2015-12-01' }}");
            var output = template();
            assert.equal(output, 'Dec 1 (tuesday)');
        });

        it("should give in-month range", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-12-01' '2015-12-02' }}");
            var output = template();
            assert.equal(output, 'Dec 1 - 2');
        });

        it("should give multi-month range", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-09-29' '2015-10-25' }}");
            var output = template();
            assert.equal(output, 'Sept 29 - Oct 25');
        });
    });

    describe('acal_page_date_format', function() {
        it("should give Jan (one value)", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1');
        });

        it("should give Jan", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-01-01' '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1');
        });
        it("should give Feb", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-02-01' '2015-02-01' }}");
            var output = template();
            assert.equal(output, 'Feb 1');
        });
        it("should give Mar", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-03-01' '2015-03-01' }}");
            var output = template();
            assert.equal(output, 'Mar 1');
        });
        it("should give Apr", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-04-01' '2015-04-01' }}");
            var output = template();
            assert.equal(output, 'Apr 1');
        });
        it("should give May", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-05-01' '2015-05-01' }}");
            var output = template();
            assert.equal(output, 'May 1');
        });
        it("should give June", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-06-01' '2015-06-01' }}");
            var output = template();
            assert.equal(output, 'June 1');
        });
        it("should give July", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-07-01' '2015-07-01' }}");
            var output = template();
            assert.equal(output, 'July 1');
        });
        it("should give Aug", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-08-01' '2015-08-01' }}");
            var output = template();
            assert.equal(output, 'Aug 1');
        });
        it("should give Sept", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-09-01' '2015-09-01' }}");
            var output = template();
            assert.equal(output, 'Sept 1');
        });
        it("should give Oct", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-10-01' '2015-10-01' }}");
            var output = template();
            assert.equal(output, 'Oct 1');
        });
        it("should give Nov", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-11-01' '2015-11-01' }}");
            var output = template();
            assert.equal(output, 'Nov 1');
        });
        it("should give Dec", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-12-01' '2015-12-01' }}");
            var output = template();
            assert.equal(output, 'Dec 1');
        });

        it("should give in-month range", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-12-01' '2015-12-02' }}");
            var output = template();
            assert.equal(output, 'Dec 1 - 2');
        });

        it("should give multi-month range", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-09-29' '2015-10-25' }}");
            var output = template();
            assert.equal(output, 'Sept 29 - Oct 25');
        });
    });


});
