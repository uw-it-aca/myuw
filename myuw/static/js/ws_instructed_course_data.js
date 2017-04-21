function InstructedCourseData(term) {
    this.url = "/api/v1/instructor_schedule/"+term;
    this.data = null;
    this.error = null;
}

InstructedCourseData.prototype.setData = function(data) {
    // MUWM-549 and MUWM-552
    var sections = data.sections;
    var section_count = sections.length;
    for (var index = 0; index < section_count; index++) {
        section = sections[index];

        var canvas_url = section.canvas_url;
        if (canvas_url) {
            if (section.class_website_url == canvas_url) {
                section.class_website_url = null;
            }
            var matches = canvas_url.match(/\/([0-9]+)$/);
            var canvas_id = matches[1];
            var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

            if (section.class_website_url == alternate_url) {
                section.class_website_url = null;
            }
        }
    }

    this.data = data;
};

InstructedCourseData.prototype.normalized = function(term) {
    var course_data = this.data;

    WebServiceData.normalize_instructors(course_data);
    $.each(course_data.related_terms, function () {
        this.is_current = (window.term.year == this.year &&
                           window.term.quarter.toLowerCase() == this.quarter.toLowerCase());
        this.matching_term = (course_data.year == this.year &&
                              course_data.quarter.toLowerCase() == this.quarter.toLowerCase());
    });

    var grading_is_open = course_data.grading_period_is_open;
    var grading_is_closed = course_data.grading_period_is_past;
    var grading_open = moment(new Date(course_data.term.grading_period_open));
    var grading_aterm_open = moment(new Date(course_data.term.aterm_grading_period_open));
    var grading_deadline = moment(new Date(course_data.term.grade_submission_deadline));
    var ref = moment();
    // search param supports testing
    if (window.location.search.length) {
        match = window.location.search.match(/\?grading_date=(.+)$/);
        if (match) {
            ref = moment(new Date(decodeURI(match[1])));
            grading_is_closed = grading_deadline.isBefore(ref);
            grading_is_open = (!grading_is_closed && grading_open.isBefore(ref));
        }
    }

    var grading_open_relative = grading_open.from(ref);
    var grading_aterm_open_relative = grading_aterm_open.from(ref);
    var grading_deadline_relative = grading_deadline.from(ref);
    var grading_open_date;
    var grading_deadline_date;

    var fmt = 'MMM D [at] h:mm A';
    var month_to_day_shift = 5;
    if (Math.abs(grading_open.diff(ref, 'days')) > month_to_day_shift) {
        grading_open_date = grading_open.format(fmt) + ' PST';
    } else {
        grading_open_date = grading_open.calendar(ref);
    }

    if (Math.abs(grading_deadline.diff(ref, 'days')) > month_to_day_shift) {
        grading_deadline_date = grading_deadline.format(fmt) + ' PST';
    } else {
        grading_deadline_date = grading_deadline.calendar(ref);
    }

    var minutes_till_open = grading_open.diff(ref, 'minutes');
    var opens_in_24_hours = (minutes_till_open >= 0 &&
                             minutes_till_open <= (24 * 60));

    var minutes_till_deadline = grading_deadline.diff(ref, 'minutes');
    var deadline_in_24_hours = (minutes_till_deadline >= 0 &&
                                minutes_till_deadline <= (24 * 60));

    $.each(course_data.sections, function (iii) {
        var section = this;
        var course_campus = section.course_campus.toLowerCase();
        section.is_seattle = (course_campus === 'seattle');
        section.is_bothell = (course_campus === 'bothell');
        section.is_tacoma =  (course_campus === 'tacoma');

        section.section_label = course_data.term.year + '-' +
            course_data.term.quarter.toLowerCase() + '-' +
            section.curriculum_abbr + '-' +
            section.course_number + '-' +
            section.section_id;

        section.grading_period_is_open = grading_is_open;
        section.grading_period_is_past = grading_is_closed;
        section.opens_in_24_hours = opens_in_24_hours;
        section.deadline_in_24_hours = deadline_in_24_hours;
        section.grading_period_open_date = grading_open_date;
        section.grading_period_relative_open = grading_open_relative;
        section.aterm_grading_period_relative_open = grading_aterm_open_relative;
        section.grade_submission_deadline_date = grading_deadline_date;
        section.grade_submission_relative_deadline = grading_deadline_relative;

        section.grading_status.all_grades_submitted =
            (section.grading_status.hasOwnProperty('submitted_count') &&
             section.grading_status.hasOwnProperty('unsubmitted_count') &&
             section.grading_status.unsubmitted_count === 0);
        if (section.grading_status.submitted_date) {
            var submitted = moment(new Date(section.grading_status.submitted_date));
            if (Math.abs(submitted.diff(ref, 'days')) > month_to_day_shift) {
                section.grading_status.submitted_relative_date = submitted.format(fmt) + ' PST';
            } else {
                section.grading_status.submitted_relative_date = submitted.calendar(ref);
            }
        }

        section.grade_submission_section_delegate = false;
        $.each(section.grade_submission_delegates, function () {
            if (this.level.toLowerCase() === 'section') {
                section.grade_submission_section_delegate = true;
                return false;
            }
        });
    });

    return course_data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.InstructedCourseData = InstructedCourseData;
