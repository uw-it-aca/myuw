$(document).ready(function() {
    NoticeAdmin.render()
});

var NoticeAdmin = {
    render: function() {
        $('#start_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm'});
        $('#end_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm'});
    }
};