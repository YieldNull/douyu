initSite('2017-12-01');
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
             userDanmuRate(data);
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
             hourMaxIncomeCateTrend(data);
              hourMaxIncomeCateRate(data);
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

function danmuTrend(data){
    var myChart=echarts.init(document.getElementById('graph1'));
    var option = {
    title: {
        text: '今日&昨日',
        left: '50%',
        textAlign: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            lineStyle: {
                color: '#ddd'
            }
        },
        backgroundColor: 'rgba(255,255,255,1)',
        padding: [5, 10],
        textStyle: {
            color: '#7588E4',
        },
        extraCssText: 'box-shadow: 0 0 5px rgba(0,0,0,0.3)'
    },
    legend: {
        right: 20,
        orient: 'vertical',
        data: ['弹幕数']
    },
    xAxis: {
        type: 'category',
        data: ['00:00','2:00','4:00','6:00','8:00','10:00','12:00','14:00','16:00','18:00','20:00',"22:00","23:00"],
        boundaryGap: false,
        splitLine: {
            show: true,
            interval: 'auto',
            lineStyle: {
                color: ['#D4DFF5']
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: '#609ee9'
            }
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14
            }
        }
    },
    yAxis: {
        type: 'value',
        splitLine: {
            lineStyle: {
                color: ['#D4DFF5']
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: '#609ee9'
            }
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14
            }
        }
    },
    series: [{
        name: '弹幕数',
        type: 'line',
        smooth: true,
        showSymbol: false,
        symbol: 'circle',
        symbolSize: 6,
        data:data.danmu,
        areaStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(216, 244, 247,1)'
                }, {
                    offset: 1,
                    color: 'rgba(216, 244, 247,1)'
                }], false)
            }
        },
        itemStyle: {
            normal: {
                color: '#58c8da'
            }
        },
        lineStyle: {
            normal: {
                width: 3
            }
        }
    }]
};
};
function danmuRate(data,total){
    var myChart=echarts.init(document.getElementById("graph2"));
    var colorList = [
    '#66c5d7', '#11c88c', '#989cff', '#ffa55d', '#9c7de1', '#5d9eff', '#ffdb5d', '#ee82ed', '#8fca5f', '#b995f5'
  ];

 // 总和
 //var total = {
   //  value: '24,652',
     //name: '用户总数'
 //}

 //var originalData = [{
   //  value: 55,
    // name: 'IOS'
 //}, {
   //  value: 70,
     //name: '安卓国内'
 //}, {
   //  value: 25,
     //name: "安卓海外"
 //}];

 echarts.util.each(data, function(item, index) {
     item.itemStyle = {
         normal: {
             color: colorList[index]
         }
     };
 });

 var option = {
     tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
    },
    backgroundColor:'#ffffff',
     title: [{
            text: "弹幕总数",
            left: '49%',
            top: '46%',
            textAlign: 'center',
            textBaseline: 'middle',
            textStyle: {
                color: '#999',
                fontWeight: 'normal',
                fontSize: 20
            }
        }, {
            text: total,
            left: '49%',
            top: '51%',
            textAlign: 'center',
            textBaseline: 'middle',
            textStyle: {
                color: '#666',
                fontWeight: 'normal',
                fontSize: 40
            }
        }],
     series: [{
         hoverAnimation: false, //设置饼图默认的展开样式
         radius: [100, 150],
         name: 'pie',
         type: 'pie',
         selectedMode: 'single',
         selectedOffset: 16, //选中是扇区偏移量
         clockwise: true,
         startAngle: 90,
         label: {
             normal: {
                 show: false
             }
         },
         labelLine: {
             normal: {
                 show: false
             }
         },
          itemStyle: {
            normal: {
                borderWidth: 3,
                borderColor: '#ffffff',
            },
            emphasis: {
                borderWidth: 0,
                shadowBlur: 5,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.2)'
            }
        },
         data: data
     }]
 };
 myChart.setOption(option, true);
};
function giftTrend(data){
    var myChart=echarts.init(document.getElementById("graph3"));
     var option = {
    title:{
        text:'礼物数趋势',
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
	grid: {
		left: '1%',
		right: '4%',
		bottom: '6%',
		top:30,
		padding:'0 0 10 0',
		containLabel: true,
	},
    legend: {//图例组件，颜色和名字
        right:10,
		top:0,
		itemGap: 16,
		itemWidth: 18,
		itemHeight: 10,
        data:[{
            name:'礼物数',
            //icon:'image://../wwwroot/js/url2.png', //路径
        },
        {
            name:'流出',
        }],
        textStyle: {
			color: '#a8aab0',
			fontStyle: 'normal',
			fontFamily: '微软雅黑',
			fontSize: 12,
        }
    },
	xAxis: [
		{
			type: 'category',
			boundaryGap: true,//坐标轴两边留白
			data: ['00:00','2:00','4:00','6:00','8:00','10:00','12:00','14:00','16:00','18:00','20:00',"22:00","23:00"],
			axisLabel: { //坐标轴刻度标签的相关设置。
				interval: 0,//设置为 1，表示『隔一个标签显示一个标签』
				margin:15,
				textStyle: {
					color: '#078ceb',
					fontStyle: 'normal',
					fontFamily: '微软雅黑',
					fontSize: 12,
				}
			},
			axisTick:{//坐标轴刻度相关设置。
				show: false,
			},
			axisLine:{//坐标轴轴线相关设置
				lineStyle:{
					color:'black',
					opacity:0.4
				}
			},
			splitLine: { //坐标轴在 grid 区域中的分隔线。
				show: false,
			}
		}
	],
	yAxis: [
		{
			type: 'value',
			splitNumber: 5,
			axisLabel: {
				textStyle: {
					color: '#a8aab0',
					fontStyle: 'normal',
					fontFamily: '微软雅黑',
					fontSize: 12,
				}
			},
			axisLine:{
			lineStyle:{
					color:'black',
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
            barWidth: 20,
            barGap:0,//柱间距离
            label: {//图形上的文本标签
                normal: {
                   show: true,
                   position: 'top',
                   textStyle: {
                       color: '#a8aab0',
                       fontStyle: 'normal',
                       fontFamily: '微软雅黑',
                       fontSize: 12,
                   },
                },
            },
            itemStyle: {//图形样式
                normal: {
					barBorderRadius: [5, 5, 0, 0],
					color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 1, color: 'rgba(127, 128, 225, 0.7)'
                    },{
                        offset: 0.9, color: 'rgba(72, 73, 181, 0.7)'
                    },{
                        offset: 0.31, color: 'rgba(0, 208, 208, 0.7)'
                    },{
                        offset: 0.15, color: 'rgba(0, 208, 208, 0.7)'
                    }, {
                        offset: 0, color: 'rgba(104, 253, 255, 0.7)'
                    }], false),
                },
            },
        }
    ]
};
};
function hourCateDanmu(data){

};