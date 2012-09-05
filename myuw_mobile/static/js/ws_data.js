WSData = {
    _course_data: null,

    course_data: function() {
        return WSData._course_data;
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
