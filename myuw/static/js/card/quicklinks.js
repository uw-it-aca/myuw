var QuickLinksCard = {
    name: 'QuickLinksCard',
    dom_target: undefined,

    run_control: function(ev) {
        var target = $(this);

        QuickLinksCard._add_link({
            type: target.attr('data-linktype'),
            id: target.attr('data-linkid')
        });

        return false;
    },
    custom_add: function(ev) {
        if (13 == ev.keyCode) {
            $("#quicklink_saving").show();
            QuickLinksCard._add_link({
                type: "custom",
                url: $("#myuw-custom-qlink").val()
            });
        }
    },
    _add_link: function(values) {
        $("#error_saving").hide();
        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        $.ajax({
            url: "/api/v1/link",
            dataType: "JSON",
            async: true,
            type: "POST",
            headers: {
                 "X-CSRFToken": csrf_token
            },
            data: JSON.stringify(values),
            complete: QuickLinksCard.redraw
        });
    },

    redraw: function(response) {
        $("#quicklink_saving").hide();
        if (response.status == 200) {
            window.quicklink_data = response.responseJSON;
            $("#myuw-custom-qlink").val("");
            QuickLinksCard.render();
        }
        else {
            $("#error_saving").show();
        }
    },

    render_init: function() {
        QuickLinksCard.dom_target = $('#QuickLinksCard');
        QuickLinksCard.render();
    },

    render: function() {
        var source = $("#quicklinks").html();
        var template = Handlebars.compile(source);

        QuickLinksCard.dom_target.html(template({
            'links': window.quicklink_data
        }));
    }
}

$("body").on('click', '.control-link', QuickLinksCard.run_control);
$("body").on('keydown', '#myuw-custom-qlink', QuickLinksCard.custom_add);
