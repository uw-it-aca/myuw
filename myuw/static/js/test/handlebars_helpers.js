Handlebars = require("../../vendor/js/handlebars-v4.5.3.js");
moment = require("../../vendor/js/moment.2.18.1.min.js");
require("datejs");
require("../card/schedule/visual.js");
require("../handlebars-helpers.js");


var assert = require("assert");
describe('Handlebar-helpers', function(){

    describe('formatPhoneNumber', function(){
        it("formatted from 555.555.5555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '555.555.5555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted from 5555555555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '5555555555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted from +1 555 555-5555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '+1 555 555-5555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted from 555 555-5555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '555 555-5555' }}");
            var output = template();
            assert.equal(output, '(555) 555-5555');
        });
        it("formatted (555)555-5555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '(555)555-5555' }}");
            var output = template();
            assert.equal(output, '(555)555-5555');
        });
        it("formatted 555-5555", function() {
            var template = Handlebars.compile("{{formatPhoneNumber '555-5555' }}");
            var output = template();
            assert.equal(output, '555-5555');
        });
        it('empty value', function(){
            var template = Handlebars.compile("{{formatPhoneNumber ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it('undefined param', function(){
            var template = Handlebars.compile("{{formatPhoneNumber undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe('strToInt', function(){
        it('convert string to int', function(){
            var template = Handlebars.compile("{{strToInt '2.0'}}");
            var output = template();
            assert.equal(output, 2);

            var template = Handlebars.compile("{{strToInt '10.0'}}");
            var output = template();
            assert.equal(output, 10);
        });
    });

    describe('date_from_string', function(){
        it('work for YYYY-MM-DD hh:mm:ss', function(){
            var d = date_from_string('2013-04-22 10:57:06-08:00');
            assert(d);
        });
        it('work for YYYY-MM-DDThh:mm:ss', function(){
            var d = date_from_string('2013-04-22T10:57:06-08:00');
            assert(d);
        });
    });

    describe('toMonthDay', function(){
        it('work for YYYY-MM-DD hh:mm', function(){
            var template = Handlebars.compile("{{toMonthDay '2013-06-10 08:30'}}");
            var output = template();
            assert.equal(output, 'Jun 10');
        });
    });

    describe('toFromNowDate', function(){
        it('in an hour', function(){
            var date = new Date();
            date.setHours(date.getHours()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in an hour");
        });
        it('in a day', function(){
            var date = new Date();
            date.setDate(date.getDate()+1);
            var str = date.toString();
            var template = Handlebars.compile("{{toFromNowDate '"+str+"'}}");
            var output = template();
            assert.equal(output, "in a day");
        });

    });

    describe("toFriendlyDate", function() {
        it ("work for a date", function() {
            var template = Handlebars.compile("{{toFriendlyDate '2013-03-04'}}");
            var output = template();
            assert.equal(output, 'Mon, Mar 4');
        });
        it ("work for a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDate '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Mon, Mar 4');
        });
        it ("work for a timezone datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDate '2018-06-07 06:59:59 UTC+0000'}}");
            var output = template();
            assert.equal(output, 'Thu, Jun 7');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDate ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{toFriendlyDate undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("toFriendlyDatetime", function() {
        it ("work for a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDatetime '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Mon, Mar 4, 1:30PM');
        });
        it ("work for a timezone datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDatetime '2018-06-07 06:59:59 UTC+0000'}}");
            var output = template();
            assert.equal(output, 'Thu, Jun 7, 6:59AM');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDatetime ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{toFriendlyDatetime undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("toFriendlyDateVerbose", function() {
        it ("work for a date", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose '2013-03-04'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4');
        });
        it ("work for a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{toFriendlyDateVerbose undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });
    describe("toFriendlyDatetimeVerbose", function() {
        it ("work for a date", function() {
            var template = Handlebars.compile("{{toFriendlyDatetimeVerbose '2013-03-04'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4, 12:00AM');
        });
        it ("work for a datetime", function() {
            var template = Handlebars.compile("{{toFriendlyDatetimeVerbose '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Monday, March 4, 1:30PM');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{toFriendlyDatetimeVerbose ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{toFriendlyDatetimeVerbose undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });
    describe("formatDateAsFinalsDay", function() {
        it ("work for a date", function() {
            var template = Handlebars.compile("{{formatDateAsFinalsDay '2013-06-14' 4}}");
            var output = template();
            assert.equal(output, 'Jun 10');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{formatDateAsFinalsDay '' 0}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{formatDateAsFinalsDay undefined 0}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatDateAsTime", function() {
        it ("convert a date to 12 hour display", function() {
            var template = Handlebars.compile("{{formatDateAsTime '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, '1:30');
        });
        it ("midnight time", function() {
            var template = Handlebars.compile("{{formatDateAsTime '2013-03-04 00:00'}}");
            var output = template();
            assert.equal(output, '0:00');
        });
        it ("undefined date", function() {
            var template = Handlebars.compile("{{formatDateAsTime ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{formatDateAsTime undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatDateAsTimeAMPM", function() {
        it ("convert PM", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, '1:30PM');
        });
        it ("convert AM", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM '2013-03-04 08:00'}}");
            var output = template();
            assert.equal(output, '8:00AM');
        });
        it ("empty date", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it ("undefined", function() {
            var template = Handlebars.compile("{{formatDateAsTimeAMPM undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe("formatTime", function() {
        it ("return HH:MM{AM,PM}", function() {
            var template = Handlebars.compile("{{formatTime '13:30:00'}}");
            var output = template();
            assert.equal(output, "1:30");
            template = Handlebars.compile("{{formatTime '12:30:00'}}");
            output = template();
            assert.equal(output, "12:30");
        });
    });

    describe("formatTimeAMPM", function() {
        it ("return HH:MM{AM,PM}", function() {
            var template = Handlebars.compile("{{formatTimeAMPM '12:00:00'}}");
            var output = template();
            assert.equal(output, "12:00PM");
            template = Handlebars.compile("{{formatTimeAMPM '11:30:00'}}");
            output = template();
            assert.equal(output, "11:30AM");
        });
    });

    describe("toUrlSafe", function() {
        it ("replace spaces", function() {
            var template = Handlebars.compile("{{toUrlSafe ' '}}");
            var output = template();
            assert.equal(output, "%20");

            template = Handlebars.compile("{{toUrlSafe '_   _'}}");
            output = template();
            assert.equal(output, "_%20%20%20_");
        });
    });

    describe("toAnchorName", function() {
        it ("replace spaces with a hyphen", function() {
            template = Handlebars.compile("{{toAnchorName 'B BIO'}}");
            output = template();
            assert.equal(output, "B-BIO");
        });
    });

    describe("toLowerCase", function() {
        it ("replace unicode", function() {
            var template = Handlebars.compile("{{toLowerCase 'OK!'}}");
            var output = template();
            assert.equal(output, "ok!");

            template = Handlebars.compile("{{toLowerCase 'È'}}");
            output = template();
            assert.equal(output, "è");
        });
        it ("be ok with blank values", function() {
            var template = Handlebars.compile("{{toLowerCase ''}}");
            var output = template();
            assert.equal(output, "");
        });

    });

    describe("termNoYear", function() {
        it ("work on non-summer terms", function() {
            var template = Handlebars.compile("{{termNoYear '2013,spring' }}");
            var output = template();

            assert.equal(output, 'spring');
        });
        it ("work on summer terms", function() {
            var template = Handlebars.compile("{{termNoYear '2013,spring,b-term' }}");
            var output = template();

            assert.equal(output, 'spring b-term');
        });

    });

    describe('acal_banner_date_format', function() {
        it("give sunday (one date)", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-25'}}");
            var output = template();
            assert.equal(output, 'Jan 25 (Sunday)');
        });

        it("give sunday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-25' '2015-01-25' }}");
            var output = template();
            assert.equal(output, 'Jan 25 (Sunday)');
        });
        it("give monday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-26' '2015-01-26' }}");
            var output = template();
            assert.equal(output, 'Jan 26 (Monday)');
        });
        it("give tuesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-27' '2015-01-27' }}");
            var output = template();
            assert.equal(output, 'Jan 27 (Tuesday)');
        });
        it("give wednesday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-28' '2015-01-28' }}");
            var output = template();
            assert.equal(output, 'Jan 28 (Wednesday)');
        });
        it("give thursday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-29' '2015-01-29' }}");
            var output = template();
            assert.equal(output, 'Jan 29 (Thursday)');
        });
        it("give friday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-30' '2015-01-30' }}");
            var output = template();
            assert.equal(output, 'Jan 30 (Friday)');
        });
        it("give saturday", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-31' '2015-01-31' }}");
            var output = template();
            assert.equal(output, 'Jan 31 (Saturday)');
        });
        it("give Jan", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-01-01' '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1 (Thursday)');
        });
        it("give Feb", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-02-01' '2015-02-01' }}");
            var output = template();
            assert.equal(output, 'Feb 1 (Sunday)');
        });
        it("give Mar", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-03-01' '2015-03-01' }}");
            var output = template();
            assert.equal(output, 'Mar 1 (Sunday)');
        });
        it("give Apr", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-04-01' '2015-04-01' }}");
            var output = template();
            assert.equal(output, 'Apr 1 (Wednesday)');
        });
        it("give May", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-05-01' '2015-05-01' }}");
            var output = template();
            assert.equal(output, 'May 1 (Friday)');
        });
        it("give June", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-06-01' '2015-06-01' }}");
            var output = template();
            assert.equal(output, 'June 1 (Monday)');
        });
        it("give July", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-07-01' '2015-07-01' }}");
            var output = template();
            assert.equal(output, 'July 1 (Wednesday)');
        });
        it("give Aug", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-08-01' '2015-08-01' }}");
            var output = template();
            assert.equal(output, 'Aug 1 (Saturday)');
        });
        it("give Sept", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-09-01' '2015-09-01' }}");
            var output = template();
            assert.equal(output, 'Sept 1 (Tuesday)');
        });
        it("give Oct", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-10-01' '2015-10-01' }}");
            var output = template();
            assert.equal(output, 'Oct 1 (Thursday)');
        });
        it("give Nov", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-11-01' '2015-11-01' }}");
            var output = template();
            assert.equal(output, 'Nov 1 (Sunday)');
        });
        it("give Dec", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-12-01' '2015-12-01' }}");
            var output = template();
            assert.equal(output, 'Dec 1 (Tuesday)');
        });

        it("give in-month range", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-12-01' '2015-12-02' }}");
            var output = template();
            assert.equal(output, 'Dec 1 - 2');
        });

        it("give multi-month range", function() {
            var template = Handlebars.compile("{{acal_banner_date_format '2015-09-29' '2015-10-25' }}");
            var output = template();
            assert.equal(output, 'Sept 29 - Oct 25');
        });
    });

    describe('acal_page_date_format', function() {
        it("give Jan (one value)", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1');
        });

        it("give Jan", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-01-01' '2015-01-01' }}");
            var output = template();
            assert.equal(output, 'Jan 1');
        });
        it("give Feb", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-02-01' '2015-02-01' }}");
            var output = template();
            assert.equal(output, 'Feb 1');
        });
        it("give Mar", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-03-01' '2015-03-01' }}");
            var output = template();
            assert.equal(output, 'Mar 1');
        });
        it("give Apr", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-04-01' '2015-04-01' }}");
            var output = template();
            assert.equal(output, 'Apr 1');
        });
        it("give May", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-05-01' '2015-05-01' }}");
            var output = template();
            assert.equal(output, 'May 1');
        });
        it("give June", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-06-01' '2015-06-01' }}");
            var output = template();
            assert.equal(output, 'June 1');
        });
        it("give July", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-07-01' '2015-07-01' }}");
            var output = template();
            assert.equal(output, 'July 1');
        });
        it("give Aug", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-08-01' '2015-08-01' }}");
            var output = template();
            assert.equal(output, 'Aug 1');
        });
        it("give Sept", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-09-01' '2015-09-01' }}");
            var output = template();
            assert.equal(output, 'Sept 1');
        });
        it("give Oct", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-10-01' '2015-10-01' }}");
            var output = template();
            assert.equal(output, 'Oct 1');
        });
        it("give Nov", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-11-01' '2015-11-01' }}");
            var output = template();
            assert.equal(output, 'Nov 1');
        });
        it("give Dec", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-12-01' '2015-12-01' }}");
            var output = template();
            assert.equal(output, 'Dec 1');
        });

        it("give in-month range", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-12-01' '2015-12-02' }}");
            var output = template();
            assert.equal(output, 'Dec 1 - 2');
        });

        it("give multi-month range", function() {
            var template = Handlebars.compile("{{acal_page_date_format '2015-09-29' '2015-10-25' }}");
            var output = template();
            assert.equal(output, 'Sept 29 - Oct 25');
        });
    });

    describe('short-year', function() {
        it('work for an integer', function() {
            var template = Handlebars.compile("{{short_year 2013}}");
            var output = template();

            assert.equal(output, '’13');
        });
        it('work for a string', function() {
            var template = Handlebars.compile("{{short_year '2017'}}");
            var output = template();

            assert.equal(output, '’17');
        });

    });

    describe("titleCaseName", function() {
        it ("all upper case", function() {
            var template = Handlebars.compile("{{titleCaseName 'JAMES AVERAGE STAFF'}}");
            var output = template();
            assert.equal(output, "James Average Staff");
        });
    });

    describe("toTitleCase", function() {
        it ("summer term", function() {
            var template = Handlebars.compile("{{toTitleCase 'summer a-term'}}");
            var output = template();
            assert.equal(output, "Summer A-Term");

            template = Handlebars.compile("{{toTitleCase 'summer b-term'}}");
            output = template();
            assert.equal(output, "Summer B-Term");

            template = Handlebars.compile("{{toTitleCase 'summer,2013,a-term'}}");
            output = template();
            assert.equal(output, "Summer 2013 A-Term");

            template = Handlebars.compile("{{toTitleCase '2013 summer, a-term'}}");
            output = template();
            assert.equal(output, "2013 Summer A-Term");
        });
        it ("non-summer term", function() {
            template = Handlebars.compile("{{toTitleCase 'winter, 2013'}}");
            output = template();
            assert.equal(output, "Winter 2013");

            template = Handlebars.compile("{{toTitleCase 'spring'}}");
            output = template();
            assert.equal(output, "Spring");

        });
    });

    describe("titleFormatTerm", function() {
        it ("summer term", function() {
            var template = Handlebars.compile("{{titleFormatTerm '2013,summer,a-term'}}");
            var output = template();
            assert.equal(output, "Summer 2013 A-Term");
        });
        it ("non-summer term", function() {
            template = Handlebars.compile("{{titleFormatTerm '2013,winter'}}");
            output = template();
            assert.equal(output, "Winter 2013");
        });
    });

    describe("ucfirst", function() {
        it ("a section type", function() {
            var template = Handlebars.compile("{{ucfirst 'QUIZ'}}");
            var output = template();
            assert.equal(output, "Quiz");
        });
        it ("a quarter", function() {
            template = Handlebars.compile("{{ucfirst 'summer'}}");
            output = template();
            assert.equal(output, "Summer");
        });
    });

    describe('formatPrice', function(){
        it('normal amount', function(){
            var template = Handlebars.compile("{{formatPrice '125.34'}}");
            var output = template();
            assert.equal(output, 125.34);
        });
        it ("integer", function() {
            var template = Handlebars.compile("{{formatPrice '10'}}");
            var output = template();
            assert.equal(output, 10.00);
        });
        it ("zero", function() {
            var template = Handlebars.compile("{{formatPrice '0'}}");
            var output = template();
            assert.equal(output, 0.00);
        });
    });

    describe('format_schedule_hour', function(){
        it('am', function(){
            var template = Handlebars.compile("{{format_schedule_hour '08' 0}}");
            var output = template();
            assert.equal(output, '08a');
        });
        it ("pm", function() {
            /* ReferenceError: VisualSchedule is not defined
            var template = Handlebars.compile("{{format_schedule_hour '12' 0}}");
            var output = template();
            assert.equal(output, '12p');
            */
            var template = Handlebars.compile("{{format_schedule_hour '13' 0}}");
            var output = template();
            assert.equal(output, '1p');
            var template = Handlebars.compile("{{format_schedule_hour '22' 0}}");
            var output = template();
            assert.equal(output, '10p');
        });
    });

    describe('pluralize', function(){
        it('plural', function(){
            var template = Handlebars.compile("{{pluralize 2 'day' 'days'}}");
            var output = template();
            assert.equal(output, 'days');
        });
        it('singular', function(){
            var template = Handlebars.compile("{{pluralize 1 'hold' 'holds'}}");
            var output = template();
            assert.equal(output, 'hold');
        });
    });

    describe('pluralize_by_size', function(){
        it('plural', function(){
            var alist = ["A", "B"];
            var raw = "{{pluralize_by_size '" + alist + "' 'Major' 'Majors'}}";
            var template = Handlebars.compile(raw);
            var output = template();
            assert.equal(output, 'Majors');
        });
        it('singular', function(){
            var alist = ['A'];
            var raw = "{{pluralize_by_size '" + alist + "' 'Major' 'Majors'}}";
            var template = Handlebars.compile(raw);
            var output = template();
            assert.equal(output, 'Major');
        });
    });

    describe('get_quarter_code', function(){
        it('each quarter', function(){
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
        it('empty input', function(){
            var template = Handlebars.compile("{{get_quarter_code ''}}");
            var output = template();
            assert.equal(output, '');
            var template = Handlebars.compile("{{get_quarter_code undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe('get_quarter_abbreviation', function(){
        it('each quarter', function(){
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
        it('empty input param', function(){
            var template = Handlebars.compile("{{get_quarter_abbreviation ''}}");
            var output = template();
            assert.equal(output, '');
        });
        it('undefined param', function(){
            var template = Handlebars.compile("{{get_quarter_abbreviation undefined}}");
            var output = template();
            assert.equal(output, '');
        });
    });

    describe('slugify', function(){
        it('replace consecutive spaces with -', function(){
            var template = Handlebars.compile("{{slugify '2013 Summer ASE 510 A'}}");
            var output = template();
            assert.equal(output, '2013-summer-ase-510-a');
        });
    });

    describe('shorten_meeting_type', function(){
        it('truncate after the third char', function(){
            var template = Handlebars.compile("{{shorten_meeting_type 'LECTURE'}}");
            var output = template();
            assert.equal(output, 'LEC');
        });
    });

    describe('formatDateAsFinalsDay', function(){
        it('get finals month + day number', function(){
            var template = Handlebars.compile("{{formatDateAsFinalsDay '2013-03-04 13:30'}}");
            var output = template();
            assert.equal(output, 'Mar 4');
        });
    });

    describe('if_mobile', function(){
        var template = Handlebars.compile("{{#if_mobile}}Is mobile{{else}}Is not mobile{{/if_mobile}}");
        var output = template();
        assert.equal(output, 'Is not mobile');
    });

    describe('protocol', function(){
        var template = Handlebars.compile("{{protocol 'test.edu/img/test.png'}}");
        var output = template();
        assert.equal(output, 'about://test.edu/img/test.png');
    });

    describe('static', function(){
        var template = Handlebars.compile("{{static '/img/test.png'}}");
        var output = template();
        assert.equal(output, 'http://static/path/img/test.png');
    });
});
