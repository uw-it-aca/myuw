// used in profile banner
Handlebars.registerHelper("formatPhoneNumber", function(str) {
    if (str.length == 10) {
        return str.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
    }
    return str;
});

Handlebars.registerHelper("formatStudentCredits", function(str) {
    return parseInt(str, 10);
});

(function() {

    function parse_date(str) {
        // After MUWM-3672, we're not using browser based parsing anymore.  Too many quirks.
        return Date.parse(str);
    }

    // used on course card
    Handlebars.registerHelper("toMonthDay", function(str) {
        return moment(parse_date(str)).format("MMM D");
    });

    // used on course card
    Handlebars.registerHelper("toMoreDay", function(str) {
        var d =  moment().from(moment(parse_date(str)), true);
        if (d.match(/^an? [a-z]+$/)) {
            return d.replace(/^an? /, '1 more ');
        } else {
            return d.replace(/ ([a-z]+)$/, ' more $1');
        }
    });

    // used on Library card
    Handlebars.registerHelper("toFromNowDate", function(str) {
        return moment(parse_date(str)).fromNow();
    });

    // used on Grade, Library card
    Handlebars.registerHelper("toFriendlyDate", function(str) {
        return moment(parse_date(str)).format("ddd, MMM D");
    });

    Handlebars.registerHelper("toFriendlyDateVerbose", function(str) {
        return moment(parse_date(str)).format("dddd, MMMM D");
    });
})();

(function() {
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    function _get_date(d) {
        return new Date(d.replace(/-/g, "/") + " 00:00:00");
    }

    function _date_range(d1, d2) {
        var date1 = _get_date(d1);
        var date2 = _get_date(d2);

        if (date1.getMonth() == date2.getMonth() && date1.getYear() == date2.getYear()) {
            return [months[date1.getMonth()], date1.getDate(), "-", date2.getDate()].join(" ");
        }
        else {
            return [months[date1.getMonth()], date1.getDate(), "-", months[date2.getMonth()], date2.getDate()].join(" ");
        }
    }

    Handlebars.registerHelper('acal_banner_date_format', function(d1, d2) {
        if (typeof(d2) != 'string' || d1 == d2) {
            var date1 = _get_date(d1);
            return [months[date1.getMonth()], date1.getDate(), "("+days[date1.getDay()]+")"].join(" ");
        }
        else {
            return _date_range(d1, d2);
        }
    });
    Handlebars.registerHelper('acal_page_date_format', function(d1, d2) {
        if (typeof(d2) != 'string' || d1 == d2) {
            var date1 = _get_date(d1);
            return [months[date1.getMonth()], date1.getDate()].join(" ");
        }
        else {
            return _date_range(d1, d2);
        }

    });
})();

Handlebars.registerHelper("safeLabel", function(str) {
    return safe_label(str);
});

Handlebars.registerHelper("toUrlSafe", function(str) {
    if(str) {
        return str.replace(/ /g, "%20");
    }
    return str;
});

Handlebars.registerHelper("toLowerCase", function(str) {
    if (str) {
        return str.toLowerCase();
    }
    return str;
});

// convert term string from "2013,summer,a-term" to "summer a-term"
Handlebars.registerHelper("termNoYear", function(term) {
    value = term.split(",");
    str = value[1];
    if (value[2]) {
        str += " " + value[2];
    }
    return str;
});


Handlebars.registerHelper('toTitleCase', function(term_str) {
    return titilizeTerm(term_str);
});

Handlebars.registerHelper("capitalizeString", function(str) {
    return capitalizeString(str);
});

