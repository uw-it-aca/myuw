var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WSData.fetch_notice_data(NoticeBanner.render, NoticeBanner.render_error);
    },

    render_error: function() {
        NoticeBanner.render_with_context({has_error: true});
    },

    render_with_context: function(context) {
        var source = $("#notice_banner").html();
        var template = Handlebars.compile(source);
        var html = template(context);
        NoticeBanner.dom_target.html(html);
    },

    render: function () {
        var notice_data = WSData.notice_data();

        if (notice_data.length > 0) {
            var critical_notices = Notices._get_critical(WSData.notice_data());
            critical_notices = Notices.sort_notices_by_start_date(critical_notices);

            $.each(critical_notices, function(idx, notice){
                notice.icon_class = NoticeBanner.get_icon_class_for_category(notice.category);
            });
            NoticeBanner._split_notice_titles(critical_notices);

            var notices = Notices.sort_notices_by_start_date(
                Notices.get_notice_page_notices(true));
            NoticeBanner._split_notice_titles(notices);

            NoticeBanner.render_with_context({
                "critical_notices": critical_notices,
                "notices": notices
            });
            NoticeBanner._init_events();
        }
    },

    _split_notice_titles: function (notices) {
        $.each(notices, function(idx, notice){
            var notice_title = $(notice.notice_content).filter(".notice-title");
            var placeholder = $("<div></div>");
            placeholder.append(notice_title);
            var notice_title_html = $(placeholder).html();

            placeholder = $("<div></div>");
            var notice_body = $(notice.notice_content).not(".notice-title");
            $.each(notice_body, function(idx, element){
                placeholder.append(element);
            });
            var notice_body_html = $(placeholder).html();
            notice.notice_title = notice_title_html;
            notice.notice_body = notice_body_html;
        });
    },


    _init_events: function () {
        $(".js-notice-link").on("click", function(e) {
            NoticeBanner._mark_read(e.currentTarget);
            var notice_id = $(e.currentTarget).parents(".notice-container").first().attr('id');
            var aria_div = $("#"+notice_id+"_div");
            var aria_focus = $("#"+notice_id+"_focus");
            var aria_a = $(e.currentTarget);

            if(aria_div.attr('aria-hidden') === "true"){
                // Remove hidden first to keep it from interfering with Bootstrap.
                aria_div.removeAttr('hidden');

                window.setTimeout(function() {
                    // Set to visible
                    aria_div.attr('aria-hidden', false);
                    aria_a.attr('aria-expanded', true);

                    // Set focus on div
                    aria_focus.attr('tabindex', 0);
                    aria_focus.focus();
                }, 300);
            } else {
                window.setTimeout(function() {
                    // Set hidden
                    aria_div.attr('aria-hidden', true);
                    aria_div.attr('hidden', 'hidden');
                    aria_a.attr('aria-expanded', false);

                    // Remove tabindex
                    aria_focus.removeAttr('tabindex');
                }, 300);
            }

        });
    },

    _mark_read: function(elm) {
        // Looks backwards because class isn't removed until elm is shown,
        // which happens long after click event fires,
        // if has class element was just shown
        if($(elm).hasClass('collapsed')){
            var notice_id = $(elm).parents(".notice-container").first().attr('id');
            WSData.mark_notices_read([notice_id]);
            var new_tag = $("#"+notice_id).find( ".new-status" ).first();
            if (new_tag.length > 0) {
                new_tag.hide();
            }
        }
    },

    get_icon_class_for_category: function(category){
        var mapping = {'Holds': 'fa-ban  text-warning',
            'Fees & Finances': 'fa-usd text-success',
            'Graduation': 'fa-graduation-cap',
            'Admission': 'fa-university text-academics',
            'Registration': 'fa-pencil-square-o text-info',
            'Insurance': 'fa-medkit text-insurance',
            'Legal': 'fa-gavel text-muted',
            'Visa': 'fa-globe text-visa'
        };
        if (category in mapping){
            return mapping[category];
        } else {
            return '';
        }

    }
};

/* node.js exports */
if (typeof exports === "undefined") {
    var exports = {};
}
exports.NoticeBanner = NoticeBanner;
