// javascript
var data;
var multi_res_card_render_called = {};

$(document).ready(function() {
    LogUtils.init_logging();
    init_profile_events();
    init_modal_events();
    var course_data = null;
    var book_data = null;
    // This is to prevent multiple events on load from making
    // multiple web service calls.  This is required due to the
    // fix for MUWM-368
    var loaded_url = null;
    var render_called = {};

    History.Adapter.bind(window,'statechange',function(){
        var history_state = History.getState();
        var data = history_state.data;
        var state = data.state;

        // Reset all the multiple resourse card render records
        resetCardRenderCalled();

        var state_url = history_state.url;
        // This is the check of the same url, to prevent
        // duplicate web service requests on page load.
        if (state_url === loaded_url) {
            return;
        }

        $("#landing").removeClass("active");
        $("#nav_course_list").removeClass("active");
        $("#nav_visual_schedule").removeClass("active");
        $("#nav_finabala").removeClass("active");

        // Page titles are defined in templates/index.html
        if (state === undefined) {
            show_page_from_url();
            return;
        }
        else if (state === "landing") {
            Landing.render(data.term, data.course_index);
            $("#landing").addClass("active");
            document.title = window.page_titles.landing;
        }
        else if (state === "future_quarters") {
            FutureQuarter.render(data.term);
            document.title = window.page_titles.future_quarters;
        }
        else if (state === "textbooks") {
            TextBooks.show_books(data.term, data.textbook);
            document.title = window.page_titles.textbooks;
        }
        else if (state === "notices") {
            Notices.show_notices();
            document.title = window.page_titles.notices;
        }
        else if (state === "category_page") {
            Category.show_category_page(data.category, data.topic);
            // Document title is set in the category.js file - custom per category
            //document.title = window.page_titles["category_page"];
        }
        else if (state === "academic_calendar") {
            AcademicCalendar.show_events();
            document.title = window.page_titles.academic_calendar;
        }

        loaded_url = state_url;
    });
    
    function show_page_from_url() {
        var path = window.location.pathname;

        var hist = window.History,
            matches;

        // All version are at the same place
        path = path.replace(/^\/mobile/, "");

        if (path.match(/^\/landing/)) {
            // The old "home" url was at /landing/ - just send that to "/"
            hist.replaceState({
                state: "landing",
            },  "", "/");
        }
        else if (path.match(/^\/textbooks\/[0-9]{4}[-,a-z]+\/[%A-Z0-9]+$/)) {
            matches = path.match(/^\/textbooks\/([0-9]{4}[-,a-z]+)\/([%A-Z0-9]+)$/);
            hist.replaceState({
                state: "textbooks",
                term: matches[1],
                textbook: matches[2]
            },  "", path);
        }
        else if (path.match(/^\/textbooks\/[0-9]{4}[-,a-z]+\/?$/i)) {
            matches = path.match(/^\/textbooks\/([0-9]{4}[-,a-z]+)\/?$/i);
            hist.replaceState({
                state: "textbooks",
                term: matches[1]
            },  "", path);
        }
        else if (path.match(/^\/textbooks\/?/)) {
            hist.replaceState({
                state: "textbooks",
                term: "current"
            },  "", path);
        }
        else if (path.match(/^\/future_quarters\/[0-9]{4},[-,a-z]+/)) {
            matches = path.match(/^\/future_quarters\/([0-9]{4},[-,a-z]+)/);
            hist.replaceState({
                state: "future_quarters",
                term: matches[1],
            },  "", path);
        }
        else if (path.match(/^\/notices/)) {
            hist.replaceState({
                state: "notices",
            },  "", "/notices/");
        }
        else if (path.match(/^\/resource\/([a-z]+)/)) {
            matches = path.match(/^\/resource\/([a-z]+)\/?([a-z]+)?/);

            var category = (matches ? matches[1] : ""),
                topic = (matches ? matches[2] : undefined),
                slug = category;
            if (topic !== undefined) {
                slug += "/" + topic;
            }

            hist.replaceState({
                state: "category_page",
                category: category,
                topic: topic
            },  "", "/resource/" + slug );
        }
        else if (path.match(/^\/academic_calendar/)) {
            hist.replaceState({
                state: "academic_calendar",
            },  "", "/academic_calendar/");
        }

        else {
            // Now we fall back to the landing page
            hist.replaceState({
                state: "landing",
            },  "", "/");
        }


        History.Adapter.trigger(window, 'statechange');
    }

    var test_status = window.location.hash.indexOf('alert') === -1 ? 'false' : 'true';
    var test_alert_color;
    if (test_status) {
        test_alert_color = window.location.hash;
    }

    show_page_from_url();

    if (test_alert_color) {
        window.location.hash = test_alert_color;
    }

    $(".finabala").bind("click", function(ev) {
        $("#myuw_nav").collapse('hide');
        var hist = window.History;
        hist.pushState({
            state: "finabala",
        },  "", "/finabala");

        return false;
    });

    $(".logout_link").bind("click", function(ev) {
        $("#logout_form").submit();
        return false;
    });

    $("#nav_course_list").bind("click", function(ev) {
        WSData.log_interaction("nav_menu_course_list");
    });

    $("#nav_visual_schedule").bind("click", function(ev) {
        WSData.log_interaction("nav_menu_visual_schedule");
    });
    
    // handle clicking on resources
    $("#categories_link").bind("click", function(ev) {
        ev.preventDefault();                
        $('html, body').animate({
            scrollTop: $("#categories").offset().top
        }, "fast");
        return false;
    });
    
    // handle touchstart to mimic :hover event for mobile touch
    $('body').bind('touchstart', function() {});
        
});


