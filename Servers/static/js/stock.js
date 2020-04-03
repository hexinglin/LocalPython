var num =10

var kChart = echarts.init(document.getElementById('k-content'));

 $.ajax({
     type: "get",
     dataType:'json',
     url: "http://127.0.0.1:8000/stock/gettest/",
     success: function(data){
         show(data);
         console.log(data);
     }
 });
let re=[];
for(let i=0;i<num;i++){
    let [...arr1]=inkdata[i];
    re.push(arr1);
}
// kChart.setOption(initKOption(re));


function addline() {
    kChart.setOption(initKOption(re));
console.log(re)
    num++;
    re.push(inkdata[num]);
    if (num>15) {
        re.shift();
    }
kChart.setOption(initKOption(re),true);

}

function show(data) {
    kChart.setOption( {
			tooltip: { //弹框指示器
				trigger: 'axis',
				axisPointer: {
					type: 'cross'
				}
			},
			legend: { //图例控件,点击图例控制哪些系列不显示
				icon: 'rect',
				type:'scroll',
				itemWidth: 14,
				itemHeight: 2,
				left: 0,
				top: '-1%',
				animation:true,
				textStyle: {
					fontSize: 12,
					color: '#0e99e2'
				},
				pageIconColor:'#0e99e2'
			},
			axisPointer: {
		// 		      link: {xAxisIndex: 'all'},
      // label: {
      //   backgroundColor: '#777'
      // }
				show: true
			},
			color: [ma5Color, ma10Color, ma20Color, ma30Color],
			grid: [{
				// id: 'gd1',
				left: '0%',
				right: '1%',
				height: '60%', //主K线的高度,
				top: '5%'
			}, {
				left: '0%',
				right: '1%',
				top: '66.5%',
				height: '10%' //交易量图的高度
			}, {
				left: '0%',
				right: '1%',
				top: '80%', //MACD 指标
				height: '14%'
			}],
			xAxis: [ //==== x轴
				{ //主图
					type: 'category',
					data: data.times,
					scale: true,
					// boundaryGap: false,
					axisLine: {
						onZero: false
					},
					axisLabel: { //label文字设置
						show: false
					},
					splitLine: {
						show: false,
						lineStyle: {
							color: '#3a3a3e'
						}
					},
					splitNumber: 20,
					min: 'dataMin',
					max: 'dataMax'
				}, { //交易量图
					type: 'category',
					gridIndex: 1,
					data: data.times,
					axisLabel: { //label文字设置
						color: '#9b9da9',
						fontSize: 10
					},
				}, { //幅图
					type: 'category',
					gridIndex: 2,
					data: data.times,
					axisLabel: {
						show: false
					}
				}
			],
			yAxis: [ //y轴
				{ //==主图
					scale: true,
					z:4,
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						inside: true, //label文字朝内对齐
					},
					splitLine: { //分割线设置
						show: false,
						lineStyle: {
							color: '#181a23'
						}
					},
				}, { //交易图
					gridIndex: 1, splitNumber: 3, z:4,
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
						fontSize: 12
					},
				}, { //幅图
					z:4, gridIndex: 2,splitNumber: 4,
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
			animation: true, //禁止动画效果
			backgroundColor: bgColor,
			blendMode: 'source-over',
			series: [{
					name: 'K线周期图表',
					type: 'candlestick',
					data: data.datas,
					barWidth: '75%',
					large: true,
					largeThreshold: 100,
					itemStyle: {
						normal: {
							color: upColor, //fd2e2e  ff4242
							color0: downColor,
							borderColor: upColor,
							borderColor0: downColor,

							//opacity:0.8
						}
					},

				}
				, {
					name: 'Volumn',
					type: 'bar',
					xAxisIndex: 1,
					yAxisIndex: 1,
					data: data.vols,
					barWidth: '75%',
					itemStyle: {
						normal: {
							color: function(params) {
								var colorList;
								if (data.datas[params.dataIndex][1] > data.datas[params.dataIndex][0]) {
									colorList = upColor;
								} else {
									colorList = downColor;
								}
								return colorList;
							},
						}
					}
				}
				, {
					name: 'MA5',
					type: 'line',
					data: data.ma5,
					smooth: true,
					symbol: "none", //隐藏选中时有小圆点
					lineStyle: {
						normal: {
							opacity: 0.8,
							color: '#39afe6',
							width: 1
						}
					},
				},
				{
					name: 'MA10',
					type: 'line',
					data: data.ma10,
					smooth: true,
					symbol: "none",
					lineStyle: { //标线的样式
						normal: {
							opacity: 0.8,
							color: '#da6ee8',
							width: 1
						}
					}
				},
				{
					name: 'MA20',
					type: 'line',
					data: data.ma20,
					smooth: true,
					symbol: "none",
					lineStyle: {
						opacity: 0.8,
						width: 1,
						color: ma20Color
					}
				},
				{
					name: 'MA30',
					type: 'line',
					data:data.ma30,
					smooth: true,
					symbol: "none",
					lineStyle: {
						normal: {
							opacity: 0.8,
							width: 1,
							color: ma30Color
						}
					}
				}
				, {
					name: 'MACD',
					type: 'bar',
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: data.macd,
					barWidth: '40%',
					itemStyle: {
						normal: {
							color: function(params) {
								var colorList;
								if (params.data >= 0) {
									colorList = upColor;
								} else {
									colorList = downColor;
								}
								return colorList;
							},
						}
					}
				}, {
					name: 'DIF',
					type: 'line',
					symbol: "none",
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: data.dif,
					lineStyle: {
						normal: {
							color: '#da6ee8',
							width: 1
						}
					}
				}, {
					name: 'DEA',
					type: 'line',
					symbol: "none",
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: data.dea,
					lineStyle: {
						normal: {
							opacity: 0.8,
							color: '#39afe6',
							width: 1
						}
					}
				}
			]
		},true);
}









