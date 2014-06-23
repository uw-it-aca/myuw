var HfsCard = {
    render: function () {
        var source = $("#hfs_card_content").html();
        var template = Handlebars.compile(source);
        var hfs_data = WSData.hfs_data();
        var template_data;
        if (!hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
            template_data = {hfs_data: null};
        } else {
            template_data = {
                hfs_data: hfs_data,
                is_only_one_card: HfsCard.is_only_one_card(hfs_data),
                is_total_two_cards: HfsCard.is_total_two_cards(hfs_data),
            };
        }
        return template(template_data);
    },


    render_init: function() {
        if (!WSData.hfs_data()) {
            return CardLoading.render("HFS");
        }
        return HfsCard.render();
    },

    render_upon_data: function() {
        var html_content = HfsCard.render();
        $("#hfs_card").html(html_content);
    },

    is_only_one_card: function(hfs_data) {
        return (hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining || !hfs_data.student_husky_card && hfs_data.employee_husky_card && !hfs_data.resident_dining || !hfs_data.student_husky_card && !hfs_data.employee_husky_card && hfs_data.resident_dining);
    },

    is_total_two_cards: function(hfs_data) {
        return (hfs_data.student_husky_card && hfs_data.employee_husky_card && !hfs_data.resident_dining || !hfs_data.student_husky_card && hfs_data.employee_husky_card && hfs_data.resident_dining || hfs_data.student_husky_card && !hfs_data.employee_husky_card && hfs_data.resident_dining);
    },
};
