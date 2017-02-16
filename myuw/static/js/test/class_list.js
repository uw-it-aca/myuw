PhotoClassList = require("../teaching/class_list.js").PhotoClassList;
var assert = require("assert");

describe("PhotoClassList", function() {
    describe('download name', function() {
        it('should escape spaces', function() {
            var section = {};
            section.curriculum_abbr = 'TEST IT';
            section.section_id = 'A1';
            section.course_number = '101';

            var name = PhotoClassList.download_name(section, 2012, 'winter');
            assert.equal(name, 'TEST_IT_101_A1_winter_2012_students.csv');
        });
    });
    describe('quoting fields', function() {
        it('should put fields in quotes, and escape double quotes', function() {
            assert.equal('"value, ok"', PhotoClassList.quote_field('value, ok'));
            assert.equal('"value\\\", \\\"ok"', PhotoClassList.quote_field('value", "ok'));
        });
    });

    describe('build download', function() {
        it('should put data in the right fields', function() {
            var data = {};
            data.registrations = [];
            data.registrations.push({student_number: '1234',
                                     netid: 'testing',
                                     full_name: 'preferred name',
                                     name: 'preferred',
                                     surname: 'name',
                                     credits: '2.0',
                                     class: 'JUNIOR',
                                     majors: [{full_name: 'my major' }],
                                     email: 'testing@uw.edu'
                                     });

            var result = PhotoClassList.build_download(data);

            var lines = result.split("\n");
            // Header...
            assert.equal(lines[0], 'Student Number,UW NetID,Name,Last Name,Quiz Section,Credits,Class,Majors,Email');

            var row1 = lines[1].split(",");
            assert.equal(row1[0], '"1234"');
            assert.equal(row1[1], '"testing"');
            assert.equal(row1[2], '"preferred"');
            assert.equal(row1[3], '"name"');
            assert.equal(row1[5], '"2.0"');
            assert.equal(row1[6], '"JUNIOR"');
            assert.equal(row1[7], '"my major"');
            assert.equal(row1[8], '"testing@uw.edu"');
        });
    });

    describe('multiple majors', function() {
        it('should just comma separate them', function() {
            assert.equal(PhotoClassList.combine_majors([{ full_name: 'major1' }, { full_name: 'another major'}, { full_name: 'a major, but with commas' }]), "major1, another major, a major, but with commas");
            assert.equal(PhotoClassList.combine_majors([{ full_name: 'major1' }]), "major1");
            assert.equal(PhotoClassList.combine_majors([]), "");
            assert.equal(PhotoClassList.combine_majors(), "");
        });
    });
});

