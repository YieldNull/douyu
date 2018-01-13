initOnedayChart();


function initOnedayChart(){
  // rankingOneday(dateOneday);
    onedayTopUserDanmu();
    onedayTopUserGift();
    onedayTopUserExpence();

}
function initSomedayChart(date1,date2) {
rankingSomeday(date1,date2);
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
};
function changeDownTab(type){
    var div1=document.getElementById("tab1D");
    var div2=document.getElementById("tab2D");
    var div3=document.getElementById("tab3D");
    var l1=document.getElementById("l1");
    var l2=document.getElementById("l2");
    var l3=document.getElementById("l3");
    document.getElementById('xx').className=''
 switch(type){
     case 1:
         div1.className="tab-pane active";
         div2.className="tab-pane";
         div3.className="tab-pane";
         l1.className="active";
         l2.className="";
         l3.className="";
         break;
     case 2:
         div2.className="tab-pane active";
         div2.className="tab-pane";
         div3.className="tab-pane";
         l1.className="active";
         l2.className="";
         l3.className="";
         break;
      case 3:
         div1.style.display="none";
         div2.style.display="none";
          div3.style.display='block';
         break;
 }
};
function changeManner(type){
    var dateOne=$("#input1").val();
    var date1=$("#input2").val();
    var date2=$("#input3").val();
     switch(type){
     case 1:
         initOnedayChart(dateOne);
         break;
     case 2:
         initSomedayChart(date1,date2);
         break
};}


//oneday请求数据
function rankingOneday(dateOne){
    $.ajax({
        url:'',
        type:'GET',
        data:{
            "dateOne":dateOne
        },
        contentType:'application/json',
        success:function (data) {
             roomOnedayTopRoom(data);
        }

    });
    //请求用户弹幕排行
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            onedayTopUserDanmu(data);
        }
    });

    //请求用户礼物数排行
     $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            onedayTopUserGift(data);
        }
    });

    //请求用户花费排行
     $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            onedayTopUserExpence(data);
        }
    });

     //请求类别排名
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            onedayTopCate(data);
        }
    });
}

//someday请求数据
function rankingSomeday(date1,date2){
    //请求弹幕、礼物、收入
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            roomSomedayTopRoom(data);
        }
    });

    //请求用户弹幕排行
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            SomedayTopUserDanmu(data);
        }
    });

    //请求用户礼物数排行
     $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            SomedayTopUserGift(data);
        }
    });

    //请求用户花费排行
     $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            SomedayTopUserExpence(data);
        }
    });

     //请求类别排名
    $.ajax({
        url: '',
        type:'GET',
        data:{
            "date1":date1,
            "date2":date2
        },
        contentType:'application/json',
        success:function(data){
            SomedayTopCate(data);
        }
    });

}

