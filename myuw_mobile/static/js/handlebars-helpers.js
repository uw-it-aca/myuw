
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

// convert term string from "2013,summer,a-term" to "summer 2013 a-term"
Handlebars.registerHelper("formatTerm", function(term) {
    value = term.split(",");
    str = value[1] + " " + value[0];
    if (value[2]) {
        str += " " + value[2];
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
    if (!formatted[1] || formatted[1].length == 0) {
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


