var CommonLoading = {

    render_init: function() {
        WSData.fetch_profile_data(Profile.render_upon_data);
    }
};
