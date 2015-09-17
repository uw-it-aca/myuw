/*global $, Handlebars, WSData*/

var Notices = {
    show_notices: function () {
        "use strict";
        CommonLoading.render_init();
        WSData.fetch_notice_data(Notices.render_notices);
    },

    _show_section: function(hidden_block, slide_link) {
        hidden_block.show();
        // Without this timeout, the animation doesn't happen - the block just appears.
        setTimeout(function() {
            hidden_block.toggleClass("slide-show");
            slide_link.siblings().find("i").removeClass("fa-angle-down");
            slide_link.siblings().find("i").addClass("fa-angle-up");
            slide_link.attr('title', 'Show less notice information');
            hidden_block.attr('aria-hidden', 'false');
            //WSData.log_interaction("show_final_card", term);
            Notices.get_notices_in_view_and_mark_read();
        }, 0);
    },

    _hide_section: function(hidden_block, slide_link) {
        hidden_block.toggleClass("slide-show");
        slide_link.attr('title', 'Show more notice information');
        hidden_block.attr('aria-hidden', 'true');

        setTimeout(function() {
            hidden_block.hide();
            slide_link.siblings().find("i").removeClass("fa-angle-up");
            slide_link.siblings().find("i").addClass("fa-angle-down");
        }, 700);
    },

    render_notices: function () {
        "use strict";
        var notices, source, template,
            expanded = false;

        notices = Notices.get_notices_by_date();

        var all_notices = [];
        var total_notices = 0;
        for (var group in notices) {
            total_notices += notices[group].notices.length;
            all_notices = all_notices.concat(notices[group].notices);
        }

        var critical_notices = Notices._get_all_critical();

        notices.total_notices = Notices.get_notice_page_notices().length;
        notices.legal = Notices.get_notices_for_category("Legal");
        notices.critical = {
            "count": critical_notices.length,
            "notices": critical_notices,
            "unread_count": Notices._get_unread_count(critical_notices)
        };

        source = $("#notices").html();
        template = Handlebars.compile(source);
        $("#main-content").html(template(notices));

        $(".panel-collapse").on('show.bs.collapse', function (e) {
            $(e.target).attr('aria-hidden', false);
            var icon = $($($(e.target).parent()).find(".fa-angle-down")[0]);
            icon.removeClass("fa-angle-down");
            icon.addClass("fa-angle-up");
        });
        $(".panel-collapse").on('hide.bs.collapse', function (e) {
            $(e.target).attr('aria-hidden', true);
            var icon = $($($(e.target).parent()).find(".fa-angle-up")[0]);
            icon.removeClass("fa-angle-up");
            icon.addClass("fa-angle-down");
        });

        /* Events for expand/close all */
        $("#expand_collapse").on("click", function(ev) {
            ev.preventDefault();
            var blocks = [$("#collapseOne"), $("#collapseTwo"), $("#collapseThree"), $("#collapseFour"), $("#collapseFive"), $("#collapseSix")];
            var i, block;

            function get_link_for_block(block) {
                return block.parent().find(".slide-link");
            }

            if (expanded) {
                expanded = false;
                for (i = 0; i < blocks.length; i++) {
                    block = blocks[i];
                    if (block.css('display') != 'none') {
                        Notices._hide_section(block, get_link_for_block(block));
                    }
                }
                setTimeout(function() {
                      $("#expand_collapse").text("Expand all");
                }, 700);
            } else if (!expanded) {
                expanded = true;
                for (i = 0; i < blocks.length; i++) {
                    block = blocks[i];
                    if (block.css('display') == 'none') {
                        Notices._show_section(block, get_link_for_block(block));
                    }
                }
                $(this).text("Collapse all");
                Notices.get_notices_in_view_and_mark_read();
            }

        });
        
        // event for slide show/hide panels
        $(".slide-link").on("click", function(ev) {
            ev.preventDefault();

            var hidden_block = $($(ev.target).closest("div.disclosure-heading").siblings(".slide-hide")[0]);
            
            var slide_link = $(this);
            
            if (hidden_block.css('display') == 'none') {
                Notices._show_section(hidden_block, slide_link);
            }
            else {
                Notices._hide_section(hidden_block, slide_link);
            }
        });

        // Event for marking notices as read on scroll, debounced
        LogUtils.de_bouncer(jQuery,'smartscroll', 'scroll', 100);
        $(window).smartscroll(function() {
                  Notices.get_notices_in_view_and_mark_read();
        });
    },


    sort_notices_by_start_date: function(notices){
        return notices.sort(function(a, b){
            return Notices._get_critical_notice_sort_date(b) -
                Notices._get_critical_notice_sort_date(a);
        });
    },

    _get_critical_notice_sort_date: function (notice){
        // Defaulting to something, using current time for now
        var date = new Date();

        var start_date_string = Notices.get_attribute_by_name('StartDate',
                                                              notice);
        var date_string = Notices.get_attribute_by_name('Date', notice);

        if(start_date_string !== undefined){
            date = Notices.parse_notice_date(start_date_string);
        } else if (date_string !== undefined){
            date = Notices.parse_notice_date(date_string);
        }
        return date;

    },

    parse_notice_date: function (notice_date) {
        var parts = notice_date.split("-");

        return new Date(parts[0], parts[1]-1, parts[2]);
    },

    get_attribute_by_name: function(attrib_name, notice){
        var attr_value;
        $.each(notice.attributes, function (idx, attr){
            if (attr.name === attrib_name){
                attr_value = attr.value;
            }
        });
        return attr_value;
    },

    get_notices_for_category: function (category) {
        "use strict";
        var i,
            notice,
            notices = WSData.notice_data(),
            filtered_notices = [];
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (notice.category === category) {
                filtered_notices.push(notice);
            }
        }
        return {"notices": filtered_notices,
                "unread_count": Notices._get_unread_count(filtered_notices),
                "critical_count": Notices._get_critical_count(filtered_notices)
                };
    },

    get_notices_for_tag: function (tag) {
        "use strict";
        var i,
            j,
            notice_tags,
            notices = WSData.notice_data(),
            filtered_notices = [];
        for (i = 0; i < notices.length; i += 1) {
            notice_tags = notices[i].location_tags;
            if (notice_tags === null) {
                continue;
            }
            for (j = 0; j < notice_tags.length; j += 1) {
                if (notice_tags[j] === tag) {
                    filtered_notices.push(notices[i]);
                }
            }
        }
        return filtered_notices;
    },

    get_ordered_finaid_notices: function (finaid_tags, is_critical) {
        var finaid_notices = [];
        for (var j = 0; j < finaid_tags.length; j += 1) {
            var notice = Notices.get_notices_for_tag(finaid_tags[j])[0];
            if (notice !== undefined && (is_critical === undefined || notice.is_critical)) {
                finaid_notices.push(notice);
            }
        }
        return (finaid_notices.length > 0 ? finaid_notices : null);
    },

    get_notices_by_date: function () {
        "use strict";
        var i,
            j,
            notice,
            date,
            today,
            notices = Notices.get_notices_for_tag('notices_date_sort'),
            notices_today = [],
            notices_week = [],
            notices_next_week = [],
            notices_future = [];

        today = Notices._get_utc_date(new Date());

        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            var notice_has_date = false;
            if (notice.attributes !== null && notice.attributes.length > 0) {
                for (j = 0; j < notice.attributes.length; j += 1){
                    if (notice.attributes[j].name === "Date"){
                        notice_has_date = true;
                        date = notice.attributes[j].value.replace(/-/g, "/");
                        date = date.replace("+00:00", " GMT");
                        date = new Date(date);

                        if (today.getDate() === date.getDate()) {
                            notices_today.push(notice);
                        } else if (Notices._get_week_number(date) === Notices._get_week_number(today)) {
                            notices_week.push(notice);
                        } else if (Notices._get_week_number(date) === Notices._get_week_number(today) + 1) {
                            notices_next_week.push(notice);
                        } else if (date > today) {
                            notices_future.push(notice);
                        }
                    }
                }
            }
            if (!notice_has_date) {
                notices_future.push(notice);
            }
        }
        return {"today":
                    {"notices": notices_today,
                    "unread_count": Notices._get_unread_count(notices_today),
                    "critical_count": Notices._get_critical_count(notices_today)
                    },
                "week":
                    {"notices": notices_week,
                    "unread_count": Notices._get_unread_count(notices_week),
                    "critical_count": Notices._get_critical_count(notices_week)
                    },
                "next_week":
                    {"notices": notices_next_week,
                    "unread_count": Notices._get_unread_count(notices_next_week),
                    "critical_count": Notices._get_critical_count(notices_next_week)
                    },
                "future":
                    {"notices": notices_future,
                    "unread_count": Notices._get_unread_count(notices_future),
                    "critical_count": Notices._get_critical_count(notices_future)
                    }
                };
    },

    get_total_unread: function (){
        return Notices._get_unread_count(Notices.get_notice_page_notices());
    },
    
    get_unread_non_critical_count: function() {
        var all_non_critical = [];
        var all_notices = Notices.get_notice_page_notices();
        for (i = 0; i < all_notices.length; i++) {
            if (!all_notices[i].is_critical) {
                all_non_critical.push(all_notices[i]);
            }
        }

        return Notices._get_unread_count(all_non_critical);
    },

    get_unread_count_by_category: function () {
        var i,
            category_counts = {},
            notices = WSData.notice_data();
        for (i = 0; i < notices.length; i += 1) {
            if (!notices[i].is_read && notices[i].category !== null) {
                if (notices[i].category in category_counts) {
                    category_counts[notices[i].category] += 1;
                } else {
                    category_counts[notices[i].category] = 1;
                }
            }
        }
        return category_counts;
    },

    _get_unread_count: function (notices) {
        var unread_count = 0;
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (!notice.is_read && notice.category !== "not a notice") {
                    unread_count += 1;
            }
        }
        return unread_count;
    },

    _get_critical: function(notices, exclude_sws_category) {
        var critical = [];
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (notice.is_critical) {
                if (exclude_sws_category === 'undefined' ||
                    notice.sws_category !== exclude_sws_category) {
                    critical.push(notice);
                }
            }
        }
        return critical;
    },

    _get_all_critical: function() {
        var critical = Notices._get_critical(WSData.notice_data(), "StudentFinAid");
        var finaid_critical_tags = ["tuition_aidhold",
                                    "tuition_missingdocs",
                                    "tuition_loanpromissory",
                                    "tuition_loancounseling",
                                    "tuition_acceptreject",
                                    "tuition_disbursedateA",
                                    "tuition_disbursedateB",
                                    "tuition_direct_deposit",
                                    "tuition_aid_prioritydate"
                                   ];
        var finaid_notices = Notices.get_ordered_finaid_notices(finaid_critical_tags, true);
        if (finaid_notices !== null) {
            critical = critical.concat(finaid_notices);
        }
        return critical;
    },

    _get_critical_count: function (notices) {
        return Notices._get_critical(notices).length;
    },

    get_total_critical_count: function () {
        return Notices._get_critical_count(WSData.notice_data());
    },

    _get_utc_date: function (date) {
        "use strict";
        return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
    },

    _get_week_number: function (d) {
        d = new Date(+d);
        d.setHours(0,0,0);
        d.setDate(d.getDate() + 4 - (d.getDay()||7));
        var yearStart = new Date(d.getFullYear(),0,1);
        var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
        return weekNo;
    },

    get_notices_in_view_and_mark_read: function () {
        var notice_hashes = [];
        $("[id^=collapse]").each(function (idx, element) {
            if ($(element).hasClass('slide-show')) {
                $.each($(element).find('ul.notices_list').children(), function (idx, notice) {
                    notice = $(notice).find('div.notice-container').first();
                    if (LogUtils.isScrolledIntoView($(notice))) {
                        if ($(notice).hasClass('unread')) {
                            notice_hashes.push($(notice).attr('id'));
                            $(notice).removeClass('unread');
                         }
                    }
                });
            }
        });
        if (notice_hashes.length > 0 ) {
            WSData.mark_notices_read(notice_hashes);
        }
    },

    get_notice_page_notices: function () {
        var page_notices = [];
        var unique_notices = [];

        var critical = Notices._get_all_critical();
        page_notices = page_notices.concat(critical);

        var legal = Notices.get_notices_for_category("Legal").notices;
        if(legal !== undefined) {
            page_notices = page_notices.concat(legal);
        }

        var date_sort = Notices.get_notices_for_tag('notices_date_sort');
        if(date_sort !== undefined) {
            page_notices = page_notices.concat(date_sort);
        }

        $(page_notices).each(function (i, notice) {
            var unmatched = true;
            $(unique_notices).each(function (i, unique_notice){
                if(unique_notice.id_hash === notice.id_hash) {
                    unmatched = false;
                }
            });
            if (unmatched) {
                unique_notices.push(notice);
            }
        });
        return unique_notices;
    }


};

