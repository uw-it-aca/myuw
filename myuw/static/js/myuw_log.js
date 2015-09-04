function MyuwLog()  {
    var myuwlog = this;

    this.link_logger = undefined;
    this.card_logger = undefined;
    this.appender = undefined;


    this.init = function() {
        this.link_logger = this.get_logger('link');
        this.card_logger = this.get_logger('card');
    };

    this.log_card = function(card, action) {
        var message = "";
        if (typeof(card.element)=== "object"){
            message = {card_name: $(card.element).attr('data-name'),
                       card_info: $(card.element).attr('data-identifier'),
                       card_position: card.pos,
                       action: action};
        }else if (typeof(card) === "string"){
            message = {card_name: card,
                       action: action};
        }

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
        this.appender.sendAllRemaining();
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
        window.setInterval(function() {
            window.myuw_log.send_links();
        }, 5000);
        return log;
    };

    this.get_appender = function() {
        var json_layout = new log4javascript.JsonLayout(true);
        var ajax_append = new log4javascript.AjaxAppender('/logging/log');
        ajax_append.setLayout(json_layout);
        ajax_append.setBatchSize(20);
        ajax_append.addHeader("X-CSRFToken", csrf_token);
        return ajax_append;
    };
}
