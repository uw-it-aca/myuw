var HfsCard = {
    render: function (hfs_notices) {
        var source = $("#hfs_card").html();
        var template = Handlebars.compile(source);
        return template(WSData.hfs_data());
    },

};
