var PhotoClassList = {
    is_desktop: undefined,

    render: function() {
        showLoading();

        if (window.hasOwnProperty('section_data') &&
            window.section_data.hasOwnProperty('section')) {

                WSData.fetch_instructed_section_details(window.section_data.section,
                                                        PhotoClassList.render_upon_data,
                                                        PhotoClassList.render_error);
        }
        //PhotoClassList.make_html();
    },

    render_upon_data: function() {
        var source = $("#photo_class_list").html();
        var template = Handlebars.compile(source);

        var data = WSData.instructed_section_details();
        data.sections[0].registrations = PhotoClassList.sort_students('surname,name');
        $("#app_content").html(template(data));

        $("#download_class_list").on("click", PhotoClassList.download_list);

        $("#sort_list").on("change", function() {
            var sorted = PhotoClassList.sort_students(this.value);

            var new_div = $("<div>");
            for (var i = 0; i < sorted.length; i++) {
                var regid = sorted[i].regid;
                var student_div = $("#student_"+regid);
                new_div.append(student_div);
            }

            $("#student_list").html(new_div.html());
        });
    },

    sort_students: function(key) {
        var data = WSData.instructed_section_details();
        var registrations = data.sections[0].registrations;

        var fields = key.split(',');
        for (var i = fields.length-1; i >= 0; i--) {
            registrations = PhotoClassList.sort_registrations(registrations, fields[i]);
        }
        return registrations;
    },

    sort_registrations: function(registrations, key) {

        var sorted = registrations.sort(function(a, b) {
            var av = a[key];
            var bv = b[key];

            if (av === undefined && bv !== undefined) {
                return 1;
            }
            if (av !== undefined && bv === undefined) {
                return -1;
            }
            // A guess at what sorting majors looks like
            try {
                av = av.map(function(x) { return x.full_name; }).join(",");
                bv = bv.map(function(x) { return x.full_name; }).join(",");
            }
            catch(exception) {
            }

            if (av > bv) {
                return 1;
            }
            if (av < bv) {
                return -1;
            }
            return 0;
        });

        return sorted;
    },

    download_name: function(section, year, quarter) {
        var base_name = section.curriculum_abbr+"_"+section.course_number+"_"+section.section_id+"_"+quarter+"_"+year+"_students.csv";

        return base_name.replace(/[^a-z0-9\._]/ig, '_');
    },

    quote_field: function(x) {
        if (x) {
            x = x.replace(/"/g, '\\"');
            return '"'+x+'"';
        }
        else {
            return '""';
        }
    },

    combine_majors: function(list) {
        if (list) {
            return list.map(function(x) { return x.full_name; }).join(", ");
        }
        return "";
    },

    build_download: function(data) {
        var registrations = PhotoClassList.sort_registrations(data.registrations, 'name');
        var lines = [];
        lines.push(["Student Number", "UW NetID", "Name", "Last Name", "Quiz Section", "Credits", "Class", "Majors", "Email"].join(","));
        for (var i = 0; i < registrations.length; i++) {
            reg = registrations[i];
            var fields = [reg.student_number,
                          reg.netid,
                          reg.name,
                          reg.surname,
                          reg.quiz_section,
                          reg.credits,
                          reg.class,
                          PhotoClassList.combine_majors(reg.majors),
                          reg.email];

            lines.push(fields.map(PhotoClassList.quote_field).join(","));
        }
        return lines.join("\n");
    },

    download_list: function() {
        var data = WSData.instructed_section_details();

        var download = PhotoClassList.build_download(data.sections[0]);
        var blob = new Blob([download], {type: "text/csv" });

        var section = data.sections[0];
        var filename = PhotoClassList.download_name(section, data.year, data.quarter);
        // from http://stackoverflow.com/questions/3665115/create-a-file-in-memory-for-user-to-download-not-through-server
        if(window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveBlob(blob, filename);
        }
        else {
            var elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(blob);

            elem.download = filename;
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
        }

        return false;
    },

    render_error: function() {
        var error_code = WSData.instructed_section_details_error_code(),
            source,
            course_template;

        if (error_code == 410) {
            Error410.render();
            return;
        }

        if (error_code === 403) {
            source = $("#instructor_section_card_not_instructor").html();
            courses_template = Handlebars.compile(source);
            $("#app_content").html(courses_template());
        } else if (error_code === 404) {
            source = $("#instructor_section_card_no_course").html();
            courses_template = Handlebars.compile(source);
            $("#app_content").html(courses_template());
        } else {
            source = CardWithError.render("Teaching Section");
            $("#app_content").html(source);
        }

    }

};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.PhotoClassList = PhotoClassList;
