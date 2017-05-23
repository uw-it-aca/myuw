function MessageData() {
    BaseData.call(this, "/api/v1/messages/");
}

MessageData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MessageData = MessageData;
