var isSingleDay = true;
var isDateRangeInited = false;

initOnedayChart("2017-12-01");

var chartOption = {
    "topRoomSingleDay": undefined,
    "topCateSingleDay": undefined,
    "topUserDanmuSingleDay": undefined,
    "topUserGiftSingleDay": undefined,
    "topUserExpenseSingleDay": undefined,
    "topRoomRange": undefined,
    "topCateRange": undefined,
    "topUserDanmuRange": undefined,
    "topUserGiftRange": undefined,
    "topUserExpenseRange": undefined
};


var jsonParser = {
    room: function (payload) {
        return {
            "room": payload.map(function (entry) {
                return entry["roomName"]
            }),
            "income": payload.map(function (entry) {
                return entry["income"]
            }),
            "gift": payload.map(function (entry) {
                return entry["gcount"]
            }),
            "danmu": payload.map(function (entry) {
                return entry["dcount"]
            }),
            "total": payload.map(function (entry) {
                return entry["factor"]
            })
        };
    },
    cate: function (payload) {
        return payload.map(function (row) {
            return {"cate": row["cateName"], "value": row["factor"]}
        })
    },
    userDanmu: function (payload) {
        return {
            "user": payload.map(function (row) {
                return row["user"]
            }),
            "danmu": payload.map(function (row) {
                return row["dcount"]
            })
        }
    },
    userGift: function (payload) {
        return {
            "user": payload.map(function (row) {
                return row["user"]
            }),
            "gift": payload.map(function (row) {
                return row["gcount"]
            })
        }
    },
    userExpense: function (payload) {
        return {
            "user": payload.map(function (row) {
                return row["user"]
            }),
            "expense": payload.map(function (row) {
                return row["expense"]
            })
        }
    }
};

function initOnedayChart(dateOneday) {
    isSingleDay = true;
    rankingOneday(dateOneday);
}

function initSomedayChart(date1, date2) {
    isSingleDay = false;
    rankingSomeday(date1, date2);
}

function restoreCharts() {
    if (isSingleDay) {
        chartOption.topRoomSingleDay.chart.setOption(chartOption.topRoomSingleDay.option);
        chartOption.topCateSingleDay.chart.setOption(chartOption.topCateSingleDay.option);
        chartOption.topUserExpenseSingleDay.chart.setOption(chartOption.topUserExpenseSingleDay.option);
        chartOption.topUserDanmuSingleDay.chart.setOption(chartOption.topUserDanmuSingleDay.option);
        chartOption.topUserGiftSingleDay.chart.setOption(chartOption.topUserGiftSingleDay.option);
    } else {
        chartOption.topRoomRange.chart.setOption(chartOption.topRoomRange.option);
        chartOption.topCateRange.chart.setOption(chartOption.topCateRange.option);
        chartOption.topUserExpenseRange.chart.setOption(chartOption.topUserExpenseRange.option);
        chartOption.topUserDanmuRange.chart.setOption(chartOption.topUserDanmuRange.option);
        chartOption.topUserGiftRange.chart.setOption(chartOption.topUserGiftRange.option);
    }
}

function changeTab(type) {
    var div1 = document.getElementById("tab1");
    var div2 = document.getElementById("tab2");
    switch (type) {
        case 1:
            div1.style.display = "block";
            div2.style.display = "none";
            isSingleDay = true;
            break;
        case 2:
            div1.style.display = "none";
            div2.style.display = "block";
            isSingleDay = false;
            break
    }

    if (!isDateRangeInited) {
        isDateRangeInited = true;
        initSomedayChart("2017-12-01", "2017-12-07");
    } else {
        restoreCharts();
    }
}


