var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WebServiceData.require({notice_data: new NoticeData()}, NoticeBanner.render);
    },

    render: function (resources) {
        var notice_data = resources.notice_data.data;

        if (notice_data.length > 0) {
            var source = $("#notice_banner").html();
            var template = Handlebars.compile(source);
            var notices = Notices._get_critical(Notices.notice_data);
            notices = Notices.sort_notices_by_start_date(notices);

            $.each(notices, function(idx, notice){
                notice.icon_class = NoticeBanner.get_icon_class_for_category(notice.category);
            });
            NoticeBanner._split_notice_titles(notices);

            var html = template({
                "total_unread": Notices.get_unread_non_critical_count(),
                "notices": notices
            });
            NoticeBanner.dom_target.html(html);
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
        return notices;
    },


    _init_events: function () {
        $(".crit-notice-title").on("click", function(e) {
            NoticeBanner._mark_read(e.target);
            var notice_id = $(e.target).parents(".notice-container").first().attr('id');
            var aria_div = $("#"+notice_id+"_div");
            if(aria_div.attr('aria-hidden')){
                aria_div.attr('aria-hidden', false);
            } else{
                aria_div.attr('aria-hidden', true);
            }
        });
    },

    _mark_read: function(elm) {
        // Looks backwards because class isn't removed until elm is shown,
        // which happens long after click event fires,
        // if has class element was just shown
        if($(elm).parent().hasClass('collapsed')){
            var notice_id = $(elm).parents(".notice-container").first().attr('id');
            WSData.mark_notices_read([notice_id]);
            var new_tag = $(elm).parent().siblings(".new-status").first();
            new_tag.hide();

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

