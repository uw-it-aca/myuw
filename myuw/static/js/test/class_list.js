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
    describe('quoting fields', function() {
        assert.equal('"value, ok"', PhotoClassList.quote_field('value, ok'));
        assert.equal('"value\\\", \\\"ok"', PhotoClassList.quote_field('value", "ok'));
    });

    describe('build download', function() {
        var data = {};
        data.registrations = [];
        data.registrations.push({student_number: '1234',
                                 netid: 'testing',
                                 full_name: 'preferred name',
                                 });

        var result = PhotoClassList.build_download(data);

        var lines = result.split("\n");
        // Header...
        assert.equal(lines[0], 'Student Number,UW NetID,Name,Quiz Section,Credits,Class,Major,Email');

        var row1 = lines[1].split(",");
        assert.equal(row1[0], '"1234"');
        assert.equal(row1[1], '"testing"');
        assert.equal(row1[2], '"preferred name"');
    });
});

