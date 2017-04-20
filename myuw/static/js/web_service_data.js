/* Simpler WSData - generic errors and data by url.
   each requirement has url, data, error properties, setData method
*/ 

WebServiceData = {
	requirement_cache: {},     // resources indexed by url

    requirement_events_id: function () {
        return 'myuw.require.' + moment().valueOf().toString();
    },
    fetch_event_id: function (requirement) {
        return 'myuw.resource.' + requirement.url;
    },
    requirement_is_loading: function (requirement) {
        var cached = WebServiceData.requirement_cache[requirement.url];
        return (cached && (cached.data === null && cached.error === null));
    },
    requirement_is_loaded: function (requirement) {
        var cached = WebServiceData.requirement_cache[requirement.url];
        return (cached && (cached.data !== null || cached.error !== null));
    },
	fetch_requirement: function(requirement, event_id) {
        if (WebServiceData.requirement_is_loaded(requirement)) {
            $(window).trigger(event_id, WebServiceData.requirement_cache[requirement.url]);
        } else if (!WebServiceData.requirement_is_loading(requirement)) {
            WebServiceData.requirement_cache[requirement.url] = requirement;
            $.ajax({
                url: requirement.url,
                dataType: "JSON",
                type: "GET",
                accepts: requirement.accepts || {html: "text/html"},
                success: function(data) {
                    requirement.setData(data);
                },
                error: function(xhr, status, error) {
                    requirement.error = {
                        xhr: xhr,
                        status: xhr.status,
                        error: error
                    };
                },
                complete: function() {
                    $(window).trigger(event_id, requirement);
                }
            });
        }
        // else fetch in flight, fetch event will catch it
    },
	requirement_loaded: function(callback, args, resources) {
        if ($.isArray(args)) {
            $.each(resources, function () {
                args.push(this);
            });
        } else {
            args = resources;
        }

        window.setTimeout(function() {
            callback.apply(null, args);
        }, 0);
    },
    require: function(requirements, callback, args) {
        var requirement_event_id = WebServiceData.requirement_events_id();
        var loaded = [];

        $(window).on(requirement_event_id, function (e, req) {
            loaded.push(req);
            if (loaded.length === requirements.length) {
                $(window).off(requirement_event_id);
                WebServiceData.requirement_loaded(callback, args, loaded);
            }
        });

  	    $.each(requirements, function () {
            var requirement = this;
            var fetch_event_id = WebServiceData.fetch_event_id(requirement);

            // fetch events separate from requirement events so
            // one fetch can satisfy multiple requests
            $(window).one(fetch_event_id, function (e, req) {
                $(window).trigger(requirement_event_id, req);
            });

            WebServiceData.fetch_requirement(requirement, fetch_event_id);
        });
    },
    normalize_instructors: function(data) {
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
            section.instructors = section.instructors.sort(WebServiceData._sort_instructors_by_last_name);
        }
    },
    _sort_instructors_by_last_name: function(a, b) {
        if (a.surname < b.surname) return -1;
        if (a.surname > b.surname) return 1;
        return 0;
    },

};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.WebServiceData = WebServiceData;
