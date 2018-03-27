Handlebars = require("../../vendor/js/handlebars-v4.0.5.js");
moment = require("../../vendor/js/moment.2.18.1.min.js");
require("datejs");
require("../visual_schedule.js");
require("../handlebars-helpers.js");

var assert = require("assert");
describe('Handlebar-helpers', function(){

    describe('formatPhoneNumber', function(){
        it('should replace 10 digits with a formatted phone number', function(){
            var template = Handlebars.compile("{{formatPhoneNumber '5035551234'}}");
            var output = template();
            assert.equal(output, "503-555-1234");
        });
        it('should return the original string', function(){
            var template = Handlebars.compile("{{formatPhoneNumber '5551234'}}");
            var output = template();
            assert.equal(output, "5551234");
            template = Handlebars.compile("{{formatPhoneNumber 'abcdefghij'}}");
            output = template();
            assert.equal(output, "abcdefghij");
        });
    });

    describe('strToInt', function(){
        it('should convert string to int', function(){
            var template = Handlebars.compile("{{strToInt '2.0'}}");
            var output = template();
            assert.equal(output, 2);
            var template = Handlebars.compile("{{strToInt '10.0'}}");
            var output = template();
            assert.equal(output, 10);
        });
    });

    describe('date_from_string', function(){
        it('should work for YYYY-MM-DD hh:mm:ss', function(){
            var d = date_from_string('2013-04-22 10:57:06-08:00');
            assert(d);
        });
        it('should work for YYYY-MM-DDThh:mm:ss', function(){
            var d = date_from_string('2013-04-22T10:57:06-08:00');
            assert(d);
        });
    });

    describe('toMonthDay', function(){
        it('should work for YYYY-MM-DD hh:mm', function(){
            var template = Handlebars.compile("{{toMonthDay '2013-06-10 08:30'}}");
            var output = template();
            assert.equal(output, 'Jun 10');
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

    describe("toFriendlyDate", function() {
        it ("should handle a date", function() {
            var template = Handlebars.compile("{{toFriendlyDate '2013-03-04'}}");
            var output = template();
            assert.equal(output, 'Mon, Mar 4');
        });
        it ("should handle a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDate '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Mon, Mar 4');
        });
        it ("should handle empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDate ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("toFriendlyDateVerbose", function() {
        it ("should convert to dddd, MMMM D", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose '2013-03-04'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4');
        });
        it ("should handle a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4');
        });
        it ("should handle empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatDateAsTime", function() {
        it ("should convert a date to 12 hour display", function() {
            var template = Handlebars.compile("{{formatDateAsTime '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, '1:30');
        });
        it ("should handle midnight time", function() {
            var template = Handlebars.compile("{{formatDateAsTime '2013-03-04 00:00'}}");
            var output = template();
            assert.equal(output, '0:00');
        });
        it ("should handle undefined date", function() {
            var template = Handlebars.compile("{{formatDateAsTime ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatDateAsTimeAMPM", function() {
        it ("should convert PM", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, '1:30PM');
        });
        it ("should convert AM", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM '2013-03-04 08:00'}}");
            var output = template();
            assert.equal(output, '8:00AM');
        });
        it ("should handle undefined date", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatTime", function() {
        it ("should return HH:MM{AM,PM}", function() {
            var template = Handlebars.compile("{{formatTime '13:30:00'}}");
            var output = template();
            assert.equal(output, "1:30");
            template = Handlebars.compile("{{formatTime '12:30:00'}}");
            output = template();
            assert.equal(output, "12:30");
        });
    });

    describe("formatTimeAMPM", function() {
        it ("should return HH:MM{AM,PM}", function() {
            var template = Handlebars.compile("{{formatTimeAMPM '12:00:00'}}");
            var output = template();
            assert.equal(output, "12:00PM");
            template = Handlebars.compile("{{formatTimeAMPM '11:30:00'}}");
            output = template();
            assert.equal(output, "11:30AM");
        });
    });

    describe("toUrlSafe", function() {
        it ("should replace spaces", function() {
            var template = Handlebars.compile("{{toUrlSafe ' '}}");
            var output = template();
            assert.equal(output, "%20");
            template = Handlebars.compile("{{toUrlSafe '_   _'}}");
            output = template();
            assert.equal(output, "_%20%20%20_");
        });
    });

    describe("toAnchorName", function() {
        it ("should replace spaces", function() {
            template = Handlebars.compile("{{toAnchorName 'B BIO'}}");
            output = template();
            assert.equal(output, "B-BIO");
        });
    });

    describe("toLowerCase", function() {
        it ("should replace unicode", function() {
            var template = Handlebars.compile("{{toLowerCase 'OK!'}}");
            var output = template();
            assert.equal(output, "ok!");

            template = Handlebars.compile("{{toLowerCase 'È'}}");
            output = template();
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
            assert.equal(output, 'Jan 25 (Sunday)');
        });

        it("should give sunday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-25' '2015-01-25' }}");
            var output = template();
            assert.equal(output, 'Jan 25 (Sunday)');
        });
        it("should give monday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-26' '2015-01-26' }}");
            var output = template();
            assert.equal(output, 'Jan 26 (Monday)');
        });
        it("should give tuesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-27' '2015-01-27' }}");
            var output = template();
            assert.equal(output, 'Jan 27 (Tuesday)');
        });
        it("should give wednesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-28' '2015-01-28' }}");
            var output = template();
            assert.equal(output, 'Jan 28 (Wednesday)');
        });
        it("should give thursday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-29' '2015-01-29' }}");
            var output = template();
            assert.equal(output, 'Jan 29 (Thursday)');
        });
        it("should give friday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-30' '2015-01-30' }}");
            var output = template();
            assert.equal(output, 'Jan 30 (Friday)');
        });
        it("should give saturday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-31' '2015-01-31' }}");
            var output = template();
            assert.equal(output, 'Jan 31 (Saturday)');
        });
        it("should give Jan", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-01' '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1 (Thursday)');
        });
        it("should give Feb", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-02-01' '2015-02-01' }}");
            var output = template();
            assert.equal(output, 'Feb 1 (Sunday)');
        });
        it("should give Mar", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-03-01' '2015-03-01' }}");
            var output = template();
            assert.equal(output, 'Mar 1 (Sunday)');
        });
        it("should give Apr", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-04-01' '2015-04-01' }}");
            var output = template();
            assert.equal(output, 'Apr 1 (Wednesday)');
        });
        it("should give May", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-05-01' '2015-05-01' }}");
            var output = template();
            assert.equal(output, 'May 1 (Friday)');
        });
        it("should give June", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-06-01' '2015-06-01' }}");
            var output = template();
            assert.equal(output, 'June 1 (Monday)');
        });
        it("should give July", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-07-01' '2015-07-01' }}");
            var output = template();
            assert.equal(output, 'July 1 (Wednesday)');
        });
        it("should give Aug", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-08-01' '2015-08-01' }}");
            var output = template();
            assert.equal(output, 'Aug 1 (Saturday)');
        });
        it("should give Sept", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-09-01' '2015-09-01' }}");
            var output = template();
            assert.equal(output, 'Sept 1 (Tuesday)');
        });
        it("should give Oct", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-10-01' '2015-10-01' }}");
            var output = template();
            assert.equal(output, 'Oct 1 (Thursday)');
        });
        it("should give Nov", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-11-01' '2015-11-01' }}");
            var output = template();
            assert.equal(output, 'Nov 1 (Sunday)');
        });
        it("should give Dec", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-12-01' '2015-12-01' }}");
            var output = template();
            assert.equal(output, 'Dec 1 (Tuesday)');
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

    describe('phone_number', function() {
        it("formatted from 555.555.5555", function() {
            var template = Handlebars.compile("{{phone_number '555.555.5555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted from 5555555555", function() {
            var template = Handlebars.compile("{{phone_number '5555555555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted from 555 555-5555", function() {
            var template = Handlebars.compile("{{phone_number '555 555-5555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("unformatted (555)555-5555", function() {
            var template = Handlebars.compile("{{phone_number '(555)555-5555' }}");
            var output = template();
            assert.equal(output, '(555)555-5555');
        });
        it("unformatted 555-5555", function() {
            var template = Handlebars.compile("{{phone_number '555-5555' }}");
            var output = template();
            assert.equal(output, '555-5555');
        });
    });

    describe('short-year', function() {
        it('should handle an integer', function() {
            var template = Handlebars.compile("{{short_year 2013 }}");
            var output = template();

            assert.equal(output, '’13');
        });
        it('should handle a string', function() {
            var template = Handlebars.compile("{{short_year '2017'}}");
            var output = template();

            assert.equal(output, '’17');
        });

    });

    describe("toTitleCase", function() {
        it ("should handle summer term", function() {
            var template = Handlebars.compile("{{toTitleCase 'summer a-term'}}");
            var output = template();
            assert.equal(output, "Summer A-Term");
            template = Handlebars.compile("{{toTitleCase 'summer b-term'}}");
            output = template();
            assert.equal(output, "Summer B-Term");

            template = Handlebars.compile("{{toTitleCase 'winter, 2013'}}");
            output = template();
            assert.equal(output, "Winter 2013");

            template = Handlebars.compile("{{toTitleCase 'spring'}}");
            output = template();
            assert.equal(output, "Spring");

            template = Handlebars.compile("{{toTitleCase 'summer,2013,a-term'}}");
            output = template();
            assert.equal(output, "Summer 2013 A-Term");

            template = Handlebars.compile("{{toTitleCase '2013 summer, a-term'}}");
            output = template();
            assert.equal(output, "2013 Summer A-Term");
        });
    });

    describe("titleFormatTerm", function() {
        it ("should handle summer term", function() {
            var template = Handlebars.compile("{{titleFormatTerm '2013,summer,a-term'}}");
            var output = template();
            assert.equal(output, "Summer 2013 A-Term");

            template = Handlebars.compile("{{titleFormatTerm '2013,winter'}}");
            output = template();
            assert.equal(output, "Winter 2013");
        });
    });

    describe("ucfirst", function() {
        it ("should handle section type", function() {
            var template = Handlebars.compile("{{ucfirst 'QUIZ'}}");
            var output = template();
            assert.equal(output, "Quiz");
        });
        it ("should handle quarter", function() {
            template = Handlebars.compile("{{ucfirst 'summer'}}");
            output = template();
            assert.equal(output, "Summer");
        });
    });

    describe('formatPrice', function(){
        it('should handle normal amount', function(){
            var template = Handlebars.compile("{{formatPrice '125.34'}}");
            var output = template();
            assert.equal(output, 125.34);
        });
        it ("should handle integer", function() {
            var template = Handlebars.compile("{{formatPrice '10'}}");
            var output = template();
            assert.equal(output, 10.00);
        });
        it ("should handle zero", function() {
            var template = Handlebars.compile("{{formatPrice '0'}}");
            var output = template();
            assert.equal(output, 0.00);
        });
    });

    describe('format_schedule_hour', function(){
        it('should handle am', function(){
            var template = Handlebars.compile("{{format_schedule_hour '08' 0}}");
            var output = template();
            assert.equal(output, '08a');
        });
        it ("should handle pm", function() {
            var template = Handlebars.compile("{{format_schedule_hour '13' 0}}");
            var output = template();
            assert.equal(output, '1p');
            var template = Handlebars.compile("{{format_schedule_hour '22' 0}}");
            var output = template();
            assert.equal(output, '10p');
        });
    });

    describe('pluralize', function(){
        it('should handle plural', function(){
            var template = Handlebars.compile("{{pluralize 2 'day' 'days'}}");
            var output = template();
            assert.equal(output, 'days');
        });
        it('should handle singular', function(){
            var template = Handlebars.compile("{{pluralize 1 'hold' 'holds'}}");
            var output = template();
            assert.equal(output, 'hold');
        });
    });

    describe('pluralize_by_size', function(){
        it('should handle plural', function(){
            var alist = ["A", "B"];
            var raw = "{{pluralize_by_size '" + alist + "' 'Major' 'Majors'}}";
            var template = Handlebars.compile(raw);
            var output = template();
            assert.equal(output, 'Majors');
        });
        it('should handle singular', function(){
            var alist = ['A'];
            var raw = "{{pluralize_by_size '" + alist + "' 'Major' 'Majors'}}";
            var template = Handlebars.compile(raw);
            var output = template();
            assert.equal(output, 'Major');
        });
    });

    describe('get_quarter_code', function(){
        it('should each quarter', function(){
            var template = Handlebars.compile("{{get_quarter_code 'Winter'}}");
            var output = template();
            assert.equal(output, 1);
            var template = Handlebars.compile("{{get_quarter_code 'Spring'}}");
            var output = template();
            assert.equal(output, 2);
            var template = Handlebars.compile("{{get_quarter_code 'Summer'}}");
            var output = template();
            assert.equal(output, 3);
            var template = Handlebars.compile("{{get_quarter_code 'Autumn'}}");
            var output = template();
            assert.equal(output, 4);
        });
        it('should handle empty input', function(){
            var template = Handlebars.compile("{{get_quarter_code ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe('get_quarter_abbreviation', function(){
        it('should each quarter', function(){
            var template = Handlebars.compile("{{get_quarter_abbreviation 'Winter'}}");
            var output = template();
            assert.equal(output, 'WIN');
            var template = Handlebars.compile("{{get_quarter_abbreviation 'Spring'}}");
            var output = template();
            assert.equal(output, 'SPR');
            var template = Handlebars.compile("{{get_quarter_abbreviation 'Summer'}}");
            var output = template();
            assert.equal(output, 'SUM');
            var template = Handlebars.compile("{{get_quarter_abbreviation 'Autumn'}}");
            var output = template();
            assert.equal(output, 'AUT');
        });
        it('should handle empty input', function(){
            var template = Handlebars.compile("{{get_quarter_abbreviation ''}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe('slugify', function(){
        it('should place consecutive spaces with -', function(){
            var template = Handlebars.compile("{{slugify '2013 Summer ASE 510 A'}}");
            var output = template();
            assert.equal(output, '2013-summer-ase-510-a');
        });
    });

    describe('shorten_meeting_type', function(){
        it('should truncate after the third char', function(){
            var template = Handlebars.compile("{{shorten_meeting_type 'LECTURE'}}");
            var output = template();
            assert.equal(output, 'LEC');
        });
    });

    describe('phone_number', function(){
        it('should handle regular phone number format', function(){
            var template = Handlebars.compile("{{phone_number '206 220 4514'}}");
            var output = template();
            assert.equal(output, '(206) 220-4514');
            var template = Handlebars.compile("{{phone_number '206-220-4514'}}");
            var output = template();
            assert.equal(output, '(206) 220-4514');
        });
    });

    
});