var showLoading = function() {
    var source = $("#loading_header").html();
    var template = Handlebars.compile(source);
    $("#page-header").html(template());

    source = $("#loading_body").html();
    template = Handlebars.compile(source);
    $("#main-content").html(template());
};

var showError = function() {
    var source = $("#error_header").html();
    var template = Handlebars.compile(source);
    $("#page-header").html(template());

    source = $("#error_body").html();
    template = Handlebars.compile(source);
    $("#main-content").html(template());
};

// The strings from our web service only work w/ the native Date parsing on chrome :(
var date_from_string = function(date_string) {
    if (!date_string) {
        return;
    }
    var matches = date_string.match(/([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})/);
    if (!matches) {
        return;
    }
    var date_object = new Date(matches[1], (parseInt(matches[2], 10) - 1), parseInt(matches[3], 10), parseInt(matches[4], 10), parseInt(matches[5], 10));
    
    return date_object;
};

var titilizeTerm = function(term) {
    //Takes a term string (Eg 2032,summer,b-term) and 
    //returns a title (Eg Summer 2032 B-term)
    var pieces = term.split(",");
    if (pieces.length === 1) {
        return capitalizeString(term);
    }
    var string = capitalizeString(pieces[1]) + " " + pieces[0];
    if (pieces.length > 2) {
        string += " " + capitalizeString(pieces[2]);
    }
    return string;

};

var capitalizeString = function(string) {
    if (string === undefined) {
        return;
    }
    if (string.match(/^[ab]-term$/gi)) {
        value = string.split("-");
        return value[0].toUpperCase() + "-" + value[1].charAt(0).toUpperCase() + value[1].slice(1);
    }
    if (!string) {
        return "";
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
};

var init_profile_events = function () {
    Profile.add_events();
};

var init_modal_events = function () {
    Modal.add_events();
};

var renderedCardOnce = function(card_name) {
    var rendered = multi_res_card_render_called[card_name];
    multi_res_card_render_called[card_name] = true;
    return rendered;
};

var resetCardRenderCalled = function() {
    multi_res_card_render_called = {};
};
