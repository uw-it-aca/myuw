function ProfileData() {
    BaseData.call(this, "/api/v1/profile/");
}

ProfileData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.ProfileData = ProfileData;
