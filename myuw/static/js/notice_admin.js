$(document).ready(function() {
    NoticeAdmin.render();
});

var NoticeAdmin = {
    render: function() {
        var start = moment($("#start_value").html());
        $('#start_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm',
                                          date: start});
        var end = moment($("#end_value").html());
        $('#end_dt').datetimepicker({format: 'YYYY-MM-DD HH:mm',
                                        date: end});
    }
};