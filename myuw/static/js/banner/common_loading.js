var CommonLoading = {

    render_init: function() {
        WSData.fetch_uwemail_data(UwEmail.render_upon_data);
        WSData.fetch_profile_data(Profile.render_upon_data);
    }
};
