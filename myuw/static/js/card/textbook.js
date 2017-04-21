var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,
    term: undefined,

    render_init: function() {
        TextbookCard.dom_target = $('#TextbookCard');
        if (!window.user.student) {
            TextbookCard.dom_target.hide();
        }
        if (TextbookCard.term === 'current') {
            if (!window.card_display_dates.is_before_eof_7days_of_term) {
                $("#TextbookCard").hide();
                return;
            }
        }

        var resources = {
            book_data: new BookData(TextbookCard.term),
            course_data: new CourseData(TextbookCard.term)
        };

        WebServiceData(resources, TextBookCard.render);
    },

    render_error: function(book_data_error, course_data_error) {
        var book_error_code = book_error_code ? book_data_error.status : null;
        var course_error_code = course_data_error ? course_data_error.status: null;
        if (course_error_code === 404 || book_error_code === 404) {
            $("#TextbookCard").hide();
            return true;
        } else if (book_error_code || course_data_error) {
            TextbookCard.dom_target.html(CardWithError.render("Textbooks"));
            return true;
        }

        return false;
    },

    render: function (resources) {
        // _render should be called only once.
        if (renderedCardOnce(TextbookCard.name)) {
            return;
        }
        var textbook_data_resource = resources.book_data;
        var course_data_resource = resources.course_data;

        if (TextbookCard.render_error(textbook_data_resource.error, course_data_resource.error)) {
            return;
        }

        var term = TextbookCard.term;
        var course_data = course_data_resource.data;
        var textbook_data  = TextBooks.process_book_data(textbook_data_resource.data, course_data);
        var no_book_assigned = true;
        var section_book_data = [];

        $.each(textbook_data.sections, function (sec_idx, section) {
            var required = 0;
            var optional = 0;
            if (section.books) {
                $.each(section.books, function (book_idx, book, section) {
                    if (book.is_required) {
                        required += 1;
                    } else {
                        optional += 1;
                    }
                    if (no_book_assigned) {
                        no_book_assigned = false;
                    }
                });
            }
            var course_id = section.curriculum + " " + section.course_number + " " + section.section_id;

            var section_data = {"course_id": course_id,
                                "color_id": section.color_id,
                                "required": required,
                                "total": required + optional,
                                "no_course_books": (required + optional) ? false :true
                               };
            section_book_data.push(section_data);
        });

        var template_data = {"term": term,
                             "no_book_assigned": no_book_assigned,
                             "quarter": course_data.quarter,
                             "year": course_data.year,
                             "summer_term": course_data.summer_term,
                             "sections": section_book_data};

        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        var raw = template(template_data);
        TextbookCard.dom_target.html(raw);
        LogUtils.cardLoaded(TextbookCard.name, TextbookCard.dom_target);
        TextbookCard.add_events(term);
    },

    add_events: function(term) {
        $("#show_term_textbooks").on("click", function(ev) {
            WSData.log_interaction("card_view_future_textbooks", term);
            var hist = window.History;
            hist.pushState({
                state: "textbooks",
                term: term
            },  "", "/textbooks/"+term);
        });
    }

};
