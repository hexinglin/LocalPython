var bgColor = "#1f212d";//背景
var upColor="#F9293E";//涨颜色
var downColor="#00aa3b";//跌颜色

// ma  颜色
var ma5Color = "#39afe6";
var ma10Color = "#da6ee8";
var ma20Color = "#ffab42";
var ma30Color = "#00940b";

/**
 * 15:20 时:分 格式时间增加num分钟
 * @param {Object} time 起始时间
 * @param {Object} num
 */
function addTimeStr(time,num){ 
	var hour=time.split(':')[0];
	var mins=Number(time.split(':')[1]);
	var mins_un=parseInt((mins+num)/60);
	var hour_un=parseInt((Number(hour)+mins_un)/24);
	if(mins_un>0){
		if(hour_un>0){
			var tmpVal=((Number(hour)+mins_un)%24)+"";
			hour=tmpVal.length>1? tmpVal:'0'+tmpVal;//判断是否是一位
		}else{
			var tmpVal=Number(hour)+mins_un+"";
			hour=tmpVal.length>1? tmpVal:'0'+tmpVal;
		}
		var tmpMinsVal=((mins+num)%60)+"";
		mins=tmpMinsVal.length>1? tmpMinsVal:0+tmpMinsVal;//分钟数为 取余60的数
	}else{
		var tmpMinsVal=mins+num+"";
		mins=tmpMinsVal.length>1? tmpMinsVal:'0'+tmpMinsVal;//不大于整除60
	} 
	return hour+":"+mins;
}

//获取增加指定分钟数的 数组  如 09:30增加2分钟  结果为 ['09:31','09:32'] 
function getNextTime(startTime, endTIme, offset, resultArr) {
	var result = addTimeStr(startTime, offset);
	resultArr.push(result);
	if (result == endTIme) {
		return resultArr;
	} else {
		return getNextTime(result, endTIme, offset, resultArr);
	}
}


/**
 * 不同类型的股票的交易时间会不同  
 * @param {Object} type   hs=沪深  us=美股  hk=港股
 */
var time_arr = function(type) { 
	if(type.indexOf('us')!=-1){//生成美股时间段
		var timeArr = new Array();
		timeArr.push('09:30')
		return getNextTime('09:30', '16:00', 1, timeArr);
	}
	if(type.indexOf('hs')!=-1){//生成沪深时间段
		var timeArr = new Array();
			timeArr.push('09:30');
			timeArr.concat(getNextTime('09:30', '11:29', 1, timeArr));
			timeArr.push('13:00');
			timeArr.concat(getNextTime('13:00', '15:00', 1, timeArr));
		return timeArr;
	}
	if(type.indexOf('hk')!=-1){//生成港股时间段
		var timeArr = new Array();
			timeArr.push('09:30');
			timeArr.concat(getNextTime('09:30', '11:59', 1, timeArr)); 
			timeArr.push('13:00');
			timeArr.concat(getNextTime('13:00', '16:00', 1, timeArr)); 
		return timeArr;
	}
	
}


/**
 * 计算价格涨跌幅百分比
 * @param {Object} price 当前价
 * @param {Object} yclose 昨收价
 */
function ratioCalculate(price,yclose){
	return ((price-yclose)/yclose*100).toFixed(3);
}




 