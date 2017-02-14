PhotoClassList = require("../teaching/class_list.js").PhotoClassList;
var assert = require("assert");

describe("PhotoClassList", function() {
    describe('download name', function() {
        it('should escape spaces', function() {
            var section = {};
            section.curriculum_abbr = 'TEST IT';
            section.section_id = 'A1';

            var name = PhotoClassList.download_name(section);
            assert.equal(name, 'TEST_IT_A1_students.csv');
        });
    });
});

