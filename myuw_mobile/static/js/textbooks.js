var TextBooks = {
    term: undefined,
    anchor_textbook: undefined,

    show_books: function(term, textbook) {
        //Navbar.render_navbar("nav-sub");
        TextBooks.term = term;
        TextBooks.anchor_textbook = textbook;
        UwEmail.render_init();
        showLoading();
        WSData.fetch_book_data(term, TextBooks._fetch_course_data);
    },

    _fetch_course_data: function() {
        WSData.fetch_course_data_for_term(TextBooks.term, TextBooks.render_books);
    },

    process_book_data: function(book_data, course_data) {
        var template_data = {
            "sections": [],
            "quarter": course_data.quarter,
            "year": course_data.year,
            "summer_term": course_data.summer_term
        };

        var index = 0;
        for (index = 0; index < course_data.sections.length; index++) {
            var section = course_data.sections[index];
            template_data["sections"].push({
                index: index,
                section_title: section["course_title"],
                curriculum: section["curriculum_abbr"],
                course_number: section["course_number"],
                section_id: section["section_id"],
                color_id: section["color_id"],
                sln: section["sln"],
                books: book_data[section["sln"]],
            });
        }

        template_data["verba_link"] = book_data["verba_link"]
        return template_data;
    },

    render_books: function() {
        var term = TextBooks.term;
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#textbooks").html();
        var template = Handlebars.compile(source);
        var template_data = TextBooks.process_book_data(WSData.book_data(term), WSData.course_data_for_term(term))
        $("#main-content").html(template(template_data));

        // Scroll to correct section
        element = $("a[name='" + TextBooks.anchor_textbook + "']");
        if (element.length > 0) {
                $('html, body').animate({
                scrollTop: element.offset().top
            });
        }
    }
};

