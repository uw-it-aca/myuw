var RenderPage = function () {
    $("#app_navigation").show();

    // set search term in input field
    var input = $("#search-results-page"),
        search_term = getUrlParameter("q");
    $(input).val(search_term);
};
