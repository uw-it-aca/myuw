var assert = require("assert");
PhotoClassList = require("../teaching/class_list.js").PhotoClassList;

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

    describe('multiple majors', function() {
        it('should just comma separate them', function() {
            assert.equal(PhotoClassList.combine_majors([{ full_name: 'major1' },
                                                        { full_name: 'another major'},
                                                        { full_name: 'a major, but with commas' }]),
                         "major1, another major, a major, but with commas");
            assert.equal(PhotoClassList.combine_majors([{ full_name: 'major1' }]), "major1");
            assert.equal(PhotoClassList.combine_majors([]), "");
            assert.equal(PhotoClassList.combine_majors(), "");
        });
    });

    describe('sort students', function() {
        it('should put registration records into right order', function() {
            var data = [{"surname": "Student2",
                         "credits": "2.0",
                         "class": "FRESHMAN",
                         "first_name": "Jane",
                         "netid": "javg003",
                         "class_code": 1,
                         "email": "javg003@uw.edu"},
                        {"surname": "Student2",
                         "credits": "2.0",
                         "class": "JUNIOR",
                         "first_name": "Jade",
                         "netid": "javg002",
                         "class_code": 3,
                         "email": "javg002@uw.edu"},
                        {"surname": "Student1",
                         "credits": "2.0",
                         "class": "SOPHOMORE",
                         "first_name": "Jake",
                         "netid": "javg001",
                         "class_code": 2,
                         "email": "javg001@uw.edu"}];
            var sorted = PhotoClassList.sort_registrations(data, 'surname');
            assert.equal(sorted[0].surname, "Student1");
            assert.equal(sorted[1].surname, "Student2");
            assert.equal(sorted[2].surname, "Student2");
            var sorted = PhotoClassList.sort_last(data);
            assert.equal(sorted[0].surname, "Student1");
            assert.equal(sorted[1].surname, "Student2");
            assert.equal(sorted[1].first_name, "Jade");
            assert.equal(sorted[2].surname, "Student2");
            assert.equal(sorted[2].first_name, "Jane");
            var sorted = PhotoClassList.sort_registrations(data, 'class_code');
            assert.equal(sorted[0].class, "FRESHMAN");
            assert.equal(sorted[1].class, "SOPHOMORE");
            assert.equal(sorted[2].class, "JUNIOR");
        });
    });

    describe('build download csv', function() {
        it('should put data in right fields', function() {
            var data = {
              "has_linked_sections": true,
              "registrations": [{"surname": "Student3",
                                 "first_name": "June",
                                 "credits": "2.0",
                                 "full_name": "June Average Student",
                                 "regid": "9136CCB8F66711D5BE060004AC494003",
                                 "student_number": "1033003",
                                 "url_key": "9136CCB8F66711D5BE060004AC494003",
                                 "class_level": "FRESHMAN",
                                 "majors": [{"degree_name": null,
                                             "short_name": "B PRE",
                                             "name": "TRAIN",
                                             "full_name": "Premajor (Bothell Campus)",
                                             "college_abbr": "",
                                             "degree_abbr": "TRAIN",
                                             "degree_level": 0,
                                             "college_full_name": "",
                                             "campus": "Bothell"}],
                                 "name": "Jane",
                                 "netid": "javg003",
                                 "linked_sections": "",
                                 "class_code": 1,
                                 "email": "javg003@uw.edu"},
                                {"surname": "Student2",
                                 "first_name": "Jade",
                                 "credits": "2.0",
                                 "full_name": "Jade Average Student",
                                 "regid": "9136CCB8F66711D5BE060004AC494002",
                                 "student_number": "1033002",
                                 "url_key": "9136CCB8F66711D5BE060004AC494002",
                                 "class_level": "JUNIOR",
                                 "majors": [{"degree_name": null,
                                             "short_name": "B PRE",
                                             "name": "TRAIN",
                                             "full_name": "Premajor (Bothell Campus)",
                                             "college_abbr": "",
                                             "degree_abbr": "TRAIN",
                                             "degree_level": 0,
                                             "college_full_name": "",
                                             "campus": "Bothell"}],
                                 "name": "Jade",
                                 "netid": "javg002",
                                 "linked_sections": "",
                                 "class_code": 3,
                                 "email": "javg002@uw.edu"},
                                {"surname": "Student1",
                                 "first_name": "Jake",
                                 "credits": "2.0",
                                 "full_name": "Jake Average Student",
                                 "regid": "9136CCB8F66711D5BE060004AC494001",
                                 "student_number": "1033001",
                                 "url_key": "9136CCB8F66711D5BE060004AC494001",
                                 "class_level": "SOPHOMORE",
                                 "majors": [{"degree_name": "ASD",
                                             "short_name": "UPCOM",
                                             "name": "UPCOM",
                                             "full_name": "UPCOM (Tacoma Campus)",
                                             "college_abbr": "",
                                             "degree_abbr": "UPCOM",
                                             "degree_level": 2,
                                             "college_full_name": "",
                                             "campus": "Tacoma"}],
                                 "name": "Jake",
                                 "netid": "javg001",
                                 "linked_sections": "A1 AQ",
                                 "class_code": 2,
                                 "email": "javg001@uw.edu"}],
                };
            var result = PhotoClassList.build_download(data);
            var lines = result.split("\n");
            // Header...
            assert.equal(lines[0],
                         'StudentNo,UWNetID,LastName,FirstName,Pronouns,Section,Credits,Class,Major,Email');
            var row1 = lines[1].split(",");
            assert.equal(row1[0], '"\t1033001"');
            assert.equal(row1[1], '"javg001"');
            assert.equal(row1[2], '"Student1"');
            assert.equal(row1[3], '"Jake"');
            assert.equal(row1[4], '"A1 AQ"');
            assert.equal(row1[5], '"2.0"');
            assert.equal(row1[6], '"SOPHOMORE"');
            assert.equal(row1[7], '"UPCOM (Tacoma Campus)"');
            assert.equal(row1[8], '"javg001@uw.edu"');

            var row2 = lines[2].split(",");
            assert.equal(row2[2], '"Student2"');
            var row3 = lines[3].split(",");
            assert.equal(row3[2], '"Student3"');
        });
    });

});
