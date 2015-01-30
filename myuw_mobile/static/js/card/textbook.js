var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,
    term: undefined,
    missing_book_error: false,

    render_init: function() {
        var term =  (TextbookCard.term === undefined) ? 'current' : TextbookCard.term;
        WSData.fetch_book_data(term, TextbookCard.render_upon_data, TextbookCard.textbook_error);
        WSData.fetch_course_data_for_term(term, TextbookCard.render_upon_data, TextbookCard._render_error);
        // may need to add a missing_course_error
    },


    _has_all_data: function () {
        return (WSData.book_data(TextbookCard.term) && WSData.course_data_for_term(TextbookCard.term));
    },

    render_upon_data: function(args) {
        //If more than one data source, multiple callbacks point to this function
        //Delay rendering until all requests are complete
        //Do something smart about not showing error if AJAX is pending
        if (!TextbookCard._has_all_data()) {
            return;
        }
        TextbookCard._render();
    },

    textbook_error: function() {
        TextbookCard.missing_book_error = true;
        TextbookCard._render_error();
    },

    _render_error: function() {
        if (TextbookCard.missing_book_error) {
        }
        else {
            var source = $("#textbook_card").html();
            var template = Handlebars.compile(source);
            TextbookCard.dom_target.html(template({'no_books': true,
                                               'term': TextbookCard.term}
                                             ));
        }
    },

    _render: function () {
        var term = TextbookCard.term;
        var course_data = WSData.course_data_for_term(term);
        var registered = true;
        var section_book_data = [];
        if (course_data.sections.length === 0) {
            registered = false;
        } else {
            var textbook_data  = TextBooks.process_book_data(WSData.book_data(term), course_data);
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
                                    "total": required + optional,
                                    "no_course_books": (required + optional) ? false :true
                                   };
                section_book_data.push(section_data);
            });
        }
        var template_data = {"registered": registered,
                             "term": term,
                             "sections": section_book_data};

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

