var HfsCard = {
    render: function () {
        var source = $("#hfs_card_content").html();
        var template = Handlebars.compile(source);
        var hfs_data = WSData.hfs_data();
        if (!hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
            hfs_data = null
        }
        return template({'hfs_data': hfs_data});
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

};
