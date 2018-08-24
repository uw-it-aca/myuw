var PhotoClassList = {
    is_desktop: undefined,

    hide_card: function() {
        if (window.user.instructor) {
            return false;
        }
        return true;
    },

    render: function() {
        if (PhotoClassList.hide_card()) {
            return;
        }
        showLoading();

        if (window.hasOwnProperty('section_data') &&
            window.section_data.hasOwnProperty('section')) {

            WSData.fetch_instructed_section_details(
                window.section_data.section,
                PhotoClassList.render_upon_data,
                PhotoClassList.render_error);
        }
        //PhotoClassList.make_html();
    },

    render_upon_data: function() {
        // build class list content
        var source = $("#photo_class_list").html();
        var template = Handlebars.compile(source);
        var data = WSData.instructed_section_details();
        var registrations = data.sections[0].registrations;

        data.sections[0].registrations = PhotoClassList.sort_students(
            registrations, 'surname,first_name');

        if (window.section_data.hasOwnProperty('available_sections') &&
                window.section_data.available_sections.length > 1) {
            data.available_sections = window.section_data.available_sections;
        }
        var raw = template(data);
        $("#main-content").html(raw);

        // add event handlers
        $("#download_class_list").on("click", PhotoClassList.download_list);

        $("#sort_list").on("change", function() {
            var data = WSData.instructed_section_details();
            var registrations = data.sections[0].registrations;
            var sorted = PhotoClassList.sort_students(registrations,
                                                      this.value);

            var new_body = $("<div>");
            for (var i = 0; i < sorted.length; i++) {
                var regid = sorted[i].regid;
                var student_row = $("#student_"+regid);
                new_body.append(student_row);
            }

            $("#student_sort").html(new_body.html());
        });

        $("#list_view").on("click", function(e) {
            e.preventDefault();
            $("#classlist_photogrid_view").attr("aria-hidden", true);
            $("#classlist_photogrid_view").attr("hidden", true);
            $("#classlist_table_view").attr("aria-hidden", false);
            $("#classlist_table_view").attr("hidden", false);
            $("#class-list-sort-controls").attr("aria-hidden", false);
            $("#class-list-sort-controls").attr("hidden", false);
            $("#list_view").attr("aria-selected", true);
            $("#grid_view").attr("aria-selected", false);
        });

        $("#grid_view").on("click", function(e) {
            e.preventDefault();
            $("#classlist_table_view").attr("aria-hidden", true);
            $("#classlist_table_view").attr("hidden", true);
            $("#classlist_photogrid_view").attr("aria-hidden", false);
            $("#classlist_photogrid_view").attr("hidden", false);
            $("#class-list-sort-controls").attr("aria-hidden", true);
            $("#class-list-sort-controls").attr("hidden", true);
            $("#list_view").attr("aria-selected", false);
            $("#grid_view").attr("aria-selected", true);
        });

        $("#available_sections").on("change", function() {
            window.section_data.section = $(this).val();
            PhotoClassList.render();
        }).val(window.section_data.section);

    },

    sort_students: function(registrations, key) {
        var fields = key.split(',');
        if (!registrations || !registrations.length) {
            return null;
        }
        for (var i = fields.length-1; i >= 0; i--) {
            registrations = PhotoClassList.sort_registrations(registrations,
                                                              fields[i]);
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
        var registrations = PhotoClassList.sort_students(
            data.registrations, 'surname,first_name');
        var add_qz_sect = data.has_linked_sections;
        var lines = [];
        var header = ["StudentNo","UWNetID","LastName","FirstName"];
        if (add_qz_sect) {
            header.push("Section");
            }
        header.push("Credits","Class","Major","Email");
        lines.push(header.join(","));

        for (i = 0; i < registrations.length; i++) {
            var reg = registrations[i];
            var fields = ["\t" + reg.student_number,  // MUWM-3978
                          reg.netid,
                          reg.surname,
                          reg.first_name];

            if (add_qz_sect) {
                fields.push(reg.linked_sections);
                }

            var credits = reg.is_auditor?"Audit":reg.credits;
            fields.push(credits,
                        reg.class_level,
                        PhotoClassList.combine_majors(reg.majors),
                        reg.email);

            lines.push(fields.map(PhotoClassList.quote_field).join(","));
        }
        return lines.join("\n");
    },

    download_list: function() {
        var data = WSData.instructed_section_details();
        var download = PhotoClassList.build_download(data.sections[0]);
        var blob = new Blob([download], {type: "text/csv" });

        var section = data.sections[0];
        var filename = PhotoClassList.download_name(section,
                                                    data.year,
                                                    data.quarter);
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

    download_class_list: function(section_label) {
        WSData.fetch_instructed_section_details(section_label,
                                                PhotoClassList.download_list,
                                                PhotoClassList.render_error);
    },

    render_error: function() {
        var error_code = WSData.instructed_section_details_error_code(),
            source,
            course_template;

        if (error_code === 410) {
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
if (typeof exports === "undefined") {
    var exports = {};
}
exports.PhotoClassList = PhotoClassList;
