var CriticalInfoCard = {
    name: 'CriticalInfoCard',
    dom_target: undefined,
    render_init: function () {
        WebServiceData.require({notice_data: new NoticeData()}, CriticalInfoCard.render);
    },

    render: function (resources) {
        var notice_resource = resources.notice_data;
        if (CriticalInfoCard.render_error(notice_resource.error)) {
            return;
        }

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

    render_error: function (notice_resource_error) {
        if (notice_resource_error) {
            CriticalInfoCard.dom_target.html(CardWithError.render("Update Critical Information"));
            return true;
        }

        return false;
    },
};
