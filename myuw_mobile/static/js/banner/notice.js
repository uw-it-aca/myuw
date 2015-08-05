var NoticeBanner = {
    dom_target: undefined,

    render_init: function(dom_taget) {
        NoticeBanner.dom_target  = dom_taget;
        WSData.fetch_notice_data(NoticeBanner.render);
    },

    render: function () {
        var notice_data = WSData.notice_data();

        if (notice_data.length > 0) {
            var source = $("#notice_banner").html();
            var template = Handlebars.compile(source);
            var notices = Notices._get_critical(WSData.notice_data());
            notices = Notices.sort_notices_by_start_date(notices);

            $.each(notices, function(idx, notice){
                notice.icon_class = NoticeBanner.get_icon_class_for_category(notice.category);
            });

            var html = template({
                "total_unread": Notices.get_total_unread(),
                "notices": notices
            });
            NoticeBanner.dom_target.html(html);
            NoticeBanner._init_events();
        }
    },

    _init_events: function () {
        var notices = $(NoticeBanner.dom_target).find(".notice-title");
        //supporting enter key for accessibility purposes
        $(".notice-container").keyup(function(e){
            if(e.keyCode === 13){
                NoticeBanner._toggle_notice($(this).find(".notice-title"));

            }
        });
        notices.on("click", function(elm){
            NoticeBanner._toggle_notice(elm.target);
        });
        $(NoticeBanner.dom_target).find(".notice-body-with-title, .notice-list").addClass("sr-only");
    },

    _toggle_notice: function(title_elm){
        var children = $(title_elm).parent().children(".notice-body-with-title, .notice-list");
        $.each(children, function(idx, child){
            if ($(child).hasClass("sr-only")){
                console.log("removing");
                console.log(child);
                $(child).removeClass("sr-only");
            } else {
                $(child).addClass("sr-only");
                console.log("adding");
                console.log(child);
            }
        });
        NoticeBanner._mark_read(children);
    },

    _mark_read: function(children) {
        if($(children[0]).hasClass("sr-only") === false){
            id_hash = $(children[0]).parent().parent().attr("id");
            WSData.mark_notices_read([id_hash]);
            var new_tag = $(children[0]).parent().children(".new-status");
            new_tag.hide();

        }
    },

    get_icon_class_for_category: function(category){
        var mapping = {'Holds': 'fa-ban  text-warning',
            'Fees & Finances': 'fa-usd text-success',
            'Graduation': 'fa-graduation-cap',
            'Admission': 'fa-university text-academics',
            'Registration': 'fa-clock-o text-info',
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

