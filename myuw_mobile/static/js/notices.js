/*global $, Handlebars, WSData*/

var Notices = {
    show_notices: function () {
        "use strict";
        WSData.fetch_notice_data(Notices.render_notices);
    },

    render_notices: function () {
        "use strict";
        var notices, source, template,
            expanded = false;

        notices = Notices.get_notices_by_date()
        notices['holds'] = Notices.get_notices_for_category("Holds");
        notices['legal'] = Notices.get_notices_for_category("Legal");

        source = $("#notices").html();
        template = Handlebars.compile(source);
        $("#main-content").html(template(notices));
        /* Events for expand/close all */
        $(".disclosure_toggle").click(function () {
            if (expanded) {
                expanded = false;
                $(".panel-collapse").collapse("hide");
                $("#expand").show();
                $("#collapse").hide();
            } else if (!expanded) {
                expanded = true;
                $(".panel-collapse").collapse("show");
                $("#expand").hide();
                $("#collapse").show();
            }

        });

    },

    get_notices_for_category: function (category) {
        "use strict";
        var i,
            notice,
            notices = WSData.notice_data(),
            filtered_notices = [];
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (notice["category"] === category) {
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
            notice_tags = notices[i]["location_tags"];
            if (notice_tags === null) {
                continue;
            }
            for (j = 0; j < notice_tags.length; j += 1) {
                if (notice_tags[j] === tag) {
                    filtered_notices.push(notices[i]);
                }
            }
        }
        return {"notices": filtered_notices,
                "unread_count": Notices._get_unread_count(filtered_notices),
                "critical_count": Notices._get_critical_count(filtered_notices)
                };
    },

    get_notices_by_date: function () {
        "use strict";
        var i,
            j,
            notice,
            date,
            notices = WSData.notice_data(),
            today,
            notices_today = [],
            notices_week = [],
            notices_next_week = [],
            notices_future = [];
        today = Notices._get_utc_date(new Date());

        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (notice['attributes'] !== null && notice['attributes'].length > 0){
                for (j = 0; j < notice['attributes'].length; j += 1){
                    if (notice['attributes'][j]['name'] === "Date"){
                        date = new Date(notice['attributes'][j]['value'] + " PST");
                        date = Notices._get_utc_date(date);
                        if(today.getDate() === date.getDate()){
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
        return Notices._get_unread_count(WSData.notice_data());
    },

    get_unread_count_by_category: function () {
        var i,
            category_counts = {},
            notices = WSData.notice_data();
        for (i = 0; i < notices.length; i += 1) {
            if (!notices[i]['is_read'] && notices[i]["category"] !== null) {
                if (notices[i]["category"] in category_counts) {
                    category_counts[notices[i]["category"]] += 1;
                } else {
                    category_counts[notices[i]["category"]] = 1;
                }
            }
        }
        return category_counts;
    },

    _get_unread_count: function (notices) {
        var unread_count = 0;
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (!notice["is_read"]) {
                    unread_count += 1;
            }
        }
        return unread_count;
    },

    _get_critical_count: function (notices) {
        var critical_count = 0;
        for (i = 0; i < notices.length; i += 1) {
            notice = notices[i];
            if (!notice["is_critical"]) {
                    critical_count += 1;
            }
        }
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
    var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7)
    return weekNo;
}
};
