WSData = {
    _course_data: null,
    _book_data: null,

    book_data: function() {
        return WSData._book_data;
    },

    course_data: function() {
        return WSData._course_data;
    },

    fetch_book_data: function(callback, args) {
            if (WSData._book_data === null) {
                $.ajax({
                    url: "/my/api/v1/books/current/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._book_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },


    fetch_course_data: function(callback, args) {
            if (WSData._course_data === null) {
                $.ajax({
                    url: "/my/api/v1/schedule/current/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._course_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        }
};
