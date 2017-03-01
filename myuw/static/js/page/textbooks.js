var RenderPage = function () {
    if (myuwFeatureEnabled('instructor_schedule')) {
        $("#app_navigation").show();
    }

    TextBooks.show_books(window.textbook_data.term,
                         window.textbook_data.textbook ? window.textbook_data.textbook.length : undefined);
};
