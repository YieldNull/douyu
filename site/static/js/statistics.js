//initSite('2017-12-01');
function initSite(vall){
    initTotalSite(vall);
};

function initTotalSite(vall){
    getTotalSite(vall);
};
function initUserAction(vall){
    getUserAction(vall);
};
function initRoomAction(vall){
    getRoomAction(vall);
}

function getTotalSite(date){
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
            danmuTrend(data);
            danmuRate(data,data.total);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             giftTrend(data);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             hourCateDanmu(data);
        }

    });
};
function getUserAction(date){
      $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
            userGiftTrend(data);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             hourCateGiftUser(data);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             userDanmuTrend(data);
             userExpense(data);
        }

    });
};
function getRoomrAction(date){
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
            incomeTrend(data);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             hourMaxIncomeCateRate(data);
              hourMaxIncomeRoomTrend(data);
        }

    });
    $.ajax({
        url:'',
        type:'GET',
        contentType:'application/json',
        success:function (data) {
             hourCateIncome(data);
        }

    });
};


var data= {
    "time": ['00:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', "22:00", "23:00"],
    "danmu": [100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200],
    "gift":[100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200,100,200,300,400,500,100],
    "income":[100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200,100,200,300,400,500,100]
}
var data2=[[100,200,300,400,500],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100]
,[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100]
,[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100],[100,500,300,200,100]]
var data1=[{value:335, name:'1:00'},
                {value:310, name:'2:00'},
                {value:274, name:'3:00'},
                {value:235, name:'4:00'},
                {value:400, name:'5:00'},
{value:335, name:'1:00'},
                {value:310, name:'6:00'},
                {value:274, name:'7:00'},
                {value:235, name:'8:00'},
                {value:400, name:'9:00'},{value:335, name:'10:00'},
                {value:310, name:'11:00'},
                {value:274, name:'12:00'},
                {value:235, name:'13:00'},
                {value:400, name:'14:00'},{value:335, name:'15:00'},
                {value:310, name:'16:00'},
                {value:274, name:'17:00'},
                {value:235, name:'18:00'},
{value:335, name:'19:00'},
                {value:310, name:'20:00'},
                {value:274, name:'21:00'},
                {value:235, name:'22:00'},
                {value:400, name:'23:00'}]
//danmuTrend(data);
//danmuRate(data,data1);
//giftTrend(data);
//hourCateDanmu(data,data2)


