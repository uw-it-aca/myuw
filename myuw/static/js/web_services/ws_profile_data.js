function ProfileData() {
    this.url = "/api/v1/profile/";
    this.data = null;
    this.error = null;
}

ProfileData.prototype.setData = function(data) {
    // normlized data

    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ProfileData = ProfileData;
