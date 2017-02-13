var PhotoClassList = {
    is_desktop: undefined,

    render: function() {
        showLoading();

        if (window.hasOwnProperty('section_data') &&
            window.section_data.hasOwnProperty('section')) {

                WSData.fetch_instructed_section_details(window.section_data.section,
                                                        PhotoClassList.render_upon_data,
                                                        PhotoClassList.render_error)
        }
        //PhotoClassList.make_html();
    },

    render_upon_data: function() {
        var source = $("#photo_class_list").html();
        var template = Handlebars.compile(source);
        console.log("Data: ", WSData.instructed_section_details());
        $("#app_content").html(template(WSData.instructed_section_details()));

        $("#download_class_list").on("click", PhotoClassList.download_list);
    },

    download_list: function() {
        var data = WSData.instructed_section_details();
        var registrations = data.sections[0].registrations;
        var lines = [];
        lines.push(["Student Number", "UW NetID", "Name", "Quiz Section", "Credits", "Class", "Major", "Email"].join(","));
        for (var i = 0; i < registrations.length; i++) {
            reg = registrations[i];
            var fields = [reg['student_number'],
                          reg['netid'],
                          reg['full_name'],
                          reg['quiz_section'],
                          reg['credits'],
                          reg['class'],
                          reg['major'],
                          reg['email']]

            var quote = function(x) {
                if (x) {
                    return '"'+x+'"';
                }
                else {
                    return '""';
                }
            }
            lines.push(fields.map(quote).join(","));
        }

        var blob = new Blob([lines.join("\n")], {type: "text/csv" });

        // from http://stackoverflow.com/questions/3665115/create-a-file-in-memory-for-user-to-download-not-through-server
        if(window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveBlob(blob, filename);
        }
        else{
            var elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(blob);
            elem.download = 'classlist.csv';
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
            $("#app_content").dom_target.html(source);
        }

    }

};
