var TextBooks = {
    show_books: function() {
        showLoading();
        WSData.fetch_book_data(TextBooks._fetch_course_data);
    },

    _fetch_course_data: function() {
        WSData.fetch_course_data(TextBooks.render_books);
    },

    render_books: function() {
        $('html,body').animate({scrollTop: 0}, 'fast');
        var source   = $("#textbooks").html();
        var template = Handlebars.compile(source);

        var book_data = WSData.book_data();
        var course_data = WSData.course_data();

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

        $("#courselist").html(template(template_data));

        source = $("#quarter-books").html();
        template = Handlebars.compile(source);
        $("#page-header").html(template({
        year: course_data.year, 
        quarter: course_data.quarter,
        summer_term: course_data.summer_term
    }));

        $(".display_list_sched").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "course_list",
            },  "", "/mobile/");

            return false;
        });


        $(".show_instructors").bind("click", function(ev) {
            var hist = window.History;
            hist.pushState({
                state: "course_list",
                course_index: ev.currentTarget.rel
            },  "", "/mobile/");

            return false;
        });



    }
};

