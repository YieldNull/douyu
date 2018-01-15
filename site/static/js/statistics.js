zip = rows => rows[0].map((_, c) => rows.map(row => row[c]));

initSite('2017-12-14');

var charts = {
    graph1: echarts.init(document.getElementById("graph1")),
    graph2: echarts.init(document.getElementById("graph2")),
    graph4: echarts.init(document.getElementById("graph4")),
    graph5: echarts.init(document.getElementById("graph5")),
    graph6: echarts.init(document.getElementById("graph6")),
    graph7: echarts.init(document.getElementById("graph7")),
    graph8: echarts.init(document.getElementById("graph8"))
};

function initSite(date) {
    $.ajax({
        url: '/api/stat/site/hourly/' + date,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            const payload = data["data"];

            drawSiteHourlyStat({
                "hour": payload.map(row => row["hour"]),
                "dcount": payload.map(row => row["dcount"]),
                "gcount": payload.map(row => row["gcount"]),
                "ucount": payload.map(row => row["ucount"]),
                "ducount": payload.map(row => row["ducount"]),
                "gucount": payload.map(row => row["gucount"]),
                "income": payload.map(row => row["income"])
            });

            drawSiteHourlyDanmuRate(payload.map(row => ({"name": "" + row["hour"], "value": row["dcount"]})));
        }
    });

    $.ajax({
        url: `/api/stat/cate/daily/${date}`,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            const payload = data["data"];

            drawCateIncomeCorrespondingToUsers(payload.map(cate =>
                [(cate["ucount"] / 10000).toFixed(2), (cate["income"] / 100000000).toFixed(2), cate["rcount"], cate["cate"]]));
        }
    });

    $.ajax({
        url: `/api/stat/cate/hourly/${date}/danmu`,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            drawSiteHourlyDanmuCountOfTopCate(zip(data["data"].map(cate => cate["data"].map(row => row["dcount"]))),
                data["data"].map(cate => ({
                    "text": cate["cate"],
                    "max": Math.max(...cate["data"].map(row => row["dcount"])),
                    "min": Math.min(...cate["data"].map(row => row["dcount"]))
                })));
        }
    });

    $.ajax({
        url: `/api/stat/weekly/hourly/${date}`,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            var payload = data["data"];

            Array.prototype.flatMap = function (lambda) {
                return Array.prototype.concat.apply([], this.map(lambda));
            };

            drawWeeklyHourly(payload.flatMap((day, d) => day["data"].map((r, h) => [d, 24 - h, r["ucount"]])),
                payload.map(day => day["weekday"]), payload.map(day => day["date"]))
        }
    });

    $.ajax({
        url: `/api/stat/site/hourly/${date}`,
        type: 'GET',
        contentType: 'application/json',
        success: function (data) {
            let payload = data["data"];

            drawUserHourlyCountWhoSendDanmu(payload.map(row => ({"name": row["hour"], "value": row["ducount"]}))); // 每小时发弹幕的用户数

            drawSiteHourlyIncome(payload.map(row => ({"name": "" + row["hour"], "value": row["income"]})));
        }

    });
}


function drawSiteHourlyStat(data) {
    var option = {
        backgroundColor: "#FFFFFF",
        title: {
            text: '每小时数据总览'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985'
                }
            }
        },
        legend: {
            data: ['总用户数', '发礼物用户数', '发弹幕用户数', '礼物总数', '弹幕总数', '全站收入']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: data.hour
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '总用户数',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.ucount
            },
            {
                name: '发礼物用户数',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.gucount
            },
            {
                name: '发弹幕用户数',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.ducount
            },
            {
                name: '礼物总数',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.gcount
            },
            {
                name: '弹幕总数',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.dcount
            },
            {
                name: '全站收入',
                type: 'line',
                stack: '总量',
                areaStyle: {normal: {}},
                data: data.income
            },

        ]
    };

    charts.graph1.setOption(option, true);
}

