var CriticalInfoCard = {
    name: 'CriticalInfoCard',
    dom_target: undefined,
    render_init: function () {
        WSData.fetch_notice_data(CriticalInfoCard.render_upon_data, CriticalInfoCard.render_error);
    },
    render_upon_data: function () {
        if (!CriticalInfoCard._has_all_data()) {
            return;
        }
        CriticalInfoCard._render();
    },

    _has_all_data: function () {
        if (WSData.notice_data()) {
            return true;
        }
        return false;
    },

    _render: function () {
        var source = $("#ns_critical_info").html();
        var template = Handlebars.compile(source);
        var notices = Notices.get_notices_for_tag("checklist_email");
        var residency_notices = Notices.get_notices_for_tag("checklist_residence");
        // Assume they're a resident if we don't get status?
        var is_resident = true;

        if (residency_notices.length > 0){
            $.each(residency_notices[0].attributes, function(idx, attr){
                if (attr.name === "ResidencyStatus"){
                    if (attr.value !== "1" && attr.value !== "2"){
                        is_resident = false;
                    }
                }
            });

        }

        if (ToRegisterCard.has_to_register_notices()){
            CriticalInfoCard.dom_target.html(template({'notices': notices,
                                                       'is_resident': is_resident}));
        } else {
            CriticalInfoCard.dom_target.hide();
        }
        LogUtils.cardLoaded(CriticalInfoCard.name, CriticalInfoCard.dom_target);

    },
    render_error: function () {
        CriticalInfoCard.dom_target.html(CardWithError.render(CriticalInfoCard.name));
    },
};
