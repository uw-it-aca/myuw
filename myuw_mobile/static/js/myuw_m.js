// mobile javascript
var data;

$(document).ready(function() {

    var course_data = null;
    var book_data = null;
    // This is to prevent multiple events on load from making
    // multiple web service calls.  This is required due to the
    // fix for MUWM-368
    var loaded_url = null;

    // Google maps gets very confused by some characters in map urls
    Handlebars.registerHelper("encodeForMaps", function(str) {
        str = str.replace(/ \(/g, " - ");
        str = str.replace(/[\)&]/g, "");
        str = encodeURIComponent(str);
        return str;
    });

    //probably extraneous
    Handlebars.registerHelper("formatTime", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10);
        if (formatted[0] > 12) {
            formatted[0] -= 12;
        }
        return formatted.join(":");
    });

    //converts 24 hour time to 12 hour
    Handlebars.registerHelper("formatTimeAMPM", function(time) {
        formatted = time.toString().split(":");
        formatted[0] = parseInt(formatted[0], 10);
        if (formatted[0] < 12) {
            formatted[1] += "AM";
        }
        else {
            formatted[1] += "PM";
        }

        if (formatted[0] > 12) {
            formatted[0] = formatted[0] - 12;
        }
        return formatted.join(":");
    });

    // converts date string into 12 hour display - no am/pm
    Handlebars.registerHelper("formatDateAsTime", function(date_str) {
        var date = date_from_string(date_str);
        var hours = date.getHours();
        var minutes = date.getMinutes();
        if (minutes < 10) {
            minutes = "0"+minutes;
        }

        if (hours > 12) {
            hours = hours - 12;
        }
        return hours + ":" + minutes;
    });



    // converts date string into 12 hour am/pm display
    Handlebars.registerHelper("formatDateAsTimeAMPM", function(date_str) {
        var date = date_from_string(date_str);
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var am_pm;
        if (hours < 12) {
            am_pm = "AM";
        }
        else {
            am_pm = "PM";
        }

        if (minutes < 10) {
            minutes = "0"+minutes;
        }
        if (hours > 12) {
            hours = hours - 12;
        }
        return hours + ":" + minutes + am_pm;
    });

    // converts date string into a day display
    Handlebars.registerHelper("formatDateAsDate", function(date_str) {
        var date = date_from_string(date_str);
        var day_of_week = date.getDay();
        var month_num = date.getMonth();
        var day_of_month = date.getDate();

        var day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        return new Handlebars.SafeString(day_names[day_of_week] + "<br />" + month_names[month_num] + " " + day_of_month);
    });

    // converts date string into the label for the final exams schedule
    Handlebars.registerHelper("formatDateAsFinalsDay", function(date_str, days_back) {
        var date = date_from_string(date_str);
        date.setDate(date.getDate() - days_back);
        var day_of_week = date.getDay();
        var month_num = date.getMonth();
        var day_of_month = date.getDate();

        var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        return month_names[month_num] + " " + day_of_month;
    });

    Handlebars.registerHelper("ucfirst", function(str) {
        return str.replace(/^([a-z])/, function(match) {
            return match.toUpperCase();
        });
    });

    Handlebars.registerHelper("formatPrice", function(price) {
        formatted = price.toString().split(".");
        if (formatted[1] && formatted[1].length == 1) {
            formatted[1] += "0";
        }
        return formatted.join(".");
    });

    Handlebars.registerHelper('equal', function(value1, value2, options) {
        if (arguments.length < 3)
            throw new Error("Handlebars Helper equal needs 2 parameters");
        if(value1 != value2) {
            return options.inverse(this);
        } 
        else {
            return options.fn(this);
        }
    });

    Handlebars.registerHelper("eachWithIndex", function(array, fn) {
        var buffer = ""; 
        for (var i = 0, j = array.length; i < j; i++) {
            var item = array[i];
            item.index = i;
            buffer += fn(item);
        }   
        return buffer;
    }); 

    Handlebars.registerHelper('format_schedule_hour', function(hour) {
        if (parseInt(hour, 10) === 12) {
            VisualSchedule.shown_am_marker = true;
            return hour + "p";
        }
        else if (hour > 12) {
            var shown_hour = hour - 12;
            if (!VisualSchedule.shown_am_marker) {
                VisualSchedule.shown_am_marker = true;
                return shown_hour + "p";
            }
            return shown_hour;
        }
        else if (hour < 12) {
            if (!VisualSchedule.shown_am_marker) {
                VisualSchedule.shown_am_marker = true;
                return hour + "a";
            }
        }
        return hour;
    });

    Handlebars.registerHelper('time_percentage', function(time, start, end) {
        return VisualSchedule.get_scaled_percentage(time, start, end);
    });

    Handlebars.registerHelper('time_percentage_height', function(start, end, min, max) {
        var top = VisualSchedule.get_scaled_percentage(start, min, max);
        var bottom = VisualSchedule.get_scaled_percentage(end, min, max);

        return bottom-top;
    });

    Handlebars.registerHelper('show_days_meetings', function(list, start_time, end_time) {
        if (!VisualSchedule.day_template) {
            var day_source = $("#visual_schedule_day").html();
            var _day_template = Handlebars.compile(day_source);

            VisualSchedule.day_template = _day_template;
        }

        return new Handlebars.SafeString(VisualSchedule.day_template({ meetings: list, start_time: start_time, end_time: end_time }));
    });

    Handlebars.registerHelper('show_days_finals', function(list, start_time, end_time, term) {
        if (!VisualSchedule.day_template) {
            var day_source = $("#finals_schedule_day").html();
            var _day_template = Handlebars.compile(day_source);

            VisualSchedule.day_template = _day_template;
        }

        return new Handlebars.SafeString(VisualSchedule.day_template({ meetings: list, start_time: start_time, end_time: end_time, term: term }));
    });




    History.Adapter.bind(window,'statechange',function(){
        var history_state = History.getState();
        var data = history_state.data;
        var state = data.state;

        var state_url = history_state.url;
        // This is the check of the same url, to prevent
        // duplicate web service requests on page load.
        if (state_url == loaded_url) {
            return;
        }

        $("#nav_course_list").removeClass("active");
        $("#nav_visual_schedule").removeClass("active");
        $("#nav_mylinks").removeClass("active");
        $("#nav_finabala").removeClass("active");

        // Page titles are defined in templates/index.html
        if (state === undefined) {
            show_page_from_url();
            return;
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
            Quarters.show_future_quarters();
            document.title = window.page_titles["future_quarters"];
        }
        else if (state === "textbooks") {
            TextBooks.show_books();
            document.title = window.page_titles["textbooks"];
        }
        else if (state === "quicklinks") {
            QuickLinks.show_links();
            $("#nav_mylinks").addClass("active");
            document.title = window.page_titles["links"];
        }
        else if (state === "finabala") {
            FinaAccounts.show_balances();
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
            //CourseList.show_list();
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
            //VisualSchedule.show_visual_schedule(matches[1]);
        }
        else if (path.match(/^\/mobile\/visual\/?/)) {
            hist.replaceState({
                state: "visual"
            },  "", "/mobile/visual");
            //VisualSchedule.show_visual_schedule();
        }
        else if (path === "/mobile/textbooks") {
            hist.replaceState({
                state: "textbooks"
            },  "", "/mobile/textbooks");
            //TextBooks.show_books();
        }
        else if (path === "/mobile/links") {
            hist.replaceState({
                state: "quicklinks"
            },  "", "/mobile/links");
            //QuickLinks.show_links();
        }
        else if (path === "/mobile/finabala") {
            hist.replaceState({
                state: "finabala"
            },  "", "/mobile/finabala");
            //FinaAccounts.show_balances();
        }
        else if (path.match(/^\/mobile\/future_quarters/)) {
            var matches = path.match(/^\/mobile\/future_quarters(\/[a-z]+)/);
            hist.replaceState({
                state: "future_quarters"
            },  "", "/mobile/future_quarters" + (matches
                                                 ? matches[1]
                                                 : ""));
            //Quarters.show_future();
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

//            Instructor.show_instructor(matches[1]);
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
});


var showLoading = function() {
    var source = $("#loading_header").html();
    var template = Handlebars.compile(source);
    $("#page-header").html(template());

    source = $("#loading_body").html();
    template = Handlebars.compile(source);
    $("#courselist").html(template());
};

var showError = function() {
    var source = $("#error_header").html();
    var template = Handlebars.compile(source);
    $("#page-header").html(template());

    source = $("#error_body").html();
    template = Handlebars.compile(source);
    $("#courselist").html(template());
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