// convert term string from "2013,summer,a-term" to "Summer 2013 A-Term"
Handlebars.registerHelper("titleFormatTerm", function(term) {
    value = term.split(",");
    str = capitalizeString(value[1]) + " " + value[0];
    if (value[2]) {
        str += " " + capitalizeString(value[2]);
    }
    return str;
});

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
    if (date_str === undefined) {
        return "";
    }
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
    if (date_str === undefined) {
        return "";
    }
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
    if (date_str === undefined) {
        return "";
    }
    var date = date_from_string(date_str);
    var day_of_week = date.getDay();
    var month_num = date.getMonth();
    var day_of_month = date.getDate();

    var day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    return new Handlebars.SafeString(day_names[day_of_week] + ", " + month_names[month_num] + " " + day_of_month);
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
    if (!formatted[1] || formatted[1].length === 0) {
        formatted[1] = "00";
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
        buffer += fn.fn(item);
    }
    return buffer;
});

Handlebars.registerHelper('format_schedule_hour', function(hour, position) {
    if (parseInt(hour, 10) === 12) {
        VisualSchedule.shown_am_marker = true;
        return hour + "p";
    }
    else if (hour > 12) {
        var shown_hour = hour - 12;
        if (position === 0) {
            return shown_hour + "p";
        }
        return shown_hour;
    }
    else if (hour < 12) {
        if (position === 0) {
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

Handlebars.registerHelper('show_card_days_meetings', function(list, start_time, end_time) {
    if (!VisualScheduleCard.day_template) {
        var day_source = $("#visual_schedule_card_day").html();
        var _day_template = Handlebars.compile(day_source);

        VisualScheduleCard.day_template = _day_template;
    }

    return new Handlebars.SafeString(VisualScheduleCard.day_template({ meetings: list, start_time: start_time, end_time: end_time }));
});

Handlebars.registerHelper('show_final_card_day', function(list, start_time, end_time, term) {
    if (!FinalExamCard.day_template) {
        var day_source = $("#final_exam_schedule_card_day").html();
        var _day_template = Handlebars.compile(day_source);

        FinalExamCard.day_template = _day_template;
    }

    return new Handlebars.SafeString(FinalExamCard.day_template({ meetings: list, start_time: start_time, end_time: end_time, term: term }));
});

Handlebars.registerHelper('pluralize', function(number, single, plural) {
    if (number === 1) {
        return single;
    }
    return plural;
});

Handlebars.registerHelper('pluralize_by_size', function(list, single, plural) {
    if (list.length === 1) {
        return single;
    }
    return plural;
});

Handlebars.registerHelper('greater_than', function(value1, value2, options) {
    if (arguments.length < 3)
        throw new Error("Handlebars Helper greater_than needs 2 parameters");
    if(value1 > value2) {
        return options.inverse(this);
    }
    else {
        return options.fn(this);
    }
});

Handlebars.registerHelper('list_greater_than', function(list, length, options) {
    if (arguments.length < 3)
        throw new Error("Handlebars Helper greater_than needs 2 parameters");
    if(list.length > length) {
        return options.inverse(this);
    }
    else {
        return options.fn(this);
    }
});


Handlebars.registerHelper('not_first', function(index, block) {
    // display block if the index greater than 0
    if (arguments.length < 2)
        throw new Error("Handlebars Helper not_first needs 1 parameter");
    if(parseInt(index) > 0) {
        return block.fn(this);
    }
});

Handlebars.registerHelper('not_equal', function(obj, value, block) {
    if (arguments.length < 3)
        throw new Error("Handlebars Helper not_equal needs 2 parameters");
    if(obj != value) {
        return block.fn(this);
    }
});

Handlebars.registerHelper('get_quarter_code', function(quarter_str) {
    if (arguments.length < 1) {
        throw new Error("Handlebars Helper quarter_code needs 1 parameter");
    }
    var q = quarter_str.toLowerCase();
    if(q === "winter") {
        return 1;
    }
    else if(q === "spring") {
        return 2;
    }
    else if(q === "summer") {
        return 3;
    }
    else if(q === "autumn") {
        return 4;
    }
    else {
        return "";
    }
});

Handlebars.registerHelper('slugify', function(value) {
    var slug = value.replace(/[^\w\s]+/gi, '').replace(/ +/gi, '-');
    return slug.toLowerCase();
});
