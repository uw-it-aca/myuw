// javascript
var data;
var multi_res_card_render_called = {};

$(window.document).ready(function() {
    LogUtils.init_logging();
    init_modal_events();
    init_search_events();
    init_close_banner_msg_events();
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

    $(".opt-out-rate-myuw").bind("click", function(ev) {
        var rating_value = ev.currentTarget.getAttribute("data-rating");
        WSData.log_interaction("opt-out_rate_myuw_" + rating_value);
        var hide = $("#leave-feedback-div-onpop");
        var expose = $("#thank-feedback-div-onpop");
        window.setTimeout(function() {
            hide.attr("hidden", true);
            hide.attr("aria-hidden", true);
            expose.attr("hidden", false);
            expose.attr("aria-hidden", false);
            expose.focus();
        }, 0);
        return false;
    });


    // handle clicking on resources
    $("#categories_link").bind("click", function(ev) {
        ev.preventDefault();
        $('html, body').animate({
            scrollTop: $("#categories").offset().top
        }, "fast");
        return false;
    });

    // handle clicking on mobile menu
    $("#menu_toggle_wrapper").bind("click", function(ev) {

        var menuButton = $("#menu_toggle");
        var menu = $("#menu_container");

        // if open
        if (menu.hasClass("slide-down")) {
            menu.toggleClass("slide-down");
            menuButton.attr("aria-expanded", false);
        // if closed
        } else {
            menu.toggleClass("slide-down");
            window.setTimeout(function() {
                menuButton.attr("aria-expanded", true);
                $("#main_menu li:first-child a").focus();
            }, 0);
        }
	});

    // handle touchstart to mimic :hover event for mobile touch
    $('body').bind('touchstart', function() {});

    register_link_recorder();

    // display myuw tour popup once
    if (window.user.display_pop_up) {
        $('#tour_modal').modal('show');
        $.ajax({
            url: "/api/v1/turn_off_tour_popup",
            dataType: "JSON",
            async: true,
            type: 'GET',
            accepts: {html: "text/html"},
            success: function(results) {
                window.user.display_pop_up = false;
            },
            error: function(xhr, status, error) { }
        });
    }
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

// common method to set display style
var get_is_desktop = function() {
    var mobile_cutoff_width = 768;
    //using innerWidth as it takes into account scroll bars
    var viewport_width = window.innerWidth;
    return (viewport_width >= mobile_cutoff_width);
};

// The strings from our web service only work w/ the native Date parsing on chrome :(
var date_from_string = function(date_string) {
    if (!date_string) {
        return;
    }
    // handle format: 2013-04-22 10:57:06-08:00
    //                2013-04-22T10:57:06-08:00
    var matches = date_string.match(/([0-9]{4})-([0-9]{2})-([0-9]{2})[ T]([0-9]{2}):([0-9]{2})/);
    if (!matches) {
        return;
    }
    var date_object = new Date(matches[1], (parseInt(matches[2], 10) - 1), parseInt(matches[3], 10), parseInt(matches[4], 10), parseInt(matches[5], 10));

    return date_object;
};

var safe_label = function(section_label) {
    if(section_label){
        return section_label.replace(/[^A-Za-z0-9]/gi, '_');
    }
    return section_label;
};

var curr_abbr_url_safe = function(curr_abbr) {
    if(curr_abbr){
        return curr_abbr.replace(/ /g, '%20').replace(/&/g, '%26');
    }
    return curr_abbr;
};

var titilizeTerm = function (term) {
    //Takes a term string (Eg summer 2013, b-term)
    //returns a title (Eg Summer 2013 B-Term)
    var i;
    var pieces = term.split(/ |, |,/);
    var string = "";
    for (i = 0; i < pieces.length; i += 1) {
        if (i > 0) {
            string += " ";
        }
        string += capitalizeString(pieces[i]);
    }
    return string;

};

var capitalizeString = function(string) {
    //Takes a string eg, b-term
    if (string === undefined) {
        return;
    }
    if (string.match(/^(full|[ab])-term$/gi)) {
        value = string.split("-");
        return value[0].charAt(0).toUpperCase() + value[0].slice(1) + "-" + value[1].charAt(0).toUpperCase() + value[1].slice(1);
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
    OutageCard.reset();
};

var toggle_card_disclosure = function(card, div_toggled, a_expose, a_hide, label) {
    var log_label = label==="" ? "" : " " + label;

    div_toggled.on('shown.bs.collapse', function() {
//        a_expose.attr("hidden", true);
//        a_expose.attr("aria-hidden", true);
//        a_hide.attr("hidden", false);
//        a_hide.attr("aria-hidden", false);
//        div_toggled.attr("aria-expanded", true);
//        div_toggled.attr("aria-hidden", false);
//        div_toggled.attr("hidden", false);
        div_toggled.attr("tabindex", "0");
        div_toggled.focus();
        window.myuw_log.log_card(card, "expand"+log_label);
    })

    div_toggled.on('hidden.bs.collapse', function() {
//        a_expose.attr("hidden", false);
//        a_expose.attr("aria-hidden", false);
//        a_hide.attr("hidden", true);
//        a_hide.attr("aria-hidden", true);
//        div_toggled.attr("aria-expanded", false);
//        div_toggled.attr("aria-hidden", true);
        div_toggled.attr("tabindex", "-1");
//        div_toggled.attr("hidden", true);
        window.myuw_log.log_card(card, "collapse"+log_label);
    })
};

var register_link_recorder = function() {
    $('body').on('mousedown', "A", record_link_click);
    // For mocha testing
    $('body').on('click', "A", record_link_click);
    // For ios open in new window
    $('body').on('touchstart', "A", record_link_click);

};

var record_link_click = function(ev) {
    var target = $(this);
    if (target.attr('data-notrack') !== undefined) {
        return;
    }

    var original_href = target.attr('myuw-data-href');
    if (target.attr('myuw-data-href')) {
        return;
    }

    // Google search puts things here...
    var href = target.attr('data-ctorig');
    if (!href) {
        href = target.attr('href');
    }

    if (!href.match('^https?://')) {
        return;
    }
    target.attr('myuw-data-href', href);

    var linklabel = target.attr('data-linklabel');
    var label = "";
    if (linklabel) {
        label = linklabel;
    }
    else {
        label = target.text();
    }

    var new_href = '/out?u='+encodeURIComponent(href)+'&l='+encodeURIComponent(label);
    target.attr('href', new_href);
};

var myuwFeatureEnabled = function(feature) {
    return (window.enabled_features.hasOwnProperty(feature) &&
            window.enabled_features[feature]);
};

var getUrlParameter = function (name) {
    var url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results){
        return null;
    }
    if (!results[2]){
        return '';
    }
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

var init_search_events = function() {
    // handle clicking on search button

    $("#search_toggle").bind("click", function(ev) {
        window.setTimeout(function() {
            if ($("#search_toggle").hasClass("collapsed")) {
                $("#search-toggle").focus();
            }
            else {
                $("#search-nav").focus();
            }
        }, 400);
	});

};

var init_close_banner_msg_events = function() {
    // handle clicking on onboarding close button

    $(".myuw-banner-msg-close-btn").bind("click", function(ev) {
        ev.preventDefault();
        var desktop_div = document.getElementById("tour_messages_desktop");
        var mobile_div = document.getElementById("tour_messages_mobile");
        $.ajax({
            url: "/api/v1/close_banner_message",
            dataType: "JSON",
            async: true,
            type: 'GET',
            accepts: {html: "text/html"},
            success: function(results) {
                if (results.done) {
                    desktop_div.className += " hidden";
                    mobile_div.className += " hidden";
                }
            },
            error: function(xhr, status, error) {
                return false;
            }
        });
    });
};

var remove_card = function(target) {
    $(target).remove();
    $(window).trigger("card-hide");
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.capitalizeString = capitalizeString;
exports.curr_abbr_url_safe = curr_abbr_url_safe;
exports.date_from_string = date_from_string;
exports.get_is_desktop = get_is_desktop;
exports.myuwFeatureEnabled = myuwFeatureEnabled;
exports.register_link_recorder = register_link_recorder;
exports.remove_card = remove_card;
exports.renderedCardOnce = renderedCardOnce;
exports.resetCardRenderCalled = resetCardRenderCalled;
exports.safe_label = safe_label;
exports.titilizeTerm = titilizeTerm;