function danmuTrend(data){
    var myChart=echarts.init(document.getElementById('graph1'));

var option = {
   backgroundColor:"#FFFFFF",
    tooltip: {
        trigger: 'axis',
        position: function (pt) {
            return [pt[0], '10%'];
        }
    },
    title: {
        left: 'center',
        text: '分时段弹幕面积图',
    },
    toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: data.time
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%']
    },
    series: [
        {
            name:'弹幕数',
            type:'line',
            smooth:true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                normal: {
                    color: 'rgb(255, 70, 131)'
                }
            },
            areaStyle: {
                normal: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 158, 68)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 70, 131)'
                    }])
                }
            },
            data: data.danmu
        }
    ]
};
myChart.setOption(option);
};
function danmuRate(data,data1){
    var myChart=echarts.init(document.getElementById("graph2"));
  var  option = {
      backgroundColor:"#ffffff",
    title : {
        text: '每个时段弹幕数占比',
        x:'center',
        top:20,
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
      toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    series : [
        {
            name: '弹幕数',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:data1,
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

  myChart.setOption(option)

};
function giftTrend(data){
    var myChart=echarts.init(document.getElementById("graph3"));
     var option = {
         backgroundColor:"#ffffff",
    title:{
        text:'礼物数趋势',
        left:"center"
    },
	tooltip: { //提示框组件
		trigger: 'axis',
		formatter: '{b}<br />{a0}: {c0}<br />{a1}: {c1}',
		axisPointer: {
			type: 'shadow',
			label: {
				backgroundColor: '#6a7985'
			}
		},
		textStyle: {
			color: '#fff',
			fontStyle: 'normal',
			fontFamily: '微软雅黑',
			fontSize: 12,
		}
	},
         toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
	xAxis: [
		{
			type: 'category',
			boundaryGap: true,//坐标轴两边留白
			data: data.time,
			axisLabel: { //坐标轴刻度标签的相关设置。
				interval: 1,//设置为 1，表示『隔一个标签显示一个标签』
				margin:15,
				textStyle: {
					fontStyle: 'normal',
					fontFamily: '微软雅黑',
					fontSize: 12,
				}
			},
			axisLine:{//坐标轴轴线相关设置
				lineStyle:{
					color:'#696969',
					opacity:0.4
				}
			},
		}
	],
	yAxis: [
		{
			type: 'value',
			splitNumber: 5,
			axisLabel: {
				textStyle: {
					fontStyle: 'normal',
					fontFamily: '微软雅黑',
					fontSize: 12,
				}
			},
			axisLine:{
			lineStyle:{
					color:'#696969',
					opacity:0.4
				}
			},
			axisTick:{
				show: false
			},
			splitLine: {
				show: true,
				lineStyle: {
					color: ['#fff'],
					opacity:0.06
				}
			}

		}
	],

    series : [
        {
            name:'礼物数',
            type:'bar',
            data:data.gift,
            barWidth: 10,
            barGap:0,//柱间距离
            label: {//图形上的文本标签
                normal: {
                   show: true,
                   position: 'top',
                   textStyle: {
                       color: '#696969',
                       fontStyle: 'normal',
                       fontFamily: '微软雅黑',
                       fontSize: 12,
                   },
                },
            },
            itemStyle: {//图形样式
                normal: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#83bff6'
                    }, {
                        offset: 1,
                        color: '#188df0'
                    }])
                },
            },
        }
    ]
};
     myChart.setOption(option)
};
function hourCateDanmu(data,data1){
    var myChart=echarts.init(document.getElementById("graph4"));
  var  option = {
      backgroundColor:'#ffffff',
    title: {
        text: '每小时每个类别弹幕数',
        top:10,
        left:10
    },
    tooltip: {
        trigger: 'item',
        backgroundColor : 'rgba(0,0,250,0.2)'
    },
    legend: {
        type: 'scroll',
        bottom: 10,
        data: (function (){
            var list = [];
            for (var i = 1; i <=24; i++) {
                list.push(i + '点 '+ '');
            }
            return list;
        })()
    },
    visualMap: {
        top: 'middle',
        right: 10,
        color: ['red', 'yellow'],
        calculable: true
    },
      toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    radar: {
       indicator : [
           { text: 'IE8-', max: 400},
           { text: 'IE9+', max: 400},
           { text: 'Safari', max: 400},
           { text: 'Firefox', max: 400},
           { text: 'Chrome', max: 400}
        ]
    },
    series : (function (){
        var series = [];
        for (var i = 1; i <= 24; i++) {
            series.push({
                name:'浏览器（数据纯属虚构）',
                type: 'radar',
                symbol: 'none',
                itemStyle: {
                    normal: {
                        lineStyle: {
                          width:1
                        }
                    },
                    emphasis : {
                        areaStyle: {color:'rgba(0,250,0,0.3)'}
                    }
                },
                data:[
                  {
                    value:data1[i],
                    name:i + "点"
                  }
                ]
            });
        }
        return series;
    })()
};
    myChart.setOption(option)

};


var data3= {
    "time": ['00:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', "22:00", "23:00"],
    "ducount": [100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200],
    "gucount":[100,200,300,400,500,100,500,300,200,100,200,300,400,500,100,500,300,200,100,200,300,400,500,100],
}
//userGiftTrend(data3)
//hourCateGiftUser()
//userDanmuTrend(data1)
//userExpense(data1)

