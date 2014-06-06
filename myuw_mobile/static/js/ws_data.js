WSData = {
    _book_data: null,
    _course_data: {},
    _hfs_data: null,
    _library_data: null,
    _tuition_data: null,
    _grade_data: {},
    _notice_data: null,
    _instructor_data: {},
    _link_data: null,
    _oquarter_data: null,

    book_data: function() {
        return WSData._book_data;
    },

    current_course_data: function() {
        return WSData._course_data["current"];
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

    notice_data: function() {
        return WSData._notice_data;
    },

    oquarter_data: function() {
        return WSData._oquarter_data;
    },


    tuition_data: function() {
        return WSData._tuition_data;
    },

    fetch_book_data: function(callback, args) {
            if (WSData._book_data === null) {
                $.ajax({
                    url: "/mobile/api/v1/books/current/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._book_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                        showError();
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },


    fetch_current_course_data: function(callback, args) {
        return WSData.fetch_course_data_for_term("current", callback, args);
    },

    fetch_course_data_for_term: function(term, callback, args) {
        if (!WSData._course_data[term]) {
            $.ajax({
                url: "/mobile/api/v1/schedule/"+term,
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    // MUWM-549 and MUWM-552
                    var sections = results.sections;
                    var section_count = sections.length;
                    for (var index = 0; index < section_count; index++) {
                        section = sections[index];

                        var canvas_url = section["canvas_url"];
                        if (canvas_url) {
                            if (section["class_website_url"] == canvas_url) {
                                section["class_website_url"] = null;
                            }
                            var matches = canvas_url.match(/\/([0-9]+)$/);
                            var canvas_id = matches[1];
                            var alternate_url = "https://uw.instructure.com/courses/"+canvas_id;

                            if (section["class_website_url"] == alternate_url) {
                                section["class_website_url"] = null;
                            }
                        }
                    }
                    WSData._course_data[term] = results;
                    callback.apply(null, args);
                },
                error: function(xhr, status, error) {
                    showError();
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }

    },

    fetch_grades_for_term: function(term, callback, args) {
        if (!term) { term = ''; }

        if (WSData.course_data_for_term(term)) {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
            return;
        }

        $.ajax({
            url: "/mobile/api/v1/grades/"+term,
            type: 'GET',
            success: function(results) {
                WSData._grade_data[term] = results;
                callback.apply(null, args);
            },
            error: function() {
                showError();
            }
        });
    },

    fetch_current_week_data: function(callback, args) {
        $.ajax({
            url: "/mobile/api/v1/current_week/",
            type: 'GET',
            success: function(results) {
                callback.apply(null, [results, args]);
            },
            error: function() {
                showError();
            }
        });
    },

    fetch_course_data: function(callback, args) {
        console.warn("Use WSData.fetch_current_course_data instead");
    },

    fetch_link_data: function(callback, args) {
            if (WSData._link_data === null) {
                $.ajax({
                    url: "/mobile/api/v1/links/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._link_data = results;
                        callback.apply(null, args);
                    },
                    error: function(xhr, status, error) {
                        showError();
                    }
                });
            }
            else {
                window.setTimeout(function() {
                    callback.apply(null, args);
                }, 0);
            }
        },

    fetch_instructor_data: function(callback, args) {
        var instructor_regid = args[1];
        if (WSData._instructor_data[instructor_regid] === undefined) {
            $.ajax({
                    url: "/mobile/api/v1/person/"+instructor_regid,
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._instructor_data[instructor_regid] = results;
                        callback.apply(null, args);
                    },  
                    error: function(xhr, status, error) {
                        showError();
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
        }
    },

    normalize_instructors: function() {
        if (window.console) {
            console.warn("Use WSData.normalize_instructors_for_current_term");
        }
        WSData.normalize_instructors_for_current_term();
    },

    fetch_hfs_data: function(callback, args) {
        if (WSData._hfs_data === null) {
            $.ajax({
                    url: "/mobile/api/v1/hfs/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._hfs_data = results;
                        //callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        showError();
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                    callback.apply(null, args);
                    }, 0);
            }
        },

    fetch_library_data: function(callback, args) {
        if (WSData._library_data === null) {
            $.ajax({
                    url: "/mobile/api/v1/library/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._library_data = results;
                        //callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        showError();
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                    callback.apply(null, args);
                    }, 0);
            }
        },

    fetch_tuition_data: function(callback, args) {
        if (WSData._tuition_data === null) {
            $.ajax({
                    url: "/mobile/api/v1/finance/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._tuition_data = results;
                        //callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        showError();
                        }
                    });
              }
        else {
            window.setTimeout(function() {
                    callback.apply(null, args);
                    }, 0);
            }
        },

    fetch_notice_data: function(callback, args) {
        if (WSData._notice_data === null) {
            $.ajax({
                url: "/mobile/api/v1/notices/",
                dataType: "JSON",

                type: "GET",
                accepts: {html: "text/html"},
                success: function(results) {
                    WSData._notice_data = results;
                    callback.apply(null, args);
                },
                error: function(xhr, status, error) {
                    showError();
                }
            });
        }
        else {
            window.setTimeout(function() {
                callback.apply(null, args);
            }, 0);
        }
    },

    fetch_oquarter_data: function(callback, args) {
        if (WSData._oquarter_data === null) {
            $.ajax({
                    url: "/mobile/api/v1/oquarters/",
                    dataType: "JSON",

                    type: "GET",
                    accepts: {html: "text/html"},
                    success: function(results) {
                        WSData._oquarter_data = results;
                        callback.apply(null, args);
                        },
                    error: function(xhr, status, error) {
                        showError();
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
                url: "/mobile/api/v1/links/",
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

    log_interaction: function(interaction_type, term) {
        var logging_term;
        if(term === undefined) {
            logging_term = "";
        }            
        else {
            logging_term = "_term_" + term.replace(/[^a-z0-9]/gi, '_');
        }

        $.ajax({
                url: "/mobile/logger/" + interaction_type + logging_term,
                type: "GET",
                success: function(results) {},
                error: function(xhr, status, error) {}
        });
    },


};
