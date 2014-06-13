var HfsCard = {
    render: function () {
        var source = $("#hfs_card").html();
        var template = Handlebars.compile(source);
        var hfs_data = WSData.hfs_data();
        if (hfs_data && !hfs_data.student_husky_card && !hfs_data.employee_husky_card && !hfs_data.resident_dining) {
            hfs_data = null
        }
        return template({'hfs_data': hfs_data});
    },

};