//一段时间图表
function roomSomedayTopRoom(data){
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
function SomedayTopUserDanmu(data){
    var myChart=echarts.init(document.getElementById('rightGraph3'));
  var  option = {
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
        data:data.user
    },
    series: [{
        name: '2',
        type: 'bar',
        data: data.danmu
    }]

};
  myChart.setOption(option);
};
function SomedayTopUserGift(data){
    var myChart=echarts.init(document.getElementById('rightGraph2'));
var option = {
    backgroundColor: '#0E2A43',
    legend: {
        bottom: 20,
        textStyle:{
            color:'#fff',
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
        show:"true",
        trigger: 'axis',
        axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    xAxis:  {
        type: 'value',
        axisTick : {show: false},
        axisLine: {
            show: false,
            lineStyle:{
                color:'#fff',
            }
        },
        splitLine: {
            show: false
        },
    },
    yAxis: [
            {
                type: 'category',
                axisTick : {show: false},
                axisLine: {
                    show: true,
                    lineStyle:{
                        color:'#fff',
                    }
                },
                data:data.user
            },

    ],
    series: [
        {
            name: '花费',
            type: 'bar',

            itemStyle:{
                normal: {
                    show: true,
                    color: '#green',
                    barBorderRadius:50,
                    borderWidth:0,
                    borderColor:'#333',
                }
            },
            barGap:'0%',
            barCategoryGap:'50%',
            data:data.gift2
        }

    ]
};
myChart.setOption(option);
};
function SomedayTopUserExpence(data){

var myChart=echarts.init(document.getElementById('rightGraph1'));
var option = {
    backgroundColor: '#0E2A43',
    legend: {
        bottom: 20,
        textStyle:{
            color:'#fff',
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
        show:"true",
        trigger: 'axis',
        axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    xAxis:  {
        type: 'value',
        axisTick : {show: false},
        axisLine: {
            show: false,
            lineStyle:{
                color:'#fff',
            }
        },
        splitLine: {
            show: false
        },
    },
    yAxis: [
            {
                type: 'category',
                axisTick : {show: false},
                axisLine: {
                    show: true,
                    lineStyle:{
                        color:'#fff',
                    }
                },
                data:data.user
            },

    ],
    series: [
        {
            name: '花费',
            type: 'bar',

            itemStyle:{
                normal: {
                    show: true,
                    color: '#277ace',
                    barBorderRadius:50,
                    borderWidth:0,
                    borderColor:'#333',
                }
            },
            barGap:'0%',
            barCategoryGap:'50%',
            data:data.expence
        }

    ]
};
myChart.setOption(option);
};
function SomedayTopCate(data){
  var myChart=echarts.init(document.getElementById('leftGraph'));
  var  option = {
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
        "data": ["TOP10", "TOP9", "TOP8", "TOP7", "TOP6","TOP5", "TOP4", "TOP3", "TOP2", "TOP1"],
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
                "formatter": function(params) {
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

};

//一天的时间图表
function roomOnedayTopRoom(data){
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
function onedayTopUserDanmu(){
     var myChart=echarts.init(document.getElementById('rightGraph3'));
  var  option = {
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
        data:['xio','kdf','fkdj']
    },
    series: [{
        name: '2',
        type: 'bar',
        data: [100,300,200]
    }]

};
  myChart.setOption(option);
};
function onedayTopUserGift(){
    var myChart=echarts.init(document.getElementById('rightGraph2'));
var option = {
    backgroundColor: '#0E2A43',
    legend: {
        bottom: 20,
        textStyle:{
            color:'#fff',
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
        show:"true",
        trigger: 'axis',
        axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    xAxis:  {
        type: 'value',
        axisTick : {show: false},
        axisLine: {
            show: false,
            lineStyle:{
                color:'#fff',
            }
        },
        splitLine: {
            show: false
        },
    },
    yAxis: [
            {
                type: 'category',
                axisTick : {show: false},
                axisLine: {
                    show: true,
                    lineStyle:{
                        color:'#fff',
                    }
                },
                data:['xio','kdf','fkdj']
            },

    ],
    series: [
        {
            name: '花费',
            type: 'bar',

            itemStyle:{
                normal: {
                    show: true,
                    color: '#green',
                    barBorderRadius:50,
                    borderWidth:0,
                    borderColor:'#333',
                }
            },
            barGap:'0%',
            barCategoryGap:'50%',
            data:[100,200,300]
        }

    ]
};
myChart.setOption(option);
};
function onedayTopUserExpence(){
    var myChart=echarts.init(document.getElementById('rightGraph1'));
var option = {
    backgroundColor: '#0E2A43',
    legend: {
        bottom: 20,
        textStyle:{
            color:'#fff',
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
        show:"true",
        trigger: 'axis',
        axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    xAxis:  {
        type: 'value',
        axisTick : {show: false},
        axisLine: {
            show: false,
            lineStyle:{
                color:'#fff',
            }
        },
        splitLine: {
            show: false
        },
    },
    yAxis: [
            {
                type: 'category',
                axisTick : {show: false},
                axisLine: {
                    show: true,
                    lineStyle:{
                        color:'#fff',
                    }
                },
                data:['xio','kdf','fkdj']
            },

    ],
    series: [
        {
            name: '花费',
            type: 'bar',

            itemStyle:{
                normal: {
                    show: true,
                    color: '#277ace',
                    barBorderRadius:50,
                    borderWidth:0,
                    borderColor:'#333',
                }
            },
            barGap:'0%',
            barCategoryGap:'50%',
            data:[100,20,344]
        }

    ]
};
myChart.setOption(option);
};
function onedayTopCate(data){
      var myChart=echarts.init(document.getElementById('leftGraph'));
  var  option = {
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
        "data": ["TOP10", "TOP9", "TOP8", "TOP7", "TOP6","TOP5", "TOP4", "TOP3", "TOP2", "TOP1"],
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
                "formatter": function(params) {
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
};