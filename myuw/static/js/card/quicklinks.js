var KEY_ENTER = 13;
var KEY_ESCAPE = 27;

var QuickLinksCard = {
    name: 'QuickLinksCard',
    dom_target: undefined,

    run_control: function(ev) {
        var target = $(this);
        var type = target.attr('data-linktype');

        if ("edit" == type) {
            return QuickLinksCard.display_edit_field(target);
        }

        QuickLinksCard._add_link({
            type: type,
            id: target.attr('data-linkid')
        });

        return false;
    },
    display_edit_field: function(target) {
        var link_id = target.attr('data-linkid');
        var id = "#custom-link-"+link_id;
        var custom_link = $(id);

        $("#custom-link-edit-id").val(link_id);
        $("#custom-link-edit-url").val(custom_link.attr('href'));
        $("#custom-link-edit-label").val(custom_link.text());

        var target_pos = target.closest('li').position();
        $("#custom-link-edit").css({left: target_pos.left, top: target_pos.top + 20});
        $("#custom-link-edit").show();

        $("#custom-link-edit-url").focus();
    },
    custom_add: function(ev) {
        if (KEY_ENTER == ev.which) {
            QuickLinksCard._save_new();
        }
    },
    _save_new: function() {
        $("#quicklink_saving").show();
        QuickLinksCard._add_link({
            type: "custom",
            url: $("#myuw-custom-qlink").val().trim()
        });
    },
    custom_edit: function(ev) {
        if (KEY_ENTER == ev.which) {
            QuickLinksCard._save_edit();
        }
    },
    _save_edit: function() {
        var label = $("#custom-link-edit-label").val().trim();
        if ("" === label) {
            $("#edit-label-required").show();
        }
        else {
            $("#edit-label-required").hide();
        }

        var csrf_token = $("input[name=csrfmiddlewaretoken]")[0].value;
        var values = {
            type: "custom-edit",
            url: $("#custom-link-edit-url").val(),
            label: label,
            id: $("#custom-link-edit-id").val()
        };

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

        return false;
    },
    handle_escape: function(ev) {
        if (KEY_ESCAPE == ev.which) {
            QuickLinksCard.hide_edit_panel();
        }
    },
    hide_edit_panel: function() {
        $("#custom-link-edit").hide();
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
};

$("body").on('click', '.control-link', QuickLinksCard.run_control);
$("body").on('click', '#close-custom-link-edit', QuickLinksCard.hide_edit_panel);
$("body").on('click', '#quicklinks-save-edits', QuickLinksCard._save_edit);
$("body").on('click', '#quicklinks-save-new', QuickLinksCard._save_new);
$("body").on('keydown', '#myuw-custom-qlink', QuickLinksCard.custom_add);
$("body").on('keydown', '#custom-link-edit', QuickLinksCard.custom_edit);
$("body").on('keydown', QuickLinksCard.handle_escape);
