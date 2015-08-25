var Modal = {
    html: function(content) {
        $("#page-modal").html(content);
    },

    show: function() {
        $("#page-content").hide();
        $("#page-modal").show();
    },

    hide: function() {
        $("#page-modal").hide();
        $("#page-content").show();
    }
};
