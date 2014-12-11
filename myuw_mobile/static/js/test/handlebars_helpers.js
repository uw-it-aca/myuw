Handlebars = require("../vendor/handlebars-v2.0.0.js");
require("../handlebars-helpers.js");

var assert = require("assert")
describe('Handlebar-helpers', function(){
  describe('phonenumber', function(){
    it('should replace 10 digits with a formatted phone number', function(){
        var template = Handlebars.compile("{{formatPhoneNumber '5035551234'}}");
        var output = template();
        assert.equal(output, "503-555-1234");
    })
  })
});
