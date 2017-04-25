function NoticeData() {
    BaseData.call(this, "/api/v1/notices/");
}

NoticeData.prototype = Object.create(BaseData.prototype);

NoticeData.prototype.setData = function (data) {
    // hook notice_data resource's data to Notice module
    Notices.set_data(data);
    this.data = data;
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.NoticeData = NoticeData;
