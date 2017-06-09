$("#added_popular input").on('change', function() {
    var campus = $("#added_popular input[name='campus']:checked").val();
    var affiliation = $("#added_popular input[name='affiliation']:checked").val();
    var require_pce = $("#added_popular input[name='pce']:checked").length;

    $(".curated_popular_link").show();

    if (campus) {
        $(".curated_popular_link[data-campus][data-campus!='"+campus+"']").hide();
    }
    if (affiliation) {
        $(".curated_popular_link[data-affiliation][data-affiliation!='"+affiliation+"']").hide();
    }
    if (require_pce) {
        $(".curated_popular_link[data-pce!='yes']").hide();
    }

});
