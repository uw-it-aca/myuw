function MyPlanData(year, quarter) {
    this.url = "/api/v1/myplan/" + year + "/" + quarter;
    this.data = null;
    this.error = null;
}

MyPlanData.prototype.setData = WebServiceData.setData;

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.MyPlanData = MyPlanData;