function userGiftTrend(data){
     var myChart=echarts.init(document.getElementById("graph3"));
var option = {
    backgroundColor:'#ffffff',
    title: {
        text: '每小时送礼物用户数',
        left:'center'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
    },
    toolbox: {
        show: true,
        feature: {
            magicType: {type: ['line', 'bar']},
            restore: {},
            saveAsImage: {}
        }
    },
    xAxis:  {
        type: 'category',
        boundaryGap: false,
        data:data.time,
    },
    yAxis: {
        type: 'value',
    },
    bottom:30,
    series: [
        {
            name:'用户数',

            type:'line',
            data:data.gucount,
            markPoint: {
                data: [
                    {type: 'max', name: '最大值'},
                    {type: 'min', name: '最小值'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }
    ]
};
myChart.setOption(option)

}
function hourCateGiftUser(){
     var myChart=echarts.init(document.getElementById("graph1"));

var hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
        '7a', '8a', '9a','10a','11a',
        '12p', '1p', '2p', '3p', '4p', '5p',
        '6p', '7p', '8p', '9p', '10p', '11p'];
var days = ['Saturday', 'Friday', 'Thursday',
        'Wednesday', 'Tuesday', 'Monday', 'Sunday'];

var data = [[0,0,5],[0,1,1],[0,2,0],[0,3,0],[0,4,0],[0,5,0],[0,6,0],[0,7,0],[0,8,0],[0,9,0],[0,10,0],[0,11,2],[0,12,4],[0,13,1],[0,14,1],[0,15,3],[0,16,4],[0,17,6],[0,18,4],[0,19,4],[0,20,3],[0,21,3],[0,22,2],[0,23,5],[1,0,7],[1,1,0],[1,2,0],[1,3,0],[1,4,0],[1,5,0],[1,6,0],[1,7,0],[1,8,0],[1,9,0],[1,10,5],[1,11,2],[1,12,2],[1,13,6],[1,14,9],[1,15,11],[1,16,6],[1,17,7],[1,18,8],[1,19,12],[1,20,5],[1,21,5],[1,22,7],[1,23,2],[2,0,1],[2,1,1],[2,2,0],[2,3,0],[2,4,0],[2,5,0],[2,6,0],[2,7,0],[2,8,0],[2,9,0],[2,10,3],[2,11,2],[2,12,1],[2,13,9],[2,14,8],[2,15,10],[2,16,6],[2,17,5],[2,18,5],[2,19,5],[2,20,7],[2,21,4],[2,22,2],[2,23,4],[3,0,7],[3,1,3],[3,2,0],[3,3,0],[3,4,0],[3,5,0],[3,6,0],[3,7,0],[3,8,1],[3,9,0],[3,10,5],[3,11,4],[3,12,7],[3,13,14],[3,14,13],[3,15,12],[3,16,9],[3,17,5],[3,18,5],[3,19,10],[3,20,6],[3,21,4],[3,22,4],[3,23,1],[4,0,1],[4,1,3],[4,2,0],[4,3,0],[4,4,0],[4,5,1],[4,6,0],[4,7,0],[4,8,0],[4,9,2],[4,10,4],[4,11,4],[4,12,2],[4,13,4],[4,14,4],[4,15,14],[4,16,12],[4,17,1],[4,18,8],[4,19,5],[4,20,3],[4,21,7],[4,22,3],[4,23,0],[5,0,2],[5,1,1],[5,2,0],[5,3,3],[5,4,0],[5,5,0],[5,6,0],[5,7,0],[5,8,2],[5,9,0],[5,10,4],[5,11,1],[5,12,5],[5,13,10],[5,14,5],[5,15,7],[5,16,11],[5,17,6],[5,18,0],[5,19,5],[5,20,3],[5,21,4],[5,22,2],[5,23,0],[6,0,1],[6,1,0],[6,2,0],[6,3,0],[6,4,0],[6,5,0],[6,6,0],[6,7,0],[6,8,0],[6,9,0],[6,10,1],[6,11,0],[6,12,2],[6,13,1],[6,14,3],[6,15,4],[6,16,0],[6,17,0],[6,18,0],[6,19,0],[6,20,1],[6,21,2],[6,22,2],[6,23,6]];

data = data.map(function (item) {
    return [item[1], item[0], item[2] || '-'];
});

var option = {
    toolbox: {
        show: true,
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    title:{
        text:'每小时每种直播类别送礼物用户数热力图'
    },
    backgroundColor:'#ffffff',
    tooltip: {
        position: 'top'
    },
    animation: false,
    grid: {
        height: '60%',
        y: '15%'
    },
    xAxis: {
        type: 'category',
        data: hours,
        splitArea: {
            show: true
        }
    },
    yAxis: {
        type: 'category',
        data: days,
        splitArea: {
            show: true
        }
    },
    visualMap: {
        min: 0,
        max: 10,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '5%'
    },
    series: [{
        name: 'Punch Card',
        type: 'heatmap',
        data: data,
        label: {
            normal: {
                show: true
            }
        },
        itemStyle: {
            emphasis: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
};
   myChart.setOption(option)

}
function userDanmuTrend(data1){
     var myChart=echarts.init(document.getElementById("graph4"));
     var labelData=[];
     for (var i = 0; i < 24; ++i) {
    labelData.push({
        value: 1,
        name: i + ':00'
    });
}
var option = {
          toolbox: {
        show: true,
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    backgroundColor:'#ffffff',
    title: {
        text: '每小时发弹幕用户数',
        left:10,
    },
    color: ['#22C3AA'],
    tooltip:{
        show:true
    },
    series: [{
        type: 'pie',
        data: data1,
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

  myChart.setOption(option)
}
function userExpense(data1){
     var myChart=echarts.init(document.getElementById("graph2"));
     var option = {
          toolbox: {
        show: true,
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
         title:{
             text:'每小时用户花费数',
             left:'center'
         },
    backgroundColor: '#ffffff',
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)",

    },
    series: [
        {
            name:'每小时用户花费',
            type:'pie',
            radius: ['42%', '55%'],
            color: ['#d74e67', '#0092ff', '#eba954', '#21b6b9','#60a900','#01949b',' #f17677'],
            label: {
                normal: {
                    formatter: '{b}\n{d}%'
                },

            },
            data:data1
        }
    ]
};
     myChart.setOption(option)
}


data4={
    'name':["ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"
    ,"ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"],
    'income':["200","100","100","200","100","100","200","100","100","200","100","100"
    ,"200","100","100","200","100","100","200","100","100","200","100","100"]
}
data5={
    'name':["ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"
    ,"ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"],
    'income':["200","100","100","200","100","100","200","100","100","200","100","100"
    ,"200","100","100","200","100","100","200","100","100","200","100","100"]
}
data6={
    'name':["ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"
    ,"ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg","ddg","sgsg","gfg"],
    'income':["200","100","100","200","100","100","200","100","100","200","100","100"
    ,"200","100","100","200","100","100","200","100","100","200","100","100"]
}
hourMaxIncomeRoomTrend(data,data4,data5)
hourMaxIncomeCateRate()
incomeTrend(data)
hourCateIncome(data,data2)

function incomeTrend(data){
    var myChart=echarts.init(document.getElementById("graph3"));
    var option = {
        toolbox: {
        feature: {
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
    backgroundColor: '#fff',
    title: {
        text: '每小时直播间收入情况',
        left: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            lineStyle: {
                color: '#333'
            }
        }
    },
    legend: {
        icon: 'rect',
        itemWidth: 14,
        itemHeight: 5,
        itemGap: 13,
        data: [''],
        right: 'center',
        textStyle: {
            fontSize: 12,
            color: '#333'
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: [{
        type: 'category',
        boundaryGap: false,
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14,
                color: '#999'
            }
        },
        data: data.time
    }],
    yAxis: [{
        type: 'value',
        name: '',
        axisTick: {
            show: false
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14,
                color: '#999'
            }
        },
        splitLine: {
            lineStyle: {
                type: 'solid',
                color: '#ccc'
            }
        }
    }],
    series: [{
        name: '全站直播间收入',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        showSymbol: false,
        lineStyle: {
            normal: {
                width: 1
            }
        },
        areaStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 136, 212, 0.2)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 136, 212, 0)'
                }], false),
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 10
            }
        },
        itemStyle: {
            normal: {
                color: 'rgb(0,136,212)',
                borderColor: 'rgba(0,136,212,0.2)',
                borderWidth: 12

            }
        },
        data: data.income
    }, ]
};
    myChart.setOption(option)
}
function hourMaxIncomeCateRate(){
    var myChart=echarts.init(document.getElementById("graph2"));
    var option = {
        toolbox: {
        feature: {
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
        backgroundColor:'#ffffff',
        title:{
            text:'最火类别收入占比',
            left:'center',
            top:20
        },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['最火类别']
    },
    series: [{
        name: '',
        type: 'pie',
        radius: ['60%', '70%'],
        label: {
            normal: {
                position: 'center'
            }
        },
        data: [{
            value: 20,
            name: '最火类别',
            label: {
                normal: {
                    formatter: '{d} %',
                    textStyle: {
                        fontSize: 50
                    }
                }
            }
        }, {
            value: 80,
            name: '占位',
            label: {
                normal: {
                    formatter: '\n完成率',
                    textStyle: {
                        color: '#555',
                        fontSize: 20
                    }
                }
            },
            tooltip: {
                show: false
            },
            itemStyle: {
                normal: {
                    color: '#aaa'
                },
                emphasis: {
                    color: '#aaa'
                }
            },
            hoverAnimation: false
        }]
    }]
};
    myChart.setOption(option)
}
function hourMaxIncomeRoomTrend(data,data1,data2){
    var myChart=echarts.init(document.getElementById("graph1"));

var colors = ['#5793f3', '#d14a61'];

var option = {
    backgroundColor:'#ffffff',
    color: colors,
    title:{
      text:"每小时收入最多的两个主播",
        left:'center'

    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    toolbox: {
        feature: {
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
    legend: {
        data: ['第1名','第2名'],
        left:10,
    },
    xAxis: [{
        type: 'category',
        axisTick: {
            alignWithLabel: true
        },
        data: data.time
    }],
    yAxis: [{
        type: 'value',
        name: '主播收入',
        axisLabel: {
            formatter: '{value}万元'
        }
    }],
    series: [{
        name: '第1名',
        type: 'bar',
        itemStyle: {//图形样式
                normal: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#83bff6'
                    }, {
                        offset: 1,
                        color: '#188df0'
                    }])
                },
            },
        data:data1.income
    }, {
        name: '第2名',
        type: 'bar',
        itemStyle: {//图形样式
                normal: {
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: '#DC143C'
                    }, {
                        offset: 1,
                        color: '#C96DD8'
                    }])
                },
            },
        data: data2.income
    } ]
};
myChart.setOption(option)
}
function hourCateIncome(data,data1){
    var myChart=echarts.init(document.getElementById("graph4"));
  var  option = {
      backgroundColor:'#ffffff',
    title: {
        text: '每小时每种直播收入',
        top:10,
        left:10
    },
    tooltip: {
        trigger: 'item',
        backgroundColor : 'rgba(0,0,250,0.2)'
    },
    legend: {
        type: 'scroll',
        bottom: 10,
        data: (function (){
            var list = [];
            for (var i = 1; i <=24; i++) {
                list.push(i + '点 '+ '');
            }
            return list;
        })()
    },
    visualMap: {
        top: 'middle',
        right: 10,
        color: ['red', 'yellow'],
        calculable: true
    },
      toolbox: {
        feature: {
            restore: {},
            saveAsImage: {}
        }
    },
    radar: {
       indicator : [
           { text: 'IE8-', max: 400},
           { text: 'IE9+', max: 400},
           { text: 'Safari', max: 400},
           { text: 'Firefox', max: 400},
           { text: 'Chrome', max: 400}
        ]
    },
    series : (function (){
        var series = [];
        for (var i = 1; i <= 24; i++) {
            series.push({
                name:'浏览器（数据纯属虚构）',
                type: 'radar',
                symbol: 'none',
                itemStyle: {
                    normal: {
                        lineStyle: {
                          width:1
                        }
                    },
                    emphasis : {
                        areaStyle: {color:'rgba(0,250,0,0.3)'}
                    }
                },
                data:[
                  {
                    value:data1[i],
                    name:i + "点"
                  }
                ]
            });
        }
        return series;
    })()
};
    myChart.setOption(option)
}