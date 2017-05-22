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
        WSData.fetch_book_data(TextbookCard.term,
                               TextbookCard.render_upon_data,
                               TextbookCard.render_error);
        WSData.fetch_course_data_for_term(TextbookCard.term,
                                          TextbookCard.render_upon_data,
                                          TextbookCard.render_error);
    },

    _has_all_data: function () {
        if (WSData.book_data(TextbookCard.term) && WSData.course_data_for_term(TextbookCard.term)) {
            return true;
        }
        return false;
    },

    render_upon_data: function(args) {
        // Having multiple callbacks come to this function,
        // delay rendering until all requests are complete.
        if (!TextbookCard._has_all_data()) {
            return;
        }

        // _render should be called only once.
        if (renderedCardOnce(TextbookCard.name)) {
            return;
        }
        TextbookCard._render();
    },

    render_error: function() {
        var book_error_code = WSData.book_data_error_code(TextbookCard.term);
        var course_error_code = WSData.course_data_error_code(TextbookCard.term);
        if (course_error_code === 404 || book_error_code === 404) {
            $("#TextbookCard").hide();
            return;
        }
        TextbookCard.dom_target.html(CardWithError.render("Textbooks"));
    },

    _render: function () {
        var term = TextbookCard.term;
        var course_data = WSData.course_data_for_term(term);
        var textbook_data  = TextBooks.process_book_data(WSData.book_data(term), course_data);
        var no_book_assigned = true;
        var section_book_data = [];

        $.each(textbook_data.enrolled_sections, function (sec_idx, section) {
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

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TextbookCard = TextbookCard;
