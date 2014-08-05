var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,
    term: undefined,
    missing_book_error: false,

    render_init: function() {
        var term =  (TextbookCard.term === undefined) ? 'current' : TextbookCard.term;
        WSData.fetch_book_data(TextbookCard.render_upon_data, term, TextbookCard.textbook_error);
        WSData.fetch_course_data_for_term(term, TextbookCard.render_upon_data);
    },

    render_upon_data: function(args) {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!TextbookCard.missing_book_error && !TextbookCard._has_all_data()) {
            TextbookCard.dom_target.html(CardWithError.render());
            return;
        }
        if (TextbookCard.missing_book_error) {
            TextbookCard._render_error();
        } else {
            TextbookCard._render();
        }

    },

    textbook_error: function() {
        TextbookCard.missing_book_error = true;
    },

    _render_error: function() {
        var term_data = WSData.course_data_for_term(TextbookCard.term);
        var term_title = term_data.quarter;
        if (term_data.summer_term !== "") {
            term_title += " " + term_data.summer_term;
        }
        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        TextbookCard.dom_target.html(template({'no_books': true,
                                               'term': term_title}));
    },

    _render: function () {
        var textbook_data  = TextBooks.process_book_data(WSData.book_data(), WSData.course_data_for_term(TextbookCard.term));

        var term_title = textbook_data.quarter;
        if (textbook_data.summer_term !== "") {
            term_title += " " + textbook_data.summer_term;
        }
        var url = "/mobile/textbooks/" + TextbookCard.term;
        var section_book_data = [];
        $.each(textbook_data.sections, function (sec_idx, section) {
            var required = 0;
            var optional = 0;
            $.each(section.books, function (book_idx, book, section) {
                if (book.is_required) {
                    required += 1;
                } else {
                    optional += 1;
                }
            });
            var course_id = section.curriculum + " " + section.course_number + " " + section.section_id;

            var section_data = {"course_id": course_id,
                                "required": required,
                                "optional": optional
            };
            section_book_data.push(section_data);
        });
        var template_data = {"page_url": url,
                             "term": term_title,
                             "sections": section_book_data}

        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        TextbookCard.dom_target.html(template(template_data));
    },

    _has_all_data: function () {
        if (WSData.book_data() && WSData.course_data_for_term(TextbookCard.term)) {
            return true;
        }
        return false;
    }

};