function drawSiteHourlyDanmuRate(data) {
    var option = {
        backgroundColor: "#ffffff",
        title: {
            text: '每个时段弹幕数占比',
            x: 'center',
            top: 20,
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '弹幕数',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: data,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    charts.graph2.setOption(option, true)

}

function drawSiteHourlyDanmuCountOfTopCate(data, indicator) {

    var option = {
        backgroundColor: '#ffffff',
        title: {
            text: '每小时每个类别弹幕数',
            top: 10,
            left: 10
        },
        tooltip: {
            trigger: 'item',
            backgroundColor: 'rgba(0,0,250,0.2)'
        },
        legend: {
            type: 'scroll',
            bottom: 10,
            data: (function () {
                var list = [];
                for (var i = 0; i <= 23; i++) {
                    list.push(i + '点');
                }
                return list;
            })()
        },
        visualMap: {
            top: 'middle',
            right: 10,
            color: ['red', 'yellow'],
            calculable: true,
            max: Math.max(...indicator.map(r => r['max'])),
            min: Math.max(...indicator.map(r => r['min'])),
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {}
            }
        },
        radar: {
            indicator: indicator
        },
        series: (function () {
            var series = [];
            for (var i = 0; i <= 23; i++) {
                series.push({
                    name: i + "点",
                    type: 'radar',
                    symbol: 'none',
                    itemStyle: {
                        normal: {
                            lineStyle: {
                                width: 1
                            }
                        },
                        emphasis: {
                            areaStyle: {color: 'rgba(0,250,0,0.3)'}
                        }
                    },
                    data: [
                        {
                            value: data[i],
                            name: i + "点"
                        }
                    ]
                });
            }
            return series;
        })()
    };

    charts.graph4.setOption(option, true)
}


function drawUserHourlyCountWhoSendDanmu(data) {

    var labelData = [];
    for (var i = 0; i < 24; ++i) {
        labelData.push({
            value: 1,
            name: i + '时'
        });
    }
    var option = {
        backgroundColor: '#ffffff',
        title: {
            text: '每小时发弹幕用户数',
            left: 10,
        },
        color: ['#22C3AA'],
        tooltip: {
            show: true
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {}
            }
        },
        series: [{
            type: 'pie',
            data: data,
            roseType: 'area',
            itemStyle: {
                normal: {
                    color: 'white',
                    borderColor: '#22C3AA'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            label: {
                normal: {
                    show: false
                }
            }
        }, {
            type: 'pie',
            data: labelData,
            radius: ['72%', '95%'],
            zlevel: -2,
            itemStyle: {
                normal: {
                    color: '#22C3AA',
                    borderColor: 'white'
                }
            },
            label: {
                normal: {
                    position: 'inside',
                }
            }
        }]
    };

    charts.graph6.setOption(option, true)
}

function drawSiteHourlyIncome(data1) {
    var option = {
        title: {
            text: '每小时全站收入',
            left: 'center'
        },
        backgroundColor: '#ffffff',
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)",
        },
        toolbox: {
            feature: {
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '每小时全站收入',
                type: 'pie',
                radius: ['42%', '55%'],
                color: ['#d74e67', '#0092ff', '#eba954', '#21b6b9', '#60a900', '#01949b', ' #f17677'],
                // label: {
                //     normal: {
                //         formatter: '{b}\n{d}%'
                //     },
                // },
                data: data1
            }
        ]
    };

    charts.graph7.setOption(option, true)
}


function drawWeeklyHourly(data, weekday, dates) {

    function renderItem(params, api) {
        var values = [api.value(0), api.value(1)];
        var coord = api.coord(values);
        var size = api.size([1, 1], values);
        return {
            type: 'sector',
            shape: {
                cx: params.coordSys.cx,
                cy: params.coordSys.cy,
                r0: coord[2] + size[0] / 2,
                r: coord[2] - size[0] / 2,
                startAngle: Math.PI + coord[3] - size[1] / 2,
                endAngle: Math.PI + coord[3] + size[1] / 2
            },
            style: api.style({
                fill: api.visual('color')
            })
        };
    }

    var hours = ['0', '1', '2', '3', '4', '5', '6',
        '7', '8', '9', '10', '11',
        '12', '13', '14', '15', '16', '17',
        '18', '19', '20', '21', '22', '23'];

    var days_map = {
        6: "周日", 5: "周六", 4: "周五",
        3: "周四", 2: "周三", 1: "周二", 0: "周一"
    };

    var days = weekday.map(w => days_map[w]);

    var maxValue = echarts.util.reduce(data, function (max, item) {
        return Math.max(max, item[2]);
    }, -Infinity);
    var minValue = echarts.util.reduce(data, function (min, item) {
        return Math.min(min, item[2]);
    }, +Infinity);

    option = {
        backgroundColor: '#ffffff',
        title: {text: "近一周每小时活跃用户数"},
        polar: {},
        tooltip: {
            formatter: param => `${dates[param.value[0]]} ${24 - param.value[1]}时<br>用户数：${param.value[2]}`
        },
        visualMap: {
            type: 'continuous',
            min: minValue,
            max: maxValue,
            top: 'middle',
            dimension: 2,
            calculable: true
        },
        angleAxis: {
            type: 'category',
            data: hours,
            boundaryGap: false,
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#ddd',
                    type: 'dashed'
                }
            },
            axisLine: {
                show: false
            }
        },
        radiusAxis: {
            type: 'category',
            data: days,
            z: 100
        },
        series: [{
            name: '活跃用户数',
            type: 'custom',
            coordinateSystem: 'polar',
            itemStyle: {
                normal: {
                    color: '#d14a61'
                }
            },
            renderItem: renderItem,
            data: data,
        }],
    };

    charts.graph5.setOption(option, true)
}

function drawCateIncomeCorrespondingToUsers(data) {
    console.log(data);

    var option = {
        backgroundColor: '#ffffff',
        title: {
            text: '直播间分类全天收入与活跃用户数的关系'
        },
        tooltip: {
            formatter: param => `分类：${param.value[3]}<br/>房间数：${param.value[2]}<br/>用户数：${param.value[0]}百万<br/>收入：${param.value[1]}亿<br/>`
        },
        xAxis: {
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },

            name: '用户数/百万',
        },
        yAxis: {
            name: '收入/亿鱼元',
            axisLabel: {
                formatter: '{value}'
            },
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            },
            scale: true
        },
        series: [{
            name: '直播间分类',
            data: data,
            type: 'scatter',
            symbolSize: function (data) {
                return data[2] / 3;//Math.sqrt(data[2]) / 5e2;
            },
            label: {
                emphasis: {
                    show: true,
                    formatter: function (param) {
                        return param.data[3];
                    },
                    position: 'top'
                }
            },
            itemStyle: {
                normal: {
                    shadowBlur: 10,
                    shadowColor: 'rgba(120, 36, 50, 0.5)',
                    shadowOffsetY: 5,
                    color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                        offset: 0,
                        color: 'rgb(251, 118, 123)'
                    }, {
                        offset: 1,
                        color: 'rgb(204, 46, 72)'
                    }])
                }
            }
        }]
    };

    charts.graph8.setOption(option);
}