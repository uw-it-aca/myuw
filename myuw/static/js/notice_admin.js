$(document).ready(function() {
    NoticeAdmin.render();
});

var NoticeAdmin = {
    render: function() {
        var start = moment.utc($("#start_value").html());
        $('#start_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm',
                                       date: start});
        var end = moment.utc($("#end_value").html());
        $('#end_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm',
                                     date: end});
        NoticeAdmin.add_events();
    },

    form_action: function(notice_group_value) {
        if (notice_group_value.length === 0) {
            $('input[name="campus"]').prop('disabled', false);
            $('input[name="affil"]').prop('disabled', false);
        } else {
            $('input[name="campus"]').prop('disabled', true);
            $('input[name="affil"]').prop('disabled', true);
        }
    },

    add_events: function() {
        $(window).on("load", function() {
            NoticeAdmin.form_action($('input[id="notice_group"]').val());
        });

        $('#notice_group').on('input', function() {
            NoticeAdmin.form_action($(this).val());
        });
    }
};
