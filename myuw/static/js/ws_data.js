WSData = {

    save_links: function(links) {
        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        $.ajax({
                url: "/api/v1/links/",
                dataType: "JSON",
                data: JSON.stringify(links),
                type: "PUT",
                accepts: {html: "text/html"},
                headers: {
                     "X-CSRFToken": csrf_token
                },
                success: function(results) {
                },
                error: function(xhr, status, error) {
                }
       });
    },

    mark_notices_read: function(notice_hashes) {
        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        $.ajax({
                url: "/api/v1/notices/",
                dataType: "JSON",
                data: JSON.stringify({"notice_hashes": notice_hashes}),
                type: "PUT",
                accepts: {html: "text/html"},
                headers: {
                     "X-CSRFToken": csrf_token
                },
                success: function() {
                },
                error: function(xhr, status, error) {
                }
       });
    },

    log_interaction: function(interaction_type, term) {
        var logging_term;
        if(term === undefined) {
            logging_term = "";
        }
        else {
            logging_term = "_term_" + term.replace(/[^a-z0-9]/gi, '_');
        }

        $.ajax({
                url: "/logger/" + interaction_type + logging_term,
                type: "GET",
                success: function(results) {},
                error: function(xhr, status, error) {}
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.WSData = WSData;
