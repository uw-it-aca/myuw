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
    },

    add_events: function() {
        $("#modal_toggle").on('click', function(){
            $("#message_modal").attr('aria-hidden', false);
        });
        $("#modal_close").on('click', function(){
            $("#message_modal").attr('aria-hidden', true);
        });

    }
};
