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
    var render_called = {};

    var test_status = window.location.hash.indexOf('alert') === -1 ? 'false' : 'true';
    var test_alert_color;
    if (test_status) {
        test_alert_color = window.location.hash;
    }

    window.RenderPage.call(this);

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
    return string.replace(/\w\S*/g,
                          function(txt){
                              return (txt.charAt(0).toUpperCase() +
                                      txt.substr(1).toLowerCase());
                          });
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

var toggle_card_disclosure = function(card, div_toggled, a_expose, a_hide, label) {
    var log_label = label==="" ? "" : " " + label;
    div_toggled.toggleClass("slide-show");
    div_toggled.css("display",
                    div_toggled.css("display") === 'none' ? '' : 'none');

    if (div_toggled.hasClass("slide-show")) {
        window.setTimeout(function() {
            div_toggled.show();
            a_expose.attr("hidden", true);
            a_expose.attr("aria-hidden", true);
            a_hide.attr("hidden", false);
            a_hide.attr("aria-hidden", false);
            div_toggled.attr("aria-expanded", true);
            div_toggled.attr("aria-hidden", false);
            div_toggled.attr("hidden", false);
            div_toggled.attr("tabindex", "0");
            div_toggled.focus();
        }, 0);
        window.myuw_log.log_card(card, "expand"+log_label);
    }
    else {
        window.setTimeout(function() {
            div_toggled.hide();
            a_expose.attr("hidden", false);
            a_expose.attr("aria-hidden", false);
            a_hide.attr("hidden", true);
            a_hide.attr("aria-hidden", true);
            div_toggled.attr("aria-expanded", false);
            div_toggled.attr("aria-hidden", true);
            div_toggled.attr("tabindex", "-1");
            div_toggled.attr("hidden", true);
        }, 700);
        window.myuw_log.log_card(card, "collapse"+log_label);
    }
};

var myuwFeatureEnabled = function(feature) {
    return (window.enabled_features.hasOwnProperty(feature) &&
            window.enabled_features[feature]);
};
