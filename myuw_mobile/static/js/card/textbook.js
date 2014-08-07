var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,
    term: undefined,
    missing_book_error: false,

    render_init: function() {
        var term =  (TextbookCard.term === undefined) ? 'current' : TextbookCard.term;
        WSData.fetch_book_data(term, TextbookCard.render_upon_data, TextbookCard.textbook_error);
        WSData.fetch_course_data_for_term(term, TextbookCard.render_upon_data, TextbookCard.textbook_error);
        // may need to add a missing_course_error
    },


    _has_all_data: function () {
        return (WSData.book_data(TextbookCard.term) && WSData.course_data_for_term(TextbookCard.term));
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
        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        TextbookCard.dom_target.html(template({'no_books': true,
                                               'term': TextbookCard.term}
                                             ));
    },

    _render: function () {
        var term = TextbookCard.term;
        var textbook_data  = TextBooks.process_book_data(WSData.book_data(term), WSData.course_data_for_term(term));

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

        var template_data = {"term": term,
                             "sections": section_book_data}

        var source = $("#textbook_card").html();
        var template = Handlebars.compile(source);
        TextbookCard.dom_target.html(template(template_data));

        $(".show_textbooks").on("click", function(ev) {
            WSData.log_interaction("card_view_future_textbooks", term);
            var hist = window.History;
            hist.pushState({
                state: "textbooks",
                term: term
            },  "", "/mobile/textbooks/"+term);
            return false;
        });

    }

};

