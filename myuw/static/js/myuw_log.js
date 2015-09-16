function MyuwLog()  {
    var myuwlog = this;

    this.link_logger = undefined;
    this.card_logger = undefined;
    this.appender = undefined;

    this.init = function() {
        this.link_logger = this.get_logger('link');
        this.card_logger = this.get_logger('card');

        $(window).unload(function() {
            window.myuw_log.send_links();
        });
    };

    this.log_card = function(card, action, extra_args) {
        var message = "",
            key;
        if (typeof(card.element)=== "object"){
            extra_args = extra_args || {};
            message = {card_name: LogUtils.get_card_name(card),
                       card_info: $(card.element).attr('data-identifier'),
                       card_position: card.pos,
                       action: action};

            for (key in extra_args) {
                if (extra_args.hasOwnProperty(key)) {
                    message[key] = extra_args[key];
                }
            }
        }else if (typeof(card) === "string"){
            message = {card_name: card,
                       action: action};
        }

        message.screen_width = $(window).width();
        message.screen_height = $(window).height();

        this.card_logger.info(JSON.stringify(message));
    };
    this.log_link = function(link, action) {
        var parent_cards = $(link).closest('.card');
        var card_name;
        var card_info;
        if (parent_cards.length > 0){
            card_info = $(parent_cards[0]).attr('data-identifier');
            card_name = $(parent_cards[0]).attr('data-name');
        }

        var href = $(link).attr('href');
        if (href !== "#") {
            var message = {href: $(link).attr('href'),
                           action: action,
                           source_card: card_name,
                           card_info: card_info};
            if (href.indexOf("notices") > -1) {
                message.unread_notice_count = Notices.get_total_unread();
            }
            this.link_logger.info(JSON.stringify(message));
        }
    };
    this.send_links = function() {
        if (this.appender.sendAllRemaining) {
            this.appender.sendAllRemaining();
        }
    };

    this.get_logger = function(name) {
        if (this.appender === undefined) {
            this.appender = this.get_appender();
        }
        var log = log4javascript.getLogger(name);
        log.addAppender(this.appender);

        //ensure all error messages are suppressed
        log4javascript.logLog.setQuietMode(true);

        //ensure logs are sent if a user doesn't navigate away
        if (!LogUtils.send_remaining_interval) {
            LogUtils.send_remaining_interval = window.setInterval(function() {
                window.myuw_log.send_links();
            }, LogUtils.PERIODIC_SEND_INTERVAL);
        }

        // Periodically log how long cards have been on screen
        if (!LogUtils.on_screen_interval_check) {
            LogUtils.on_screen_interval_check = window.setInterval(function() {
                LogUtils.periodicVisibilityLogging();
            }, LogUtils.PERIODIC_ONSCREEN_INTERVAL);
        }
        return log;
    };

    this.get_appender = function() {
        var json_layout = new log4javascript.JsonLayout(true);
        var append;
        if (window.location.hash == "#console") {
            append = new log4javascript.BrowserConsoleAppender('/logging/log');
        }
        else {
            append = new log4javascript.AjaxAppender('/logging/log');
            append.setBatchSize(20);
            append.addHeader("X-CSRFToken", csrf_token);
        }
        append.setLayout(json_layout);
        return append;
    };
}

