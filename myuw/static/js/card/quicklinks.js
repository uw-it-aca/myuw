var KEY_ENTER = 13;
var KEY_ESCAPE = 27;

var QuickLinksCard = {
    name: 'QuickLinksCard',
    dom_target: undefined,
    opened_panels: {},
    hidden_panel: undefined,

    run_control: function(ev) {
        var target = $(this);
        var type = target.attr('data-linktype');

        if ("edit" == type) {
            QuickLinksCard.display_edit_field(target);
            return false;
        }
        if ("remove" == type) {
            QuickLinksCard.hide_edit_panel();
        }

        QuickLinksCard._add_link({
            type: type,
            id: target.attr('data-linkid')
        });

        return false;
    },
    display_edit_field: function(target) {
        QuickLinksCard.display_edit_links();
        QuickLinksCard.hidden_panel = target.parent();
        QuickLinksCard.hidden_panel.css('display', 'none');
        var link_id = target.attr('data-linkid');
        var id = "#custom-link-"+link_id;
        var custom_link = $(id);

        $("#edit-label-required").hide();
        $("#edit-url-required").hide();
        $("#custom-link-edit-id").val(link_id);
        $("#custom-link-edit-url").val(custom_link.attr('href'));
        $("#custom-link-edit-label").val(custom_link.text());

        var target_pos = target.closest('li').position();
        $("#custom-link-edit").css({left: 0, top: target_pos.top + 20});
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
    _post_custom_edit_save: function(response) {
        if (response.status == 200) {
            QuickLinksCard.redraw(response);
            QuickLinksCard.hide_edit_panel();
        }
        QuickLinksCard.hide_custom_quicklinks_panel();
    },
    _save_edit: function() {
        function validate(field) {
            var value = $("#custom-link-edit-"+field).val().trim();
            if ("" === value) {
                $("#edit-"+field+"-required").show();
            }
            else {
                $("#edit-"+field+"-required").hide();
            }
        }
        validate("label");
        validate("url");

        var label = $("#custom-link-edit-label").val().trim();

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
            complete: QuickLinksCard._post_custom_edit_save
        });

        return false;
    },
    handle_escape: function(ev) {
        if (KEY_ESCAPE == ev.which) {
            QuickLinksCard.hide_edit_panel();
        }
    },
    display_edit_links: function() {
        if (QuickLinksCard.hidden_panel) {
            QuickLinksCard.hidden_panel.css('display', '');
        }
    },
    hide_edit_panel: function() {
        $("#custom-link-edit").hide();
        QuickLinksCard.display_edit_links();
        return false;
    },
    hide_custom_quicklinks_panel: function() {
        $("#custom_qlinks").collapse({toggle: false});
        $("#custom_qlinks").collapse("hide");
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
            var html = $(QuickLinksCard.get_html());
            var replace_ids = ['#popular_qlinks', '.myuw-qlinks-active', '.myuw-qlinks-recent',
                               '#custom-link-edit', '#custom_qlinks'];
            var i = 0;
            for (i = 0; i < replace_ids.length; i++) {
                var id = replace_ids[i];
                $(id).html(html.find(id).html());
            }
        }
        else {
            $("#error_saving").show();
        }
    },

    render_init: function() {
        QuickLinksCard.render();
    },

    get_html: function() {
        var source = $("#quicklinks").html();
        var template = Handlebars.compile(source);
        return template({
            'links': window.quicklink_data
        });
    },

    render: function() {
        QuickLinksCard.dom_target.html(QuickLinksCard.get_html());
        QuickLinksCard.add_events();
    },
    collapse_event: function(caller) {
        // Closing a collapse that hasn't been opened at least once results in
        // a regex error in jquery code...
        if ("popular" == caller) {
            if (QuickLinksCard.opened_panels.custom) {
                $("#custom_qlinks").collapse("hide");
            }
        }
        if ("custom" == caller) {
            if (QuickLinksCard.opened_panels.popular) {
                $("#popular_qlinks").collapse("hide");
            }
        }
        QuickLinksCard.opened_panels[caller] = true;
    },
    add_events: function() {
        if (QuickLinksCard.events_added) {
            return;
        }
        QuickLinksCard.events_added = true;

        $("#popular_qlinks").on("show.bs.collapse", function() { QuickLinksCard.collapse_event('popular'); });
        $("#custom_qlinks").on("show.bs.collapse", function() { QuickLinksCard.collapse_event('custom'); });
        $("body").on('click', '.control-link', QuickLinksCard.run_control);
        $("body").on('click', '#close-custom-link-edit', QuickLinksCard.hide_edit_panel);
        $("body").on('click', '#quicklinks-save-edits', QuickLinksCard._save_edit);
        $("body").on('click', '#quicklinks-save-new', QuickLinksCard._save_new);
        $("body").on('keydown', '#myuw-custom-qlink', QuickLinksCard.custom_add);
        $("body").on('keydown', '#custom-link-edit', QuickLinksCard.custom_edit);
        $("body").on('keydown', QuickLinksCard.handle_escape);
    }
};


