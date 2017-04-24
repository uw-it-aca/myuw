var CommonLoading = {

    render_init: function() {
        WebServiceData.require({profile_data: new ProfileData()}, Profile.render_upon_data);
    }
};
