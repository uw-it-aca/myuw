var ACourseCard = {

    render: function (term, c_section) {
        var source = $("#course_card_strut").html();
        var template = Handlebars.compile(source);
        var raw = template(c_section);
        $('#course_card_container' + c_section.index).html(raw);
    }
};
