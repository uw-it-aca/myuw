WSData = {
    _book_data: {},
    _book_data_error_status: {},
    _category_link_data: {},
    _course_data: {},
    _instructed_emaillist_data_error_status: {},
    _instructed_emaillist_data: {},
    _instructed_section_data: {},
    _instructed_section_data_error_status: {},
    _instructed_section_details: null,
    _instructed_section_details_error_status: null,
    _department_events: null,
    _grade_data: {},
    _mygrad_data: null,
    _library_data: null,
    _oquarter_data: null,
    _notice_data: null,
    _notice_data_error_status: null,
    _profile_data: null,
    _profile_data_error_status: null,
    _tuition_data: null,
    _link_data: null,
    _success_callbacks: {},
    _error_callbacks: {},
    _callback_args: {},
    _academic_calendar_data: null,
    _current_academic_calendar_data: null,
    _myplan_data: {},
    _thrive_data: null,
    _upass_data: null,


    // MUWM-1894 - enqueue callbacks for multiple callers of urls.
    _is_running_url: function(url) {
        if (WSData._success_callbacks[url] && WSData._success_callbacks[url].length) {
            return true;
        }
        return false;
    },
    _enqueue_callbacks_for_url: function(url, success, error, args) {
        if (!WSData._success_callbacks[url]) {
            WSData._success_callbacks[url] = [];
            WSData._error_callbacks[url] = [];
            WSData._callback_args[url] = [];
        }
        // Even if these are null, push them so the lists stay in sync.
        WSData._success_callbacks[url].push(success);
        WSData._error_callbacks[url].push(error);
        WSData._callback_args[url].push(args);
    },

    _run_success_callbacks_for_url: function(url) {
        var i,
            callback,
            args;

        for (i = 0; i < WSData._success_callbacks[url].length; i++) {
            callback = WSData._success_callbacks[url][i];
            args = WSData._callback_args[url][i];

            if (callback) {
                callback.apply(null, args);
            }
        }

        delete WSData._success_callbacks[url];
        delete WSData._error_callbacks[url];
        delete WSData._callback_args[url];
    },

    _run_error_callbacks_for_url: function(url) {
        var i,
            callback,
            args;

        for (i = 0; i < WSData._error_callbacks[url].length; i++) {
            callback = WSData._error_callbacks[url][i];
            args = WSData._callback_args[url][i];

            if (callback) {
                callback.apply(null, args);
            }
        }

        delete WSData._success_callbacks[url];
        delete WSData._error_callbacks[url];
        delete WSData._callback_args[url];
        WSData._display_outage_message(url);
    },

    _display_outage_message: function(url) {
        // Displays the outage card if specific webservices are down
        if (WSData._is_outage_api_url(url)){
            var card = OutageCard;
            card.dom_target =  $("#" + card.name);
            card.render_init();
            window.webservice_outage = true;
        }

    },

    _is_outage_api_url: function(url) {
        var endpoints = [
            "profile",
            "notices",
            "schedule"
        ];
        var is_outage = false;
        $(endpoints).each(function(idx, endpoint){
            if (url.indexOf(endpoint) !== -1){
                is_outage = true;
            }
        });
        return is_outage;

    },

    book_data: function(term) {
        return WSData._book_data[term];
    },

    book_data_error_code: function(term) {
        return WSData._book_data_error_status[term];
    },

    instructed_section_data_error_code: function(section_label) {
        return WSData._instructed_section_data_error_status[section_label];
    },
    normalized_instructed_section_data: function(section_label) {
        var section_data = WSData.instructed_section_data(section_label);
        if (section_data) {
            WSData._normalize_instructors(section_data);
        }
        return section_data;
    },

    instructed_section_data: function(section_label) {
        return WSData._instructed_section_data[section_label];
    },

    instructed_section_details: function() {
        return WSData._instructed_section_details;
    },

    instructed_section_details_error_code: function() {
        return WSData._instructed_section_details_error_status;
    },

    grade_data_for_term: function(term) {
        if (!term) { term = ''; }
        return WSData._grade_data[term];
    },

    library_data: function() {
        return WSData._library_data;
    },

    link_data: function() {
        return WSData._link_data;
    },

    mygrad_data: function() {
        return WSData._mygrad_data;
    },

    notice_data: function() {
        return WSData._notice_data;
    },

    oquarter_data: function() {
        return WSData._oquarter_data;
    },

    category_link_data: function(category) {
        return WSData._category_link_data[category];
    },

    tuition_data: function() {
        return WSData._tuition_data;
    },

    profile_data: function() {
        return WSData._profile_data;
    },

    dept_event_data: function() {
        return WSData._department_events;
    },
    thrive_data: function() {
        return WSData._thrive_data;
    },
    upass_data: function() {
        return WSData._upass_data;
    },

    academic_calendar_data: function() {
        return WSData._academic_calendar_data;
    },

    current_academic_calendar_data: function() {
        return WSData._current_academic_calendar_data;
    },

    myplan_data: function(year, quarter) {
        if (WSData._myplan_data[year]) {
            if (WSData._myplan_data[year][quarter]) {
                return WSData._myplan_data[year][quarter];
            }
        }
        return null;
    },

    fetch_academic_calendar_events: function(callback, err_callback, args) {
        if (!WSData._academic_calendar_data) {
            var url = "/api/v1/academic_events";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._academic_calendar_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_current_academic_calendar_events: function(callback, err_callback, args) {
        if (!WSData._current_academic_calendar_data) {
            var url = "/api/v1/academic_events/current/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._current_academic_calendar_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_instructed_section_data: function(section_label, callback, err_callback, args) {
        if (!WSData._instructed_section_data[section_label]) {
            var url = "/api/v1/instructor_section/" + section_label;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",
                async: true,
                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    // MUWM-549 and MUWM-552
                    var sections = results.sections;
                    var section_count = sections.length;
                    for (var index = 0; index < section_count; index++) {
                        section = sections[index];

                        var canvas_url = section.canvas_url;
                        if (canvas_url) {
                            if (section.class_website_url == canvas_url) {
                                section.class_website_url = null;
                            }
                            var matches = canvas_url.match(/\/([0-9]+)$/);
                            var canvas_id = matches[1];
                            var alternate_url = "https://canvas.uw.edu/courses/"+canvas_id;

                            if (section.class_website_url == alternate_url) {
                                section.class_website_url = null;
                            }
                        }
                    }
                    WSData._instructed_section_data_error_status[section_label] = null;
                    WSData._instructed_section_data[section_label] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._instructed_section_data_error_status[section_label] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }

    },

    fetch_instructed_section_details: function(section_label, callback, err_callback, args) {
        var url = "/api/v1/instructor_section_details/" + section_label;

        if (WSData._is_running_url(url)) {
            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            return;
        }

        WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

        $.ajax({
            url: url,
            dataType: "JSON",
            async: true,
            type: "GET",
            accepts: {html: "text/html"},
            success: function(results) {
                WSData._instructed_section_details_error_status = null;
                WSData._instructed_section_details = results;
                WSData._run_success_callbacks_for_url(url);
            },
            error: function(xhr, status, error) {
                WSData._instructed_section_details_error_status = xhr.status;
                WSData._run_error_callbacks_for_url(url);
            }
        });

    },

    fetch_grades_for_term: function(term, callback, err_callback, args) {
        if (!term) { term = ''; }

        if (WSData.course_data_for_term(term)) {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
            return;
        }

        $.ajax({
            url: "/api/v1/grades/"+term,
            type: 'GET',
            success: function(results) {
                WSData._grade_data[term] = results;
                err_callback.call(null, status, error);
            },
            error: function(xhr, status, error) {
                err_callback.call(null, xhr.status, error);
            }
        });
    },

    fetch_current_week_data: function(callback, err_callback, args) {
        $.ajax({
            url: "/api/v1/current_week/",
            type: 'GET',
            success: function(results) {
                callback.apply(null, [results, args]);
            },
            error: function() {
                err_callback.call(null, status, error);
            }
        });
    },

    fetch_link_data: function(callback, err_callback, args) {
            if (WSData._link_data === null) {
                $.ajax({
                    url: "/api/v1/links/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._link_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, status, error);
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },

    fetch_library_data: function(callback, err_callback, args) {
        if (WSData._library_data === null) {
            $.ajax({
                    url: "/api/v1/library/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._library_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_mygrad_data: function(callback, err_callback, args) {
        if (WSData._mygrad_data === null) {
            $.ajax({
                url: "/api/v1/grad/",
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._mygrad_data = results;
                    callback.apply(null, args);
                },
                error: function(xhr, status, error) {
                    err_callback.call(null, xhr.status, error);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_tuition_data: function(callback, err_callback, args) {
        if (WSData._tuition_data === null) {
            $.ajax({
                    url: "/api/v1/finance/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._tuition_data = results;
                        if (callback !== null) {
                            callback.apply(null, args);
                        }
                    },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_notice_data: function(callback, err_callback, args) {
        if (WSData._notice_data === null) {
            var url = "/api/v1/notices/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._notice_data = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._notice_data_error_status = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_oquarter_data: function(callback, err_callback, args) {
        if (WSData._oquarter_data === null) {
            $.ajax({
                    url: "/api/v1/oquarters/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._oquarter_data = results;
                        callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_category_links: function(callback, err_callback, args) {
        var category = args[0];
        if (WSData._category_link_data[category] === undefined) {
            $.ajax({
                    url: "/api/v1/categorylinks/" + category,
                    dataType: "JSON",
                    type: "GET",
                    accepts: {html: "application/json"},
                    success: function(results) {
                        WSData._category_link_data[category] = results;
                        callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        err_callback.call(null, xhr.status, error);
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_profile_data: function(callback, err_callback, args) {
        if (WSData._profile_data === null) {
            var url = "/api/v1/profile/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._profile_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._profile_data_error_status = xhr.status;
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_myplan_data: function(year, quarter, callback, err_callback, args) {
        if (WSData.myplan_data(year, quarter) === null) {
            var url = "/api/v1/myplan/"+year+"/"+quarter;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    if (!WSData._myplan_data[year]) {
                        WSData._myplan_data[year] = {};
                    }
                    WSData._myplan_data[year][quarter] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._run_error_callbacks_for_url(url);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_upass_data: function(callback, err_callback, args) {
        if (WSData.upass_data() === null) {
            var url = "/api/v1/upass/";
            $.ajax({
                url: url,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "application/json"},
                success: function(results) {
                    WSData._upass_data = results;
                    if (callback !== null) {
                        callback.apply(null, args);
                    }
                },
                error: function(xhr, status, error) {
                    err_callback.call(null, xhr.status, error);
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

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
    },

    fetch_thrive_data: function(callback, err_callback, args) {
        if (WSData._thrive_data === null) {
            var url = "/api/v1/thrive/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._thrive_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_thrive_data_history: function(callback, err_callback, args) {
        if (WSData._thrive_data === null) {
            var url = "/api/v1/thrive/?history=1";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._thrive_data = results;
                        WSData._run_success_callbacks_for_url(url);
                    },
                    error: function(xhr, status, error) {
                        WSData._run_error_callbacks_for_url(url);
                    }
                 });
              }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_instructed_section_emaillist_data: function(section_label, callback, err_callback, args) {
        if (!WSData._instructed_emaillist_data[section_label]) {
            var url = "/api/v1/emaillist/" + section_label;

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);

            $.ajax({
                url: url,
                dataType: "JSON",
                async: true,
                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._instructed_emaillist_data_error_status[section_label] = null;
                    WSData._instructed_emaillist_data[section_label] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._instructed_emaillist_data_error_status[section_label] = xhr.status;
                    WSData._run_error_callbacks_for_url(url);
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

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.WSData = WSData;
