/*jshint esversion: 6 */

// used on profile student_info, directory_info
Handlebars.registerHelper("formatPhoneNumber", function(value) {
    if (arguments.length === 0 || value === undefined || value.length === 0) {
        return '';
    }
    if (value.match(/^\+1 /)) {
        value = value.substring(3);
    }
    var regexp = /^(\d{3})([ -\.]?)(\d{3})([ -\.]?)(\d{4})$/;
    var number = value.match(regexp);
    if (number) {
        return '(' + number[1] + ') ' + number[3] + '-' + number[5];
    }
    return value;
});

// used on future_quarter.html
Handlebars.registerHelper("strToInt", function(str) {
    // credit string to integer
    return parseInt(str, 10);
});

(function() {
    // used on course card
    Handlebars.registerHelper("toMonthDay", function(str) {
        return moment(str).format("MMM D");
    });

    // used on Library card
    Handlebars.registerHelper("toFromNowDate", function(str) {
        return moment(str).fromNow();
    });

    // On Grade, Library, Course, tuition, medicine password
    Handlebars.registerHelper("toFriendlyDate", function(date_str) {
        if (date_str === undefined || date_str.length === 0) {
            return "";
        }
        return moment(date_str).format("ddd, MMM D");
    });

    Handlebars.registerHelper("toFriendlyDateVerbose", function(date_str) {
        if (date_str === undefined || date_str.length === 0) {
            return "";
        }
        return moment(date_str).format("dddd, MMMM D");
    });
})();

(function() {
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
                  'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'];
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday'];

    function _get_date(d) {
        return new Date(d.replace(/-/g, "/") + " 00:00:00");
    }

    function _date_range(d1, d2) {
        var date1 = _get_date(d1);
        var date2 = _get_date(d2);

        if (date1.getMonth() === date2.getMonth() && date1.getYear() === date2.getYear()) {
            return [months[date1.getMonth()], date1.getDate(), "-", date2.getDate()].join(" ");
        }
        else {
            return [months[date1.getMonth()], date1.getDate(), "-", months[date2.getMonth()], date2.getDate()].join(" ");
        }
    }

    Handlebars.registerHelper('acal_banner_date_format', function(d1, d2) {
        if (typeof(d2) !== 'string' || d1 === d2) {
            var date1 = _get_date(d1);
            return [months[date1.getMonth()], date1.getDate(), "("+days[date1.getDay()]+")"].join(" ");
        }
        else {
            return _date_range(d1, d2);
        }
    });
    Handlebars.registerHelper('acal_page_date_format', function(d1, d2) {
        if (typeof(d2) !== 'string' || d1 === d2) {
            var date1 = _get_date(d1);
            return [months[date1.getMonth()], date1.getDate()].join(" ");
        }
        else {
            return _date_range(d1, d2);
        }

    });

    Handlebars.registerHelper('short_year', function(year) {
        year = ""+year;
        return "’"+year.substr(-2,2);
    });
})();

Handlebars.registerHelper("safeLabel", function(str) {
    return safe_label(str);
});

Handlebars.registerHelper("toUrlSafe", function(curr_abbr) {
    return curr_abbr_url_safe(curr_abbr);
});

// a letter followed by up to 33 letters, digits, periods, or hyphens.
Handlebars.registerHelper("toAnchorName", function(curr_abbr) {
    return curr_abbr.replace(/ /g, '-');
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

Handlebars.registerHelper('titleCaseName', function(str) {
    return str.split(' ').map(function(w) {
        return w[0].toUpperCase() + w.substr(1).toLowerCase();
    }).join(' ');
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
    if (str) {
        str = str.replace(/ \(/g, " - ");
        str = str.replace(/[\)&]/g, "");
        str = encodeURIComponent(str);
    }
    return str;
});

//convert to 12 hour and remove seconds
Handlebars.registerHelper("formatTime", function(time) {
    formatted = time.toString().split(":");
    formatted[0] = parseInt(formatted[0], 10);
    if (formatted[0] > 12) {
        formatted[0] -= 12;
    }
    return formatted[0] + ":" + formatted[1];
});

//converts 24 hour time to 12 hour, remove seconds
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
        formatted[0] -= 12;
    }
    return formatted[0] + ":" + formatted[1];
});