var LogUtils = {
    PERCENTAGE_VISIBLE_THRESHOLD: 0.50,
    PERCENTAGE_OFFSCREEN_THRESHOLD: 0.05,
    PERIODIC_ONSCREEN_INTERVAL: 1000,
    PERIODIC_SEND_INTERVAL: 2000,
    current_visible_cards: {},

    get_new_visible_cards: function(){
        var cards = LogUtils.get_all_cards(),
            card_id,
            visible_cards = [],
            offscreen = [];


        $(cards).each(function(i, card){
            if(LogUtils.isScrolledIntoView(card.element)){
                visible_cards.push(card);
            }

            else if(LogUtils.isOffViewport(card.element)){
                offscreen.push(card);
            }
        });

        var log_values = LogUtils.evaluateCurrentlyVisibleCards(visible_cards, offscreen);
        LogUtils.logCardOnscreenChanges(log_values);
    },

    isScrolledIntoView: function(elem) {
        var docViewTop = $(window).scrollTop();
        var docViewBottom = docViewTop + $(window).height();

        var elmHeight = $(elem).height();
        var offset = $(elem).offset();
        var elemTop = $(elem).offset().top;
        var elemBottom = elemTop + elmHeight;

        return LogUtils.isInViewport(docViewTop, docViewBottom, elemTop, elemBottom);
    },

    isInViewport: function(viewport_top, viewport_bottom, elem_top, elem_bottom) {
        // 2 cases of completely off-screen
        if (elem_bottom < viewport_top) {
            return false;
        }
        if (elem_top > viewport_bottom) {
            return false;
        }

        // If it's fully on-screen...
        if ((elem_bottom <= viewport_bottom) && (elem_top >= viewport_top)) {
            return true;
        }

        var visible_height;
        // If we're above the viewport:
        if (elem_top < viewport_top) {
            visible_height = elem_bottom - viewport_top;
        }
        else {
            visible_height = viewport_bottom - elem_top;
        }
        var actual_height = elem_bottom - elem_top;
        var viewport_size = viewport_bottom - viewport_top;

        // If the top or bottom of the element is off-screen...
        // it can be on-screen if 80% of the card is visible
        if (visible_height >= actual_height * LogUtils.PERCENTAGE_VISIBLE_THRESHOLD) {
            return true;
        }

        // or if the card takes up 80% of the screen
        if (visible_height >= viewport_size * LogUtils.PERCENTAGE_VISIBLE_THRESHOLD) {
            return true;
        }

        return false;
    },

    // Only used on elements that have been on-viewport
    isOffViewport: function(viewport_top, viewport_bottom, elem_top, elem_bottom) {
        // 2 cases of completely off-screen
        if (elem_bottom < viewport_top) {
            return true;
        }
        if (elem_top > viewport_bottom) {
            return true;
        }

        // If it's fully on-screen...
        if ((elem_bottom <= viewport_bottom) && (elem_top >= viewport_top)) {
            return false;
        }

        var visible_height;
        // If we're above the viewport:
        if (elem_top < viewport_top) {
            visible_height = elem_bottom - viewport_top;
        }
        else {
            visible_height = viewport_bottom - elem_top;
        }
        var actual_height = elem_bottom - elem_top;
        var viewport_size = viewport_bottom - viewport_top;

        // If the top or bottom of the element is off-screen...
        // it's offscreen if 5% or less is visible
        if (visible_height > actual_height * LogUtils.PERCENTAGE_OFFSCREEN_THRESHOLD) {
            return false;
        }

        // or if the card takes up 5% or less of the screen
        if (visible_height > viewport_size * LogUtils.PERCENTAGE_OFFSCREEN_THRESHOLD) {
            return false;
        }

        return true;
    },


    get_new_visible_links: function () {
        var links = LogUtils.get_links_in_view();
        $(links).each(function(i, link) {
            var href = $(link).attr('href');
            if(!window.viewed_links.hasOwnProperty(href)){
                window.viewed_links[href] = link;
                window.myuw_log.log_link(link, "view");
            }

        });
    },

    get_links_in_view: function(){
       var links = [];
       $("a").each(function (i, link_elm) {
           var href = $(link_elm).attr('href');
           if (href !== "#"){
               if(LogUtils.isScrolledIntoView(link_elm)){
                   //Ensure link or parents aren't hidden
                   if(LogUtils.is_link_disclosed(link_elm)){
                       links.push(link_elm);
                   }
               }
           }
       });
       return links;
    },

    is_link_disclosed: function(elm) {
        return $(elm).attr("aria-hidden") !== true &&
               $(elm).parents('[aria-hidden="true"]').length === 0;

    },

    get_all_cards: function(){
       var cards = [],
           pos = 0;
       $("div").find("[data-type='card']").each(function (i, card) {
           pos++;
           cards.push({element: card, pos: pos});
       });
       return cards;
    },

    _init_link_logging: function() {
       $(document).on("click", "a", function () {
           window.myuw_log.log_link(this, "click");
           window.myuw_log.send_links();
       });
       LogUtils.de_bouncer(jQuery,'smartscroll', 'scroll', 100);
       window.viewed_links = {};
       $(window).smartscroll(function(e) {
           LogUtils.get_new_visible_links();
       });
    },

    _init_card_logging: function() {
        LogUtils.registerCardLoadEvents();
        LogUtils.de_bouncer(jQuery,'smartscroll', 'scroll', 100);
        $(window).smartscroll(function(e) {
            LogUtils.get_new_visible_cards();
        });
    },

    de_bouncer: function($,cf,of, interval){
       var debounce = function (func, threshold, execAsap) {
           var timeout;
           return function debounced () {
               var obj = this, args = arguments;
               function delayed () {
                   if (!execAsap)
                       func.apply(obj, args);
                   timeout = null;
               }
               if (timeout)
                   clearTimeout(timeout);
               else if (execAsap)
                   func.apply(obj, args);
               timeout = setTimeout(delayed, threshold || interval);
           };
       };
       jQuery.fn[cf] = function(fn){  return fn ? this.bind(of, debounce(fn)) : this.trigger(cf); };
    },

    init_logging: function () {
       myuwlog = new MyuwLog();

       myuwlog.init();
       window.myuw_log = myuwlog;
       LogUtils._init_link_logging();
       LogUtils._init_card_logging();
    },

    get_card_name: function(card) {
        var name = $(card.element).attr('data-name');
        var identifier = $(card.element).attr('data-identifier');

        if (identifier) {
            return name + "-" + identifier;
        }
        return name;
    },

    evaluateCurrentlyVisibleCards: function(cards, offscreen) {
        var values = {
            scrolled_out: [],
            scrolled_in: []
        };

        var new_visible_cards = {};
        var i, len;

        for (i = 0, len = cards.length; i < len; i++) {
            var card = cards[i];
            var card_name = LogUtils.get_card_name(card);

            if (LogUtils.current_visible_cards[card_name]) {
                new_visible_cards[card_name] = LogUtils.current_visible_cards[card_name];
                delete LogUtils.current_visible_cards[card_name];
            }
            else {
                new_visible_cards[card_name] = {
                    card: card,
                    first_onscreen: new Date().getTime(),
                    is_newly_read: false,
                    has_been_read: false,
                    rand: Math.random().toString(36).substring(2)
                };

                values.scrolled_in.push(new_visible_cards[card_name]);
            }
        }


        var newly_offscreen_keys = {};
        var key;
        for (i = 0, len = offscreen.length; i < len; i++) {
            key = LogUtils.get_card_name(offscreen[i]);
            newly_offscreen_keys[key] = true;
        }
        for (key in LogUtils.current_visible_cards) {
            if (LogUtils.current_visible_cards.hasOwnProperty(key)) {
                if (newly_offscreen_keys[key]) {
                    values.scrolled_out.push(LogUtils.current_visible_cards[key]);
                    delete LogUtils.current_visible_cards[key];
                }
                else {
                    new_visible_cards[key] = LogUtils.current_visible_cards[key];
                }
            }
        }

        LogUtils.current_visible_cards = new_visible_cards;
        return values;
    },

    logCardOnscreenChanges: function(changes) {
        var i,
            len,
            card;
        for (i = 0, len = changes.scrolled_in.length; i < len; i++) {
            window.myuw_log.log_card(changes.scrolled_in[i].card, "view", {
                rand: changes.scrolled_in[i].rand
            });
        }
        for (i = 0, len = changes.scrolled_out.length; i < len; i++) {
            card = changes.scrolled_out[i].card;
            window.myuw_log.log_card(card, "time_viewed", {
                time_visible: ((new Date().getTime()) - changes.scrolled_out[i].first_onscreen) / 1000,
                final: true,
                rand: changes.scrolled_out[i].rand
            });
        }
    },

    periodicVisibilityLogging: function() {
        var cards = LogUtils.getCurrentlyVisibleCards();
        for (var i = 0, len = cards.length; i < len; i++) {
            var card = cards[i];
            if (card.is_newly_read) {
                window.myuw_log.log_card(card.card, "read", {
                    rand: card.rand
                });
            }

            window.myuw_log.log_card(card.card, "time_viewed", {
                time_visible: ((new Date().getTime()) - card.first_onscreen) / 1000,
                final: false,
                rand: card.rand
            });
        }
    },

    getCurrentlyVisibleCards: function() {
        var list = [],
            key;
        for (key in LogUtils.current_visible_cards) {
            if (LogUtils.current_visible_cards.hasOwnProperty(key)) {
                var card = LogUtils.current_visible_cards[key];
                card.time_visible = ((new Date().getTime()) - card.first_onscreen) / 1000;

                if (card.time_visible >= 1.0) {
                    if (!card.has_been_read) {
                        card.is_newly_read = true;
                    }
                    else {
                        card.is_newly_read = false;
                    }
                    card.has_been_read = true;
                }
                list.push(card);
            }
        }
        return list;
    },

    // This should only be used in the test harness.
    _resetVisibleCards: function() {
        LogUtils.current_visible_cards = {};
    },

    registerCardLoadEvents: function() {
        $(window).on("myuw:card_load", LogUtils._logCardLoaded);
    },

    _logCardLoaded: function(ev, name, el) {
        var message = {
            action: "loaded",
            card_name: name,
            on_screen: LogUtils.isScrolledIntoView(el),
            screen_width: $(window).width(),
            screen_height: $(window).height()
        };
        window.myuw_log.card_logger.info(JSON.stringify(message));
        LogUtils.get_new_visible_cards();
        LogUtils.get_new_visible_links();
    },

    cardLoaded: function(name, el) {
        $(window).trigger("myuw:card_load", [ name, el ]);
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.LogUtils = LogUtils;
exports.MyuwLog = MyuwLog;

