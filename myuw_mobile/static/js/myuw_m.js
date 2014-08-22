// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;
    // This is to prevent multiple events on load from making
    // multiple web service calls.  This is required due to the
    // fix for MUWM-368
    var loaded_url = null;

    History.Adapter.bind(window,'statechange',function(){
        var history_state = History.getState();
        var data = history_state.data;
        var state = data.state;

        var state_url = history_state.url;
        // This is the check of the same url, to prevent
        // duplicate web service requests on page load.
        if (state_url === loaded_url) {
            return;
        }

        $("#landing").removeClass("active");
        $("#nav_course_list").removeClass("active");
        $("#nav_visual_schedule").removeClass("active");
        $("#nav_mylinks").removeClass("active");
        $("#nav_finabala").removeClass("active");

        // Page titles are defined in templates/index.html
        if (state === undefined) {
            show_page_from_url();
            return;
        }
        else if (state === "landing") {
            Landing.render(data.term, data.course_index);
            $("#landing").addClass("active")
            document.title = window.page_titles["landing"];
        }
        else if (state === "course_list") {
            // Figure out what to do from the url
            CourseList.show_list(data.term, data.course_index);
            $("#nav_course_list").addClass("active");
            document.title = window.page_titles["course_list"];
        }
        else if (state === "instructor") {
            Instructor.show_instructor(data.term, data.instructor);
            document.title = window.page_titles["instructor"];
        }
        else if (state === "future_quarters") {
            FutureQuarter.render(data.term);
            document.title = window.page_titles["future_quarters"];
        }
        else if (state === "textbooks") {
            TextBooks.show_books(data.term, data.textbook);
            document.title = window.page_titles["textbooks"];
        }
        else if (state === "quicklinks") {
            QuickLinks.show_links();
            $("#nav_mylinks").addClass("active");
            document.title = window.page_titles["links"];
        }
        else if (state === "finabala") {
            HfsAccounts.show_balances();
            $("#nav_finabala").addClass("active");
            document.title = window.page_titles["finabala"];
        }
        else if (state === "visual") {
            VisualSchedule.show_visual_schedule(data.term, data.course_index);
            $("#nav_visual_schedule").addClass("active");
            document.title = window.page_titles["visual"];
        }
        else if (state === "final_exams") {
            FinalExams.show_finals(data.term, data.course_index);
            document.title = window.page_titles["finals"];
        }
        else if (state === "grades") {
            Grades.show_grades(data.term);
            document.title = window.page_titles["grades"];
        }
        else if (state === "weekly") {
            Weekly.show_current_week(data);
            document.title = window.page_titles["weekly"];
        }
        else if (state === "libraries") {
            Libraries.show_card();
            document.title = window.page_titles["libraries"];
        }
        else if (state === "notices") {
            Notices.show_notices();
            document.title = window.page_titles["notices"];
        }
        else if (state === "category_page") {
            Category.show_category_page(data.category, data.topic);
            document.title = window.page_titles["category_page"];
        }


        loaded_url = state_url;
    });
    
    function show_page_from_url() {
        var path = window.location.pathname;

        var hist = window.History;

        // The replaceState is for MUWM-368
        if (path === "/mobile/") {
            hist.replaceState({
                state: "course_list",
                }, "", "/mobile"
            );
        }
        else if (path.match(/^\/mobile\/[0-9]{4},[a-z]+[,-abterm]*$/)) {
            var matches = path.match(/^\/mobile\/([0-9]{4},[a-z]+[,-abterm]*)$/);
            var state = "course_list";
            var term = matches[1];
            hist.replaceState({
                state: "course_list",
                term: matches[1]
            }, "", "/mobile/"+matches[1]);
        }
        else if (path.match(/^\/mobile\/visual\/[^\/]+\/[0-9]+$/)) {
            var matches = path.match(/^\/mobile\/visual\/([^\/]+)\/([0-9]+)/);
            hist.replaceState({
                state: "visual",
                term: matches[1],
                course_index: matches[2]
            },  "", "/mobile/visual/"+matches[1]+"/"+matches[2]);
        }
        else if (path.match(/^\/mobile\/visual\/[0-9]{4},[a-z]+[,-abterm]*$/)) {
            var matches = path.match(/^\/mobile\/visual\/([0-9]{4},[a-z]+[,-abterm]*)$/);
            hist.replaceState({
                state: "visual",
                term: matches[1]
            },  "", "/mobile/visual/"+matches[1]);
        } 
        else if (path.match(/^\/mobile\/visual\/[0-9]+$/)) {
            var matches = path.match(/^\/mobile\/visual\/([0-9]+)/);
            hist.replaceState({
                state: "visual",
                course_index: matches[1]
            },  "", "/mobile/visual/"+matches[1]);
        }
        else if (path.match(/^\/mobile\/visual\/?/)) {
            hist.replaceState({
                state: "visual"
            },  "", "/mobile/visual");
        }
        else if (path.match(/^\/mobile\/landing/)) {
            hist.replaceState({
                state: "landing",
            },  "", "/mobile/landing/");
        }
        else if (path.match(/^\/mobile\/textbooks\/[0-9]{4}[-,a-z]+\/[A-Z0-9]+$/)) {
            var matches = path.match(/^\/mobile\/textbooks\/([0-9]{4}[-,a-z]+)\/([A-Z0-9]+)$/);
            hist.replaceState({
                state: "textbooks",
                term: matches[1],
                textbook: matches[2]
            },  "", path);
        }
        else if (path.match(/^\/mobile\/textbooks\/[0-9]{4}[-,a-z]+$/i)) {
             var matches = path.match(/^\/mobile\/textbooks\/([0-9]{4}[-,a-z]+)$/i);
             hist.replaceState({
                 state: "textbooks",
                 term: matches[1]
             },  "", path);
        }
        else if (path.match(/^\/mobile\/textbooks\/?/)) {
            hist.replaceState({
                state: "textbooks",
                term: "current"
            },  "", path);
        }
        else if (path === "/mobile/links") {
            hist.replaceState({
                state: "quicklinks"
            },  "", "/mobile/links");
        }
        else if (path === "/mobile/finabala") {
            hist.replaceState({
                state: "finabala"
            },  "", "/mobile/finabala");
        }
        else if (path.match(/^\/mobile\/future_quarters\/[0-9]{4},[-,a-z]+/)) {
            var matches = path.match(/^\/mobile\/future_quarters\/([0-9]{4},[-,a-z]+)/);
            hist.replaceState({
                state: "future_quarters",
                term: matches[1],
            },  "", path);
        }
        else if (path === "/mobile/final_exams") {
            hist.replaceState({
                state: "final_exams"
            },  "", "/mobile/final_exams");
        }
        else if (path.match("/mobile/final_exams/[0-9]+$")) {
            var matches = path.match(/^\/mobile\/final_exams\/([0-9]+)/);
            hist.replaceState({
                state: "final_exams",
                course_index: matches[1]
            },  "", "/mobile/final_exams/"+matches[1]);
        }
        else if (path.match(/^\/mobile\/final_exams\/[^\/]+\/[0-9]+/)) {
            var matches = path.match(/^\/mobile\/final_exams\/([^\/]+)\/([0-9]+)/);
            hist.replaceState({
                state: "final_exams",
                term: matches[1],
                course_index: matches[2]
            },  "", "/mobile/final_exams/"+matches[1]+"/"+matches[2]);
        }
        else if (path.match(/^\/mobile\/final_exams\/[^\/]+/)) {
            var matches = path.match(/^\/mobile\/final_exams\/([^\/]+)/);
            hist.replaceState({
                state: "final_exams",
                term: matches[1],
            },  "", "/mobile/final_exams/"+matches[1]);
        }
        else if (path.match(/^\/mobile\/instructor\/[A-Z0-9]+/)) {
            var matches = path.match(/^\/mobile\/instructor\/([A-Z0-9]+)/);
            hist.pushState({
                state: "instructor",
                instructor: matches[1]
            },  "", "/mobile/instructor/"+matches[1]);
        }
        else if (path.match(/^\/mobile\/grades/)) {
            var matches = path.match(/^\/mobile\/grades\/([0-9,a-z]+)/);
            hist.replaceState({
                state: "grades",
                term: (matches ? matches[1] : "")
            },  "", "/mobile/grades/" + (matches
                                                 ? matches[1]
                                                 : ""));
        }
        else if (path.match(/^\/mobile\/weekly/)) {
            hist.replaceState({
                state: "weekly",
            },  "", "/mobile/weekly/");
        }
        else if (path.match(/^\/mobile\/libraries/)) {
            hist.replaceState({
                state: "libraries",
            },  "", "/mobile/libraries/");
        }
        else if (path.match(/^\/mobile\/notices/)) {
            hist.replaceState({
                state: "notices",
            },  "", "/mobile/notices/");
        }
        else if (path.match(/^\/mobile\/resource\/([a-z]+)/)) {
            var matches = path.match(/^\/mobile\/resource\/([a-z]+)\/?([a-z]+)?/),
                category = (matches ? matches[1] : ""),
                topic = (matches ? matches[2] : undefined);
            var slug = category;
            if (topic !== undefined) {
                slug += "/" + topic;
            }

            hist.replaceState({
                state: "category_page",
                category: category,
                topic: topic
            },  "", "/mobile/resource/" + slug );
        }
        else {
            // Just fall back to the course list?
            hist.replaceState({
                state: "course_list",
                }, "", "/mobile"
            );
            //CourseList.show_list();
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

    $(".quicklinks").bind("click", function(ev) {
        $("#myuw_nav").collapse('hide');
        var hist = window.History;
        hist.pushState({
            state: "quicklinks",
        },  "", "/mobile/links");

        return false;
    });

    $(".finabala").bind("click", function(ev) {
        $("#myuw_nav").collapse('hide');
        var hist = window.History;
        hist.pushState({
            state: "finabala",
        },  "", "/mobile/finabala");

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
    
    $("#categories_link").bind("click", function(ev) {
        ev.preventDefault();                
        $('html, body').animate({
            scrollTop: $("#categories").offset().top
        }, "fast");
        return false;
    });
        
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
    //Takes a term string (Eg 2032,summer,b-term) and returns a title (Eg Summer 2032: B-term)
    var pieces = term.split(",");
    var string = _capitalizeString(pieces[1]) + " " + pieces[0];
    if (pieces.length > 2) {
        string += ": " + _capitalizeString(pieces[2]);
    }
    return string

}

var _capitalizeString = function(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

var isScrolledIntoView = function(elem) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}