function changeDownTab(type) {
    var div1 = document.getElementById("tab1D");
    var div2 = document.getElementById("tab2D");
    var div3 = document.getElementById("tab3D");

    switch (type) {
        case 1:
            div1.style.display = "block";
            div2.style.display = "none";
            div3.style.display = 'none';

            if (isSingleDay) {
                chartOption.topUserExpenseSingleDay.chart.setOption(chartOption.topUserExpenseSingleDay.option);
            } else {
                chartOption.topUserExpenseRange.chart.setOption(chartOption.topUserExpenseRange.option);
            }

            break;
        case 2:
            div1.style.display = "none";
            div2.style.display = "block";
            div3.style.display = 'none';

            if (isSingleDay) {
                chartOption.topUserGiftSingleDay.chart.setOption(chartOption.topUserGiftSingleDay.option);
            } else {
                chartOption.topUserGiftRange.chart.setOption(chartOption.topUserGiftRange.option);
            }
            break;
        case 3:
            div1.style.display = "none";
            div2.style.display = "none";
            div3.style.display = 'block';

            if (isSingleDay) {
                chartOption.topUserDanmuSingleDay.chart.setOption(chartOption.topUserDanmuSingleDay.option);
            } else {
                chartOption.topUserDanmuRange.chart.setOption(chartOption.topUserDanmuRange.option);
            }
            break;
    }
}

function changeManner(type) {
    var dateOne = $("#input1").val();
    var date1 = $("#input2").val();
    var date2 = $("#input3").val();
    switch (type) {
        case 1:
            initOnedayChart(dateOne);
            break;
        case 2:
            initSomedayChart(date1, date2);
            break;
    }
}


//oneday请求数据
function rankingOneday(dateOne) {
    $.ajax({
        url: '/api/stat/site/top/room/' + dateOne + '?limit=10',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topRoomSingleDay = roomOnedayTopRoom(jsonParser.room(data["data"]))
        }

    });

    //请求类别排名
    $.ajax({
        url: '/api/stat/site/top/cate/' + dateOne + '?limit=10',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topCateSingleDay = onedayTopCate(jsonParser.cate(data["data"]))
        }
    });

    //请求用户弹幕排行
    $.ajax({
        url: '/api/stat/site/top/user/' + dateOne + '/danmu?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topUserDanmuSingleDay = onedayTopUserDanmu(jsonParser.userDanmu(data["data"]))
        }
    });

    //请求用户礼物数排行
    $.ajax({
        url: '/api/stat/site/top/user/' + dateOne + '/gift?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topUserGiftSingleDay = onedayTopUserGift(jsonParser.userGift(data["data"]))
        }
    });

    //请求用户花费排行
    $.ajax({
        url: '/api/stat/site/top/user/' + dateOne + '/expense?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topUserExpenseSingleDay = onedayTopUserExpence(jsonParser.userExpense(data["data"]))
        }
    });
}

//someday请求数据
function rankingSomeday(date1, date2) {
    $.ajax({
        url: '/api/stat/site/top/room/' + date1 + '/' + date2 + '?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topRoomRange = roomSomedayTopRoom(jsonParser.room(data["data"]))
        }

    });

    //请求类别排名
    $.ajax({
        url: '/api/stat/site/top/cate/' + date1 + '/' + date2 + '?limit=10',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topCateRange = SomedayTopCate(jsonParser.cate(data["data"]));
        }
    });

    //请求用户弹幕排行
    $.ajax({
        url: '/api/stat/site/top/user/' + date1 + '/' + date2 + '/danmu?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {

            chartOption.topUserDanmuRange = SomedayTopUserDanmu(jsonParser.userDanmu(data["data"]));
        }
    });

    //请求用户礼物数排行
    $.ajax({
        url: '/api/stat/site/top/user/' + date1 + '/' + date2 + '/gift?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topUserGiftRange = SomedayTopUserGift(jsonParser.userGift(data["data"]));
        }
    });

    //请求用户花费排行
    $.ajax({
        url: '/api/stat/site/top/user/' + date1 + '/' + date2 + '/expense?limit=20',
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            chartOption.topUserExpenseRange = SomedayTopUserExpense(jsonParser.userExpense(data["data"]));
        }
    });

}

