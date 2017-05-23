/* Simpler WSData - generic errors and data by url.
   each requirement has url, data, error properties, setData method
*/

WebServiceData = {
	requirement_cache: {},     // resources indexed by url

    requirement_events_id: function () {
        return 'myuw.require.' + Math.random().toString(16).substring(2);
    },
    fetch_event_id: function (requirement) {
        return 'myuw.resource.' + requirement.url.replace(/[\?=&%]/g, '_');
    },
    requirement_is_loading: function (requirement) {
        var cached = WebServiceData.requirement_cache[requirement.url];
        return (cached && (cached.data === null && cached.error === null));
    },
    requirement_is_loaded: function (requirement) {
        var cached = WebServiceData.requirement_cache[requirement.url];
        return (cached && (cached.data !== null || cached.error !== null));
    },
    clear_requirement_cache: function () {
        WebServiceData.requirement_cache = {};
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
                    $(window).trigger(event_id, requirement);
                },
                error: function(xhr, status, error) {
                    requirement.error = {
                        xhr: xhr,
                        status: xhr.status,
                        error: error
                    };
                    WebServiceData._display_outage_message(requirement.url);
                    $(window).trigger(event_id, requirement);
                }
                // do not trigger on "complete", data needs to be processed first
            });
        }
        // else fetch is in flight, event trigger serves as the callback queue
    },
	requirement_loaded: function(callback, args, resources) {
        if ($.isArray(args)) {
            args.push(resources);
        } else {
            args = [resources];
        }

        window.setTimeout(function() {
            callback.apply(null, args);
        }, 0);
    },
    require: function(requirements, callback, args) {
        var requirement_event_id = WebServiceData.requirement_events_id();
        var requirement_count = Object.keys(requirements).length;
        var name;
        var loaded = 0;
        var name_url_map = {};
        var fetch_handler = function (e, req) {
            $(window).trigger(requirement_event_id, req);
        };
        var requirement_handler = function (e, req) {
            requirements[name_url_map[req.url]] = req;
            if (++loaded === requirement_count) {
                $(window).off(requirement_event_id);
                WebServiceData.requirement_loaded(callback, args, requirements);
            }
        };

        $(window).on(requirement_event_id, requirement_handler);

        for (name in requirements) {
            var requirement = requirements[name];
            var fetch_event_id = WebServiceData.fetch_event_id(requirement);
            name_url_map[requirement.url] = name;

            // fetch events separate from requirement events so
            // one fetch can satisfy multiple requests
            $(window).one(fetch_event_id, fetch_handler);
            WebServiceData.fetch_requirement(requirement, fetch_event_id);
        }
    },
    _display_outage_message: function(url) {
        // Displays the outage card if specific webservices are down
        if (WebServiceData._is_outage_api_url(url)){
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
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.WebServiceData = WebServiceData;