// converts date string into 12 hour display - no am/pm
Handlebars.registerHelper("formatDateAsTime", function(date_str) {
    if (date_str === undefined || date_str.length === 0) {
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
    if (date_str === undefined || date_str.length === 0) {
        return "";
    }
    var date = date_from_string(date_str);
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

Handlebars.registerHelper("ucfirst", function(str) {
    lstr = str.toLowerCase();
    return lstr.replace(/^([a-z])/, function(match) {
        return match.toUpperCase();
    });
});

Handlebars.registerHelper("formatPrice", function(price) {
    formatted = price.toString().split(".");
    if (formatted[1] && formatted[1].length === 1) {
        formatted[1] += "0";
    }
    if (!formatted[1] || formatted[1].length === 0) {
        formatted[1] = "00";
    }
    return formatted.join(".");
});

Handlebars.registerHelper('format_schedule_hour', function(hour, position) {
    if (parseInt(hour, 10) === 12) {
        VisualScheduleCard.shown_am_marker = true;
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

// converts date string into the label for the final exams schedule
Handlebars.registerHelper("formatDateAsFinalsDay", function(date_str, days_back) {
    if (date_str === undefined || date_str.length === 0) {
            return "";
        }
    var date = moment(date_str);
    date.subtract(days_back, "days");
    return date.format("MMM D");
});


Handlebars.registerHelper('time_percentage', function(time, start, end) {
    return VisualScheduleCard.get_scaled_percentage(time, start, end);
});

Handlebars.registerHelper('time_percentage_height', function(start, end, min, max) {
    var top = VisualScheduleCard.get_scaled_percentage(start, min, max);
    var bottom = VisualScheduleCard.get_scaled_percentage(end, min, max);

    return bottom-top;
});

Handlebars.registerHelper('to_percent', function(decimal){
    return Math.round(decimal * 100);
});

Handlebars.registerHelper('show_days_meetings', function(list, start_time, end_time) {
    if (!VisualScheduleCard.day_template) {
        var day_source = $("#visual_schedule_day").html();
        var _day_template = Handlebars.compile(day_source);

        VisualScheduleCard.day_template = _day_template;
    }

    return new Handlebars.SafeString(VisualScheduleCard.day_template({ meetings: list, start_time: start_time, end_time: end_time }));
});

Handlebars.registerHelper('show_days_finals', function(list, start_time, end_time, term) {
    if (!VisualScheduleCard.day_template) {
        var day_source = $("#finals_schedule_day").html();
        var _day_template = Handlebars.compile(day_source);

        VisualScheduleCard.day_template = _day_template;
    }

    return new Handlebars.SafeString(VisualScheduleCard.day_template({ meetings: list, start_time: start_time, end_time: end_time, term: term }));
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

Handlebars.registerHelper('get_quarter_code', function(quarter_str) {
    if (arguments.length === 0 || quarter_str === undefined || quarter_str.length === 0) {
        return "";
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
});

Handlebars.registerHelper('get_quarter_abbreviation', function(quarter_str) {
    if (arguments.length === 0 || quarter_str === undefined || quarter_str.length === 0) {
        return "";
    }
    var q = quarter_str.toLowerCase();
    if(q === "winter") {
        return "WIN";
    }
    else if(q === "spring") {
        return "SPR";
    }
    else if(q === "summer") {
        return "SUM";
    }
    else if(q === "autumn") {
        return "AUT";
    }
});

Handlebars.registerHelper('slugify', function(value) {
    var slug = value.replace(/[^\w\s]+/gi, '').replace(/ +/gi, '-');
    return slug.toLowerCase();
});

Handlebars.registerHelper('shorten_meeting_type', function(str) {
    if (str.length > 4) {
        return str.substring(0, 3);
    }
    return str;
});

/********************************
* Below are {{# block helpers
********************************/

Handlebars.registerHelper("eachWithIndex", function(array, fn) {
    var buffer = "";
    for (var i = 0, j = array.length; i < j; i++) {
        var item = array[i];
        item.index = i;
        buffer += fn.fn(item);
    }
    return buffer;
});

Handlebars.registerHelper('equal', function(value1, value2, options) {
    if (arguments.length < 3) {
        throw new Error("Handlebars Helper equal needs 2 parameters");
    }
    if(value1 !== value2) {
        return options.inverse(this);
    }
    else {
        return options.fn(this);
    }
});

/**
 * The {{#exists}} helper checks if a variable is defined.
 * being 0 or null are considered defined.
 */
Handlebars.registerHelper('exists', function(variable, options) {
    if (typeof variable !== 'undefined') {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('greater_than', function(value1, value2, options) {
    if (arguments.length < 3) {
        throw new Error("Handlebars Helper greater_than needs 2 parameters");
    }
    if(value1 > value2) {
        return options.inverse(this);
    }
    else {
        return options.fn(this);
    }
});

Handlebars.registerHelper('not_first', function(index, block) {
    // display block if the index greater than 0
    if (arguments.length < 2) {
        throw new Error("Handlebars Helper not_first needs 1 parameter");
    }
    if(parseInt(index) > 0) {
        return block.fn(this);
    }
});

Handlebars.registerHelper('not_equal', function(obj, value, block) {
    if (arguments.length < 3) {
        throw new Error("Handlebars Helper not_equal needs 2 parameters");
    }
    if(obj !== value) {
        return block.fn(this);
    }
});

Handlebars.registerHelper('not_empty', function(array1, array2, options) {
    if (arguments.length < 3) {
        throw new Error("Handlebars Helper not_empty needs 2 parameters");
    }
    if (array1.length > 0 || array2.length > 0 ) {
        return options.fn(this);
    }
    return options.inverse(this);
});

Handlebars.registerHelper('if_mobile', function(options) {
    return (window.is_mobile) ? options.fn(this) : options.inverse(this);
});

Handlebars.registerHelper('protocol', function(url) {
    return window.location.protocol + '//' + url;
});

Handlebars.registerHelper('static', function(path) {
    return window.static_url + path;
});
