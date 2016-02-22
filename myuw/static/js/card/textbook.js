var TextbookCard = {
    name: 'TextbookCard',
    dom_target: undefined,
    term: undefined,
    _ajax_count: 0,

    render_init: function() {
        if (!window.user.student) {
            $("#TextbookCard").hide();
        }
        if (TextbookCard.term === 'current') {
            if (!window.card_display_dates.is_before_eof_7days_of_term) {
                $("#TextbookCard").hide();
                return;
            }
        }
        TextbookCard._ajax_count = 2;
        WSData.fetch_book_data(TextbookCard.term, TextbookCard.render_upon_data, TextbookCard.render_error);
        WSData.fetch_course_data_for_term(TextbookCard.term, TextbookCard.render_upon_data, TextbookCard.render_error);
    },

    _has_all_data: function () {
        return (WSData.book_data(TextbookCard.term) && WSData.course_data_for_term(TextbookCard.term));
    },

    render_upon_data: function(args) {
        if (TextbookCard._has_all_data()) {
            TextbookCard._render();
        }
    },

    render_error: function() {
        var book_error_code = WSData.book_data_error_code();
        var course_error_code = WSData.course_data_error_code();
        if (course_error_code === 404 || book_error_code === 404) {
            $("#TextbookCard").hide();
            return;
        }
        TextbookCard.dom_target.html(CardWithError.render("Textbooks"));
    },

    _render: function () {
        var term = TextbookCard.term;
        var course_data = WSData.course_data_for_term(term);
        var no_book_assigned = true;
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
                    if (no_book_assigned) {
                        no_book_assigned = false;
                    }
                });
                var course_id = section.curriculum + " " + section.course_number + " " + section.section_id;

                var section_data = {"course_id": course_id,
                                    "color_id": section.color_id,
                                    "required": required,
                                    "total": required + optional,
                                    "no_course_books": (required + optional) ? false :true
                                   };
                section_book_data.push(section_data);
            });
        }
        var template_data = {"registered": registered,
                             "term": term,
                             "no_book_assigned": no_book_assigned,
                             "quarter": course_data.quarter,
                             "year": course_data.year,
                             "summer_term": course_data.summer_term,
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
            },  "", "/textbooks/"+term);
            return false;
        });
        LogUtils.cardLoaded(TextbookCard.name, TextbookCard.dom_target);

    }

};
