initOnedayChart(2017-10-01);


function initOnedayChart(dateOneday){
   roomOnedayTop(dateOneday);
}
function initSomedayChart(date1,date2) {
rankingLeftTwo(date1,date2);
}
function changeTab(type){
    var div1=document.getElementById("tab1");
    var div2=document.getElementById("tab2");
 switch(type){
     case 1:
         div1.style.display="block";
         div2.style.display="none";
         initOnedayChart(2017-10-01);
         break;
     case 2:
         div1.style.display="none";
         div2.style.display="block";
         initSomedayChart(2017-10-01,2017-10-07);
         break
 }
}

function rankingLeftOne(dateOne){
    $.ajax({
        url:'',
        type:'GET',
        data:{
            "dateOne":dateOne
        },
        contentType:'application/json',
        success:function (data) {
             roomOnedayTop(data);
        }

    });
}
function rankingLeftTwo(date1,date2){
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            roomSomedayTop(data);
        }
    });
}

function roomSomedayTop(data){
    var myChart=echarts.init(document.getElementById('leftRankingTwo'));
    var option={
            title:{
                text:'主播排行榜',
            },
        legend:{
                show:true,
                data:['收入','礼物','弹幕']
        },
        grid:{
               top:100
        },
        angleAxis:{
           type:'category'  ,
           data:data.room
        },
        radiusAxis:{

        },
        polar:{

        },
        tooltip:{
              show:true,

        },
        series:[{
              type:'bar',
              data:data.income,
              coordinateSystem:'polar',
              name:'收入',
              stack:'a'
        },{
           type:'bar',
              data:data.gift,
              coordinateSystem:'polar',
              name:'礼物',
              stack:'a'
        },{
           type:'bar',
              data:data.danmu,
              coordinateSystem:'polar',
              name:'弹幕',
              stack:'a'
        },]

    };
      myChart.setOption(option);
};
function roomOnedayTop(data){
    var myChart=echarts.init(document.getElementById('leftRankingOne'));
    var option = {
    backgroundColor: '#0E2A43',
    title: {
        text: "主播排行榜",
        textStyle: {
            color: '#00FFFF',
            fontSize: 24
        }
    },
    legend: {
        bottom: 20,
        textStyle: {
            color: '#fff',
        },
        data: ['收入', '礼物','弹幕']
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
            show: false,
            lineStyle: {
                color: '#fff',
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
                    color: '#fff',
                }
            },
            data:data.room
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
            data:data.room
        },{
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
            data:data.room
        },

    ],
    series: [{
            name: '总值',
            type: 'bar',
            xAxisIndex: 1,

            itemStyle: {
                normal: {
                    show: true,
                    color: '#277ace',
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            barWidth: '5%',
            data: data.total
        }, {
            name: '总值',
            type: 'bar',
            xAxisIndex: 1,

            itemStyle: {
                normal: {
                    show: true,
                    color: '#277ace',
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            barWidth: '5%',
            barGap: '100%',
            data: data.total
        },
        {
            name: '总值',
            type: 'bar',
            xAxisIndex: 1,

            itemStyle: {
                normal: {
                    show: true,
                    color: '#277ace',
                    barBorderRadius: 50,
                    borderWidth: 0,
                    borderColor: '#333',
                }
            },
            barWidth: '5%',
            barGap: '100%',
            data: data.total
        },{
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
                        color: '#fff'
                    }
                }
            },
            barWidth: '5%',
            data: data.income
        }, {
            name: '礼物',
            type: 'bar',
            barWidth: '5%',
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
                        color: '#fff'
                    }
                }
            },
            data:data.gift
        },{
            name: '弹幕',
            type: 'bar',
            barWidth: '5%',
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
                        color: '#fff'
                    }
                }
            },
            barGap: '100%',
            data: data.danmu
        }

    ]
};
    myChart.setOption(option);
};