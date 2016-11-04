WSData = {
    _book_data: {},
    _book_data_error_status: {},
    _category_link_data: {},
    _course_data: {},
    _course_data_error_status: {},
    _department_events: null,
    _grade_data: {},
    _hfs_data: null,
    _mygrad_data: null,
    _iasystem_data: null,
    _library_data: null,
    _oquarter_data: null,
    _notice_data: null,
    _notice_data_error_status: null,
    _profile_data: null,
    _profile_data_error_status: null,
    _tuition_data: null,
    _instructor_data: {},
    _link_data: null,
    _success_callbacks: {},
    _error_callbacks: {},
    _callback_args: {},
    _academic_calendar_data: null,
    _current_academic_calendar_data: null,
    _myplan_data: {},
    _thrive_data: null,


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
    },


    book_data: function(term) {
        return WSData._book_data[term];
    },

    book_data_error_code: function(term) {
        return WSData._book_data_error_status[term];
    },

    course_data_error_code: function(term) {
        return WSData._course_data_error_status[term];
    },
    normalized_course_data: function(term) {
        var course_data;
        if (term) {
            course_data = WSData.course_data_for_term(term);
        } else {
            course_data = WSData.current_course_data();
        }
        if (course_data) {
            WSData._normalize_instructors(course_data);
        }
        return course_data;
    },

    current_course_data: function() {
        return WSData._course_data.current;
    },

    course_data: function() {
        if (window.console) {
            console.warn("Use WSData.current_course_data");
        }
        return WSData.current_course_data();
    },

    course_data_for_term: function(term) {
        return WSData._course_data[term];
    },

    grade_data_for_term: function(term) {
        if (!term) { term = ''; }
        return WSData._grade_data[term];
    },

    iasystem_data: function() {
        return WSData._iasystem_data;
    },

    hfs_data: function() {
        return WSData._hfs_data;
    },

    instructor_data: function(regid) {
        return WSData._instructor_data[regid];
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

    fetch_event_data: function(callback, err_callback, args) {
        if (WSData._department_events === null) {
            $.ajax({
                    url: "/api/v1/deptcal/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._department_events = results;
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

    fetch_book_data: function(term, callback, err_callback, args) {
        if (!WSData._book_data[term]) {
            var url = "/api/v1/book/" + term;

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
                    WSData._book_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._book_data_error_status[term] = xhr.status;
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


    fetch_current_course_data: function(callback, err_callback, args) {
        return WSData.fetch_course_data_for_term("current", callback, err_callback, args);
    },

    fetch_course_data_for_term: function(term, callback, err_callback, args) {
        if (!WSData._course_data[term]) {
            var url = "/api/v1/schedule/"+term;

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
                            var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

                            if (section.class_website_url == alternate_url) {
                                section.class_website_url = null;
                            }
                        }
                    }
                    WSData._course_data_error_status = null;
                    WSData._course_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._course_data_error_status[term] = xhr.status;
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

    fetch_instructed_course_data_for_term: function(term, callback, err_callback, args) {
        if (!WSData._course_data[term]) {
            var url = "/api/v1/instructor_schedule/"+term;

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
                            var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

                            if (section.class_website_url == alternate_url) {
                                section.class_website_url = null;
                            }
                        }
                    }
                    WSData._course_data_error_status = null;
                    WSData._course_data[term] = results;
                    WSData._run_success_callbacks_for_url(url);
                },
                error: function(xhr, status, error) {
                    WSData._course_data_error_status[term] = xhr.status;
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

    fetch_course_data: function(callback, args) {
        console.warn("Use WSData.fetch_current_course_data instead");
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

    fetch_instructor_data: function(callback, err_callback, args) {
        var instructor_regid = args[1];
        if (WSData._instructor_data[instructor_regid] === undefined) {
            $.ajax({
                    url: "/api/v1/person/"+instructor_regid,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._instructor_data[instructor_regid] = results;
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


    normalize_instructors_for_term: function(term) {
        WSData._normalize_instructors(WSData.course_data_for_term(term));
    },

    normalize_instructors_for_current_term: function() {
        WSData._normalize_instructors(WSData.current_course_data());
    },

    _sort_instructors_by_last_name: function(a, b) {
        if (a.surname < b.surname) return -1;
        if (a.surname > b.surname) return 1;
        return 0;
    },

    _normalize_instructors: function(data) {
        if (!data.sections.length) {
            return;
        }
        if (data.sections[0].instructors !== undefined) {
            return;
        }

        var section_index = 0;
        for (section_index = 0; section_index < data.sections.length; section_index++) {
            var section = data.sections[section_index];
            section.instructors = [];

            var instructors = {};
            var meeting_index = 0;
            for (meeting_index = 0; meeting_index < section.meetings.length; meeting_index++) {
                var meeting = section.meetings[meeting_index];
                var instructor_index = 0;
                for (instructor_index = 0; instructor_index < meeting.instructors.length; instructor_index++) {
                    var instructor = meeting.instructors[instructor_index];

                    if (instructors[instructor.uwregid] === undefined) {
                        section.instructors.push(instructor);
                    }
                    instructors[instructor.uwregid] = true;
                }
            }
            section.instructors = section.instructors.sort(WSData._sort_instructors_by_last_name);
        }
    },

    normalize_instructors: function() {
        if (window.console) {
            console.warn("Use WSData.normalize_instructors_for_current_term");
        }
        WSData.normalize_instructors_for_current_term();
    },

    fetch_hfs_data: function(callback, err_callback, args) {
        if (WSData._hfs_data === null) {
            $.ajax({
                    url: "/api/v1/hfs/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._hfs_data = results;
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

    fetch_iasystem_data: function(callback, err_callback, args) {
        if (WSData._iasystem_data === null) {
            var url = "/api/v1/ias/";

            if (WSData._is_running_url(url)) {
                WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
                return;
            }

            WSData._enqueue_callbacks_for_url(url, callback, err_callback, args);
            $.ajax({
                url: url,
                dataType: "JSON",

                type: 'GET',
                accepts: {html: "application/json"},
                success: function(results) {
                    WSData._iasystem_data = results;
                    if (callback !== null) {
                        callback.apply(null, args);
                    }
                },
                error: function(xhr, status, error) {
                    if (err_callback !== null) {
                        err_callback.call(null, xhr.status, error);
                    }
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

};
