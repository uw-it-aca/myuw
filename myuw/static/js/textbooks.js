var TextBooks = {
    term: undefined,

    show_books: function(term, textbook) {
        //Navbar.render_navbar("nav-sub");
        TextBooks.term = term;
        showLoading();
        CommonLoading.render_init();
        var requirements = {
            books: new BookData(term),
            course_data: new CourseData(term)
        };

        if (myuwFeatureEnabled('instructor_schedule')) {
            requirements.instructed_course_data = new InstructedCourseData(term);
        }

        WebServiceData.require(requirements, TextBooks.render_books);
    },

    render_error: function(book_error, course_error, instructed_course_error) {
        var book_err_status = book_error ? book_error.status : null;
        var course_err_status = course_error ? course_error.status : null;
        var instructed_course_err_status = instructed_course_error ? instructed_course_error.status : null;

        if (book_err_status === 543 || course_err_status === 543 || instructed_course_err_status === 543) {
            var raw = CardWithError.render("Textbooks");
            $("#main-content").html(raw);
            return true;
        }

        return false;
    },

    process_book_data: function(book_data, course_data, instructed_course_data) {
        var template_data = {
            "teaching_sections": [],
            "enrolled_sections": [],
            "sections": [],
            "quarter": course_data ? course_data.quarter : instructed_course_data.quarter,
            "year": course_data ? course_data.year: instructed_course_data.year,
            "summer_term": course_data ? course_data.summer_term : instructed_course_data.summer_term
        };

        var section_data = function (i, section, instructor) {
            return {
                index: i,
                section_title: section.course_title,
                curriculum: section.curriculum_abbr,
                course_number: section.course_number,
                section_id: section.section_id,
                color_id: section.color_id,
                sln: section.sln,
                books: book_data ? book_data[section.sln] : [],
                has_books: (book_data &&
                            (section.sln in book_data) &&
                            book_data[section.sln].length > 0),
                is_instructor: instructor,
                bothell_campus: section.course_campus.toLowerCase() === 'bothell',
                tacoma_campus: section.course_campus.toLowerCase() === 'tacoma'
            };
        };

        if (course_data) {
            $.each(course_data.sections, function (index) {
                var section = section_data(index, this, false);
                template_data.enrolled_sections.push(section);
                template_data.sections.push(section);
            });
        }

        if (myuwFeatureEnabled('instructor_textbooks') && instructed_course_data) {
            $.each(instructed_course_data.sections, function (index) {
                var section = section_data(index, this, true);
                template_data.teaching_sections.push(section);
                template_data.sections.push(section);
            });
        }

        // Determine if we need to collapse the textbook sections and whether the user is teaching
        var num_sections = template_data.enrolled_sections.length + template_data.teaching_sections.length;
        template_data.collapse_sections = num_sections > 10;
        template_data.is_teaching = template_data.teaching_sections.length > 0;

        template_data.verba_link = book_data ? book_data.verba_link : null;
        return template_data;
    },

    render_books: function(resources) {
        var book_resource = resources.books;
        var course_resource = resources.course_data;
        var instructed_course_resource = resources.instructed_course_data;

        if (TextBooks.render_error(book_resource.error,
                                   course_resource.error,
                                   instructed_course_resource.error)) {
            return;
        }

        var term = TextBooks.term;
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#textbooks").html();
        var template = Handlebars.compile(source);
        var template_data = TextBooks.process_book_data(book_resource.data,
                                                        course_resource.data,
                                                        instructed_course_resource.data);
        if (template_data !== undefined){
            $("#main-content").html(template(template_data));
        }

        // Scroll to correct section
        element = $("a[name='" + location.hash.substring(1) + "']");
        if (element.length > 0) {
                $('html, body').animate({
                scrollTop: element.offset().top
            });
        }
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TextBooks = TextBooks;
