var TextBooks = {
    term: undefined,
    anchor_textbook: undefined,

    show_books: function(term, textbook) {
        //Navbar.render_navbar("nav-sub");
        TextBooks.term = term;
        TextBooks.anchor_textbook = textbook;
        showLoading();
        CommonLoading.render_init();
        WSData.fetch_book_data(term, TextBooks.render_books, TextBooks.render_error);
        WSData.fetch_course_data_for_term(TextBooks.term, TextBooks.render_books, TextBooks.render_error);
        WSData.fetch_instructed_course_data_for_term(TextBooks.term, TextBooks.render_books, TextBooks.render_error);
    },

    render_error: function() {
        var book_err_status = WSData.book_data_error_code(TextBooks.term);
        var course_err_status = WSData.course_data_error_code(TextBooks.term);
        var instructed_course_err_status = WSData.instructed_course_data_error_code(TextBooks.term);

        if (book_err_status === 543 || course_err_status === 543 || instructed_course_err_status === 543) {
            var raw = CardWithError.render("Textbooks");
            $("#main-content").html(raw);
        }
    },

    process_book_data: function(book_data, course_data, instructed_course_data) {
        if (!book_data) {
            // If we had an error loading bookstore content
            return;
        }
        var template_data = {
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
                books: book_data[section.sln],
                is_instructor: instructor,
                bothell_campus: section.course_campus.toLowerCase() === 'bothell',
                tacoma_campus: section.course_campus.toLowerCase() === 'tacoma'
            };
        };

        if (course_data) {
            $.each(course_data.sections, function (index) {
                template_data.sections.push(section_data(index, this, false));
            });
        }

        if (myuwFeatureEnabled('instructor_textbooks') && instructed_course_data) {
            $.each(instructed_course_data.sections, function (index) {
                template_data.sections.push(section_data(index, this, true));
            });
        }

        template_data.verba_link = book_data.verba_link;
        return template_data;
    },

    _has_all_data: function () {
        var book_data = WSData.book_data(TextBooks.term);
        var course_data = WSData.course_data_for_term(TextBooks.term);
        var instructed_course_data = WSData.instructed_course_data_for_term(TextBooks.term);
        var course_err_status = WSData.course_data_error_code(TextBooks.term);
        var instructed_course_err_status = WSData.instructed_course_data_error_code(TextBooks.term);

        return (book_data &&
                (course_data ||
                 (course_data === undefined && course_err_status === 404)) &&
                (instructed_course_data || 
                 (instructed_course_data === undefined && instructed_course_err_status === 404)));
    },

    render_books: function() {
        if(!TextBooks._has_all_data()){
            return;
        }
        var term = TextBooks.term;
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#textbooks").html();
        var template = Handlebars.compile(source);
        var template_data = TextBooks.process_book_data(WSData.book_data(term),
                                                        WSData.course_data_for_term(term),
                                                        WSData.instructed_course_data_for_term(term));
        if (template_data !== undefined){
            $("#main-content").html(template(template_data));
        }


        // Scroll to correct section
        element = $("a[name='" + TextBooks.anchor_textbook + "']");
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
