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
});
