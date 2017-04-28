var QuickLinks = {
    add_link: function(url, label) {
        console.log("In add_link", url, label);
    },
    run_control: function(ev) {
        var target = $(this);
        console.log("In run_control", this, ev, target.attr('data-linkid'), target.attr('data-linktype'));

        return false;
    }
}

$("body").on('click', '.control-link', QuickLinks.run_control);
