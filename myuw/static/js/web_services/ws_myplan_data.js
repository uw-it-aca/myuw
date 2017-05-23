function MyPlanData(year, quarter) {
    BaseData.call(this, "/api/v1/myplan/" + year + "/" + quarter);
}

MyPlanData.prototype = Object.create(BaseData.prototype);

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MyPlanData = MyPlanData;