//一段时间图表
function roomSomedayTopRoom(data) {
    var myChart = echarts.init(document.getElementById('leftRankingTwo'));
    var option = {
        title: {
            text: '主播排行榜',
        },
        legend: {
            show: true,
            data: ['收入', '礼物', '弹幕']
        },
        grid: {
            top: 100
        },
        angleAxis: {
            type: 'category',
            data: data.room
        },
        radiusAxis: {},
        polar: {},
        tooltip: {
            show: true,

        },
        series: [{
            type: 'bar',
            data: data.income,
            coordinateSystem: 'polar',
            name: '收入',
            stack: 'a'
        }, {
            type: 'bar',
            data: data.gift,
            coordinateSystem: 'polar',
            name: '礼物',
            stack: 'a'
        }, {
            type: 'bar',
            data: data.danmu,
            coordinateSystem: 'polar',
            name: '弹幕',
            stack: 'a'
        },]

    };

    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function SomedayTopUserDanmu(data) {
    console.table(data)
    var myChart = echarts.init(document.getElementById('rightGraph3'));
    var option = {
        title: {
            text: '用户弹幕数排行榜',
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: "{a} <br/>{b} : {c}%"
        },
        legend: {
            data: ['弹幕数']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01],
            "axisLabel": {
                "interval": 0,
                formatter: '{value}%',
            }
        },
        yAxis: {
            type: 'category',
            data: data.user
        },
        series: [{
            name: '2',
            type: 'bar',
            data: data.danmu
        }]

    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function SomedayTopUserGift(data) {
    var myChart = echarts.init(document.getElementById('rightGraph2'));
    var option = {
        backgroundColor: '#0E2A43',
        legend: {
            bottom: 20,
            textStyle: {
                color: '#fff',
            },
            data: ['花费']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },

        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        xAxis: {
            type: 'value',
            axisTick: {show: false},
            axisLine: {
                show: false,
                lineStyle: {
                    color: '#fff',
                }
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                data: data.user
            },

        ],
        series: [
            {
                name: '花费',
                type: 'bar',

                itemStyle: {
                    normal: {
                        show: true,
                        color: '#277ace',
                        barBorderRadius: 50,
                        borderWidth: 0,
                        borderColor: '#333',
                    }
                },
                barGap: '0%',
                barCategoryGap: '50%',
                data: data.gift
            }

        ]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function SomedayTopUserExpense(data) {

    var myChart = echarts.init(document.getElementById('rightGraph1'));
    var option = {
        backgroundColor: '#0E2A43',
        legend: {
            bottom: 20,
            textStyle: {
                color: '#fff',
            },
            data: ['花费']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },

        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        xAxis: {
            type: 'value',
            axisTick: {show: false},
            axisLine: {
                show: false,
                lineStyle: {
                    color: '#fff',
                }
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                data: data.user
            },

        ],
        series: [
            {
                name: '花费',
                type: 'bar',

                itemStyle: {
                    normal: {
                        show: true,
                        color: '#277ace',
                        barBorderRadius: 50,
                        borderWidth: 0,
                        borderColor: '#333',
                    }
                },
                barGap: '0%',
                barCategoryGap: '50%',
                data: data.expense
            }

        ]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function SomedayTopCate(data) {
    var myChart = echarts.init(document.getElementById('leftGraph'));
    var option = {
        "title": {
            "text": "最受欢迎类别排行榜",
            "textStyle": {
                "color": "#bcbfff",
                "fontWeight": "bold",
                "fontSize": 14
            },
            "top": "4%",
            "left": "2.2%"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": { // 坐标轴指示器，坐标轴触发有效
                "type": "shadow" // 默认为直线，可选为："line" | "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "10%",
            "bottom": "3%",
            "containLabel": true
        },
        "yAxis": [{
            "type": "category",
            "data": ["TOP10", "TOP9", "TOP8", "TOP7", "TOP6", "TOP5", "TOP4", "TOP3", "TOP2", "TOP1"],
            "axisLine": {
                "show": false
            },
            "axisTick": {
                "show": false,
                "alignWithLabel": true
            },
            "axisLabel": {
                "textStyle": {
                    "color": "#ffb069"
                }
            }
        }],
        "xAxis": [{
            "type": "value",
            "axisLine": {
                "show": false
            },
            "axisTick": {
                "show": false
            },
            "axisLabel": {
                "show": false
            },
            "splitLine": {
                "show": false
            }
        }],

        "series": [{
            "name": "弹幕数",
            "type": "bar",
            "data": data,
            "barCategoryGap": "35%",
            "label": {
                "normal": {
                    "show": true,
                    "position": "right",
                    "formatter": function (params) {
                        return params.data.cate;
                    },
                    "textStyle": {
                        "color": "#bcbfff" //color of value
                    }
                }
            },
            "itemStyle": {
                "normal": {
                    "color": new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                        "offset": 0,
                        "color": "#ffb069" // 0% 处的颜色
                    }, {
                        "offset": 1,
                        "color": "#ec2e85" // 100% 处的颜色
                    }], false)
                }
            }
        }]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

//一天的时间图表
function roomOnedayTopRoom(data) {
    var myChart = echarts.init(document.getElementById('leftRankingOne'));
    var option = {
        title: {
            text: "主播排行榜",
            textStyle: {
                color: 'black',
                fontSize: 24
            }
        },
        legend: {
            bottom: 20,
            textStyle: {
                color: 'gray',
            },
            data: ['收入', '礼物', '弹幕']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },

        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        yAxis: {
            type: 'value',
            axisTick: {
                show: false
            },
            axisLine: {
                lineStyle: {
                    color: 'black',
                    opacity:0.4
                }
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#aaa',
                }
            },
        },
        xAxis: [{
            type: 'category',
            axisTick: {
                show: false
            },
            axisLine: {
                show: true,
                lineStyle: {
                    color: 'black',
                    opacity:0.4
                }
            },
            data: data.room
        }, {
            type: 'category',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                show: false
            },
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            },
            data: data.room
        }, {
            type: 'category',
            axisLine: {
                show: false
            },
            axisTick: {
                show: false
            },
            axisLabel: {
                show: false
            },
            splitArea: {
                show: false
            },
            splitLine: {
                show: false
            },
            data: data.room
        },

        ],
        series: [{
            name: '收入',
            type: 'bar',
            itemStyle: {
                normal: {
                    show: true,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#00FFE6'
                    }, {
                        offset: 1,
                        color: '#007CC6'
                    }]),
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            label: {
                normal: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        color: 'black'
                    }
                }
            },
            barWidth: '10%',
            data: data.income
        }, {
            name: '礼物',
            type: 'bar',
            barWidth: '10%',
            itemStyle: {
                normal: {
                    show: true,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#3023AE'
                    }, {
                        offset: 1,
                        color: '#C96DD8'
                    }]),
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            label: {
                normal: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        color: 'black'
                    }
                }
            },
            data: data.gift
        }, {
            name: '弹幕',
            type: 'bar',
            barWidth: '10%',
            itemStyle: {
                normal: {
                    show: true,
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#FFFF00'
                    }, {
                        offset: 1,
                        color: '#C96DD8'
                    }]),
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            label: {
                normal: {
                    show: true,
                    position: 'top',
                    textStyle: {
                        color: 'black'
                    }
                }
            },
            barGap: '100%',
            data: data.danmu
        }

        ]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function onedayTopUserDanmu(data) {
    var myChart = echarts.init(document.getElementById('rightGraph3'));
    var option = {
        title: {
            text: '用户弹幕数排行榜',
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: "{a} <br/>{b} : {c}%"
        },
        legend: {
            data: ['弹幕数']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01],
            "axisLabel": {
                "interval": 0,
                formatter: '{value}%',
            }
        },
        yAxis: {
            type: 'category',
            data: data.user
        },
        series: [{
            name: '弹幕数',
            type: 'bar',
            data: data.danmu
        }]

    };

    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function onedayTopUserGift(data) {
    var myChart = echarts.init(document.getElementById('rightGraph2'));
    var option = {
        backgroundColor: '#0E2A43',
        legend: {
            bottom: 20,
            textStyle: {
                color: '#fff',
            },
            data: ['礼物']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },

        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        xAxis: {
            type: 'value',
            axisTick: {show: false},
            axisLine: {
                show: false,
                lineStyle: {
                    color: '#fff',
                }
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                data: data.user
            },

        ],
        series: [
            {
                name: '礼物',
                type: 'bar',

                itemStyle: {
                    normal: {
                        show: true,
                        color: '#green',
                        barBorderRadius: 50,
                        borderWidth: 0,
                        borderColor: '#333',
                    }
                },
                barGap: '0%',
                barCategoryGap: '50%',
                data: data.gift
            }

        ]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function onedayTopUserExpence(data) {
    var myChart = echarts.init(document.getElementById('rightGraph1'));
    var option = {
        backgroundColor: '#0E2A43',
        legend: {
            bottom: 20,
            textStyle: {
                color: '#fff',
            },
            data: ['花费']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
        },

        tooltip: {
            show: "true",
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
                type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        xAxis: {
            type: 'value',
            axisTick: {show: false},
            axisLine: {
                show: false,
                lineStyle: {
                    color: '#fff',
                }
            },
            splitLine: {
                show: false
            },
        },
        yAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: '#fff',
                    }
                },
                data: data.user
            },

        ],
        series: [
            {
                name: '花费',
                type: 'bar',

                itemStyle: {
                    normal: {
                        show: true,
                        color: '#277ace',
                        barBorderRadius: 50,
                        borderWidth: 0,
                        borderColor: '#333',
                    }
                },
                barGap: '0%',
                barCategoryGap: '50%',
                data: data.expense
            }

        ]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

function onedayTopCate(data) {
    var myChart = echarts.init(document.getElementById('leftGraph'));
    var option = {
        "title": {
            "text": "最受欢迎类别排行榜",
            "textStyle": {
                "color": "#bcbfff",
                "fontWeight": "bold",
                "fontSize": 14
            },
            "top": "4%",
            "left": "2.2%"
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": { // 坐标轴指示器，坐标轴触发有效
                "type": "shadow" // 默认为直线，可选为："line" | "shadow"
            }
        },
        "grid": {
            "left": "3%",
            "right": "10%",
            "bottom": "3%",
            "containLabel": true
        },
        "yAxis": [{
            "type": "category",
            "data": ["TOP10", "TOP9", "TOP8", "TOP7", "TOP6", "TOP5", "TOP4", "TOP3", "TOP2", "TOP1"],
            "axisLine": {
                "show": false
            },
            "axisTick": {
                "show": false,
                "alignWithLabel": true
            },
            "axisLabel": {
                "textStyle": {
                    "color": "#ffb069"
                }
            }
        }],
        "xAxis": [{
            "type": "value",
            "axisLine": {
                "show": false
            },
            "axisTick": {
                "show": false
            },
            "axisLabel": {
                "show": false
            },
            "splitLine": {
                "show": false
            }
        }],

        "series": [{
            "name": "弹幕数",
            "type": "bar",
            "data": data,
            "barCategoryGap": "35%",
            "label": {
                "normal": {
                    "show": true,
                    "position": "right",
                    "formatter": function (params) {
                        return params.data.cate;
                    },
                    "textStyle": {
                        "color": "#bcbfff" //color of value
                    }
                }
            },
            "itemStyle": {
                "normal": {
                    "color": new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                        "offset": 0,
                        "color": "#ffb069" // 0% 处的颜色
                    }, {
                        "offset": 1,
                        "color": "#ec2e85" // 100% 处的颜色
                    }], false)
                }
            }
        }]
    };
    myChart.setOption(option);

    return {
        chart: myChart,
        option: option
    }
}

$(function () {
    var width = $("#bottomRightParent").width();

    $("#rightGraph1").width(width * 0.98);
    $("#rightGraph2").width(width * 0.98);
    $("#rightGraph3").width(width * 0.98);
});