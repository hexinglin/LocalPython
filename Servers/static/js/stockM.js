var num =10
var dealtime = 100;

var mChart = echarts.init(document.getElementById('m-line'));
// show(mdata1);
let re={};
mdata1 = [];
 $.ajax({
     type: "get",
     dataType:'json',
     url: "http://127.0.0.1:8000/stock/getmin/",
     success: function(data){
         mdata1 = data;
         re={
         	  date:mdata1.date,
			 priceArr:[],
			 avgPrice:[],
			 vol:[],
			 gap:0,
			 cost:5,
			 yestclose: data.yestclose
		 };
         //实时刷新时间单位为毫秒
		 setInterval(addline(),dealtime);

     }
 });

i=0;

function addline() {
	re.priceArr.push(mdata1.priceArr[i]);
	re.avgPrice.push(mdata1.avgPrice[i]);
	re.vol.push(mdata1.vol[i]);
	gapt = Math.abs(re.yestclose-mdata1.priceArr[i]);
	if(gapt>re.gap){
		re.gap=gapt;
	}
	i++;
	show(re);
}

function show(m_datas) {
	var times = time_arr('hs');
    mChart.setOption({
		tooltip: { //弹框指示器
			trigger: 'axis',
			axisPointer: {
				type: 'cross'
			},
			formatter: function(params, ticket, callback) {
				var i = params[0].dataIndex;

				var color;
				if (m_datas.priceArr[i] > m_datas.yestclose) {
					color ='style="color:#ff4242"';
				} else {
					color ='style="color:#26bf66"';
				}

				var html = '<div class="commColor" style="width:100px;"><div>当前价 <span  '+color+' >' + m_datas.priceArr[i] + '</span></div>';
				html += '<div>均价 <span  '+color+' >' + m_datas.avgPrice[i] + '</span></div>';
				html += '<div>涨幅 <span  '+color+' >' + ratioCalculate(m_datas.priceArr[i],m_datas.yestclose)+ '%</span></div>';
				html += '<div>成交量 <span  '+color+' >' + m_datas.vol[i] + '</span></div></div>'
				return html;
			}
		},
		legend: { //图例控件,点击图例控制哪些系列不显示
			icon: 'rect',
			type: 'scroll',
			itemWidth: 14,
			itemHeight: 2,
			left: 0,
			top: '-1%',
			textStyle: {
				fontSize: 12,
				color: '#0e99e2'
			}
		},
		axisPointer: {
			show: true
		},
		color: [ma5Color, ma10Color],
		grid: [{
				id: 'gd1',
				left: '0%',
				right: '1%',
				height: '67.5%', //主K线的高度,
				top: '5%'
			},
			{
				id: 'gd2',
				left: '0%',
				right: '1%',
				height: '67.5%', //主K线的高度,
				top: '5%'
			}, {
				id: 'gd3',
				left: '0%',
				right: '1%',
				top: '75%',
				height: '19%' //交易量图的高度
			}
		],
		xAxis: [ //==== x轴
			{ //主图
				gridIndex: 0,
				data:times,
				axisLabel: { //label文字设置
					show: false
				},
				splitLine: {
					show: true,
					lineStyle: {
						type:'dotted', //虚线
						color: '#481a23'
					}
				}
			},
			{
				show:false,
				gridIndex: 1,
				data: times,
				axisLabel: { //label文字设置
					show: false
				},
				splitLine: {
					show: false,
				}
			}, { //交易量图
				splitNumber: 2,
				type: 'category',
				gridIndex: 2,
				data: times,
				axisLabel: { //label文字设置
					color: '#9b9da9',
					fontSize: 10
				},
			}
		],
		yAxis: [ //y轴
			{
				gridIndex: 0,
				scale: true,
				splitNumber: 4,
				min:(m_datas.yestclose - m_datas.gap).toFixed(2),
				max:(m_datas.yestclose + m_datas.gap).toFixed(2),
				// interval:m_datas.yestclose,
				axisLabel: { //label文字设置
					inside: true, //label文字朝内对齐
					fontWeight:'bold',
					color:function(val){
						if(val==m_datas.yestclose){
							return '#aaa'
						}
						return val>m_datas.yestclose? upColor:downColor;
					}
				},splitLine: { //分割线设置
					show: true,
					lineStyle: {
						type:'dotted', //虚线
						color: '#481a23'
					}
				},
			}, {
				scale: true,
				gridIndex: 1,
				splitNumber: 4,
				min:(m_datas.yestclose - m_datas.gap).toFixed(2),
				max:(m_datas.yestclose + m_datas.gap).toFixed(2),
				position: 'right',
				axisLabel: { //label文字设置
					color:function(val){
						if(val==m_datas.yestclose){
							return '#aaa'
						}
						return val>m_datas.yestclose? upColor:downColor;
					},
					inside: true, //label文字朝内对齐
					fontWeight:'bold',
					formatter:function(val){
						var resul=ratioCalculate(val,m_datas.yestclose);
						return  Number(resul).toFixed(2)+' %'}
				},
				splitLine: { //分割线设置
					show: false,
					lineStyle: {
						type:'dotted', //虚线
						color: '#481a23'
					}
				},
				axisPointer:{show:true,
					label:{
						formatter:function(params){ //计算右边Y轴对应的当前价的涨幅比例
							return  ratioCalculate(params.value,m_datas.yestclose)+'%';
						}
					}
				}
			}
			, { //交易图
				gridIndex: 2,z:4,
				splitNumber: 3,
				axisLine: {
					onZero: false
				},
				axisTick: {
					show: false
				},
				splitLine: {
					show: false
				},
				axisLabel: { //label文字设置
					color: '#c7c7c7',
					inside: true, //label文字朝内对齐
					fontSize: 8
				},
			}
		],
		dataZoom: [

		],
		//animation:false,//禁止动画效果
		backgroundColor: bgColor,
		blendMode: 'source-over',
		series: [{
				name: '当前价',
				type: 'line',
				data: m_datas.priceArr,
				smooth: true,
				symbol: "circle", //中时有小圆点
				lineStyle: {
					normal: {
						opacity: 0.8,
						color: '#39afe6',
						width: 1
					}
				}
				,areaStyle: {
					normal: {
						color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
							offset: 0,
							color: 'rgba(0, 136, 212, 0.7)'
						}, {
							offset: 0.8,
							color: 'rgba(0, 136, 212, 0.02)'
						}], false),
						shadowColor: 'rgba(0, 0, 0, 0.1)',
						shadowBlur: 10
					}
				}
				,markLine: {
					symbol: ['none', 'none'],//去掉箭头
					itemStyle: {
						normal: { lineStyle: { type: 'solid', color:'blue'}
						,label: { show: false, position:'left' } }
					},
					data: [{
							name: 'Y 轴值为 100 的水平线',
							yAxis: m_datas.yestclose,
					}
					]
				}
			},
			{
				name: '成本',
				type: 'line'
				,markLine: {
					show:false,
					symbol: ['none', 'none'],//去掉箭头
					itemStyle: {
						normal: { lineStyle: { type: 'dotted', color:'yellow'}
						,label: { show: false, position:'left' } }
					},
					data: [{
							name: '成本线',
							yAxis: m_datas.cost,
					}
					]
				}

			},
			{
				name: '均价',
				type: 'line',
				data: m_datas.avgPrice,
				smooth: true,
				symbol: "circle",
				lineStyle: { //标线的样式
					normal: {
						opacity: 0.8,
						color: '#da6ee8',
						width: 1
					}
				}
			},{
				type: 'line',
				data: m_datas.priceArr,
				smooth: true,
				symbol: "none",
				gridIndex: 1,
				xAxisIndex: 1,
				yAxisIndex: 1,
				lineStyle: { //标线的样式
					normal: {
						width: 0
					}
				}
			},
			{
				name: 'Volumn',
				type: 'bar',
				gridIndex: 2,
				xAxisIndex: 2,
				yAxisIndex: 2,
				data: m_datas.vol,
				barWidth: '60%',
				itemStyle: {
					normal: {
						color: function(params) {
							var colorList;
							if (m_datas.priceArr[params.dataIndex] > m_datas.priceArr[params.dataIndex-1]) {
								colorList = upColor;
							} else {
								colorList = downColor;
							}
							return colorList;
						},
					}
				}
			}
		]
	},true);
}









