var num =10
var dealtime = 500;
var systime = -1;
var showterval;
let re={};
let accountInfo ={}
var nowStockData = [];
var myStock={}
var willStock={}

document.getElementById('speed').onclick=function () {
	dealtime = dealtime - 200;
	if (dealtime <= 100){
		dealtime = 100;
		document.getElementById('speed').disabled = true;
	}
	clearInterval(showterval);//停止
	showterval = setInterval(addline,dealtime);
	document.getElementById('slow').disabled = false;

}

document.getElementById('slow').onclick=function () {
	dealtime = dealtime + 200;
	if (dealtime >= 900){
		document.getElementById('slow').disabled = true;
		dealtime = 900;
	}
	clearInterval(showterval);//停止
	showterval = setInterval(addline,dealtime);
	document.getElementById('speed').disabled = false;
}

document.getElementById('start').onclick= function() {
	if ('开始' ==document.getElementById('start').innerHTML ){
		document.getElementById('start').innerHTML ='暂停';
		//实时刷新时间单位为毫秒
	 	showterval = setInterval(addline,dealtime);
	 	document.getElementById('slow').disabled = false;
	 	document.getElementById('speed').disabled = false;
	}else {
		document.getElementById('start').innerHTML ='开始';
		clearInterval(showterval);//停止
		document.getElementById('slow').disabled = true;
	 	document.getElementById('speed').disabled = true;
	}

}

document.getElementById('buy').onclick= function() {
	costPricet = document.getElementById('price').value;
	numt = document.getElementById('num').value;
	if (costPricet<nowStockData.yestclose*0.9 | costPricet>nowStockData.yestclose*1.1){
		alert('超过价格区间');
		return;
	}
	if (numt<100){
		alert('数量不对');
		return;
	}
	if (accountInfo.available < costPricet*numt){
		alert('可用金额不对');
		return;
	}
	myinfo={
		flag:new Date().getTime(),
		code:nowStockData.code,
		costPrice:costPricet,
		action:'buy',
		num:numt
	}
	willStock[myinfo.flag] = myinfo;
	accountInfo.available -= costPricet*numt;
}
document.getElementById('sale').onclick= function() {
	costPricet = document.getElementById('price').value;
	numt = document.getElementById('num').value;
	if (costPricet<nowStockData.yestclose*0.9 | costPricet>nowStockData.yestclose*1.1){
		alert('超过价格区间');
		return;
	}
	if (numt<100){
		alert('数量不对');
		return;
	}
	let ha = myStock[nowStockData.code];
	if (!ha){
		alert('余额不足');
		return;
	}
	if (numt>ha.cannum){
		alert('余额不足');
		return;
	}
	myinfo={
			flag:new Date().getTime(),
			code:nowStockData.code,
			costPrice:costPricet,
			action:'sale',
			num:numt
		}
	willStock[myinfo.flag] = myinfo
	ha.cannum -= numt;
}



window.onload = function(){
	$.ajax({
		 type: "get",
		 dataType:'json',
		 url: "http://127.0.0.1:8000/stock/getmin/",
		 success: function(data){
			 nowStockData = data;
			 re={
				date:data.date,
				 priceArr:[],
				 avgPrice:[],
				 vol:[],
				 gap:0,
				 cost:5,
				 yestclose: data.yestclose
			 };
			 document.getElementById('price').value = data.yestclose
			 document.getElementById('start').disabled = false;
			 show(re);
		 }
	 });
		accountInfo={
			lave:100000.0,
			available:100000.0,
			market_value:0.0,
			percentage:0.0,
			book_assets:0.0,
		}
}

function checkTransaction() {
	//目前忽略 成交量
	for (let key in willStock) {
		let v = willStock[key];
		let ha = myStock[v.code]
		if ('sale'==v.action & nowStockData.priceArr[systime] >= v.costPrice){
			//卖出
			if (ha){
				let sum = ha.num*ha.costPrice - nowStockData.priceArr[systime]*v.num;
				ha.num -= parseInt(v.num);
				ha.cannum -=parseInt(v.num);
				ha.costPrice = sum/ha.num;
				delete willStock[key];
				accountInfo.lave += nowStockData.priceArr[systime]*v.num;
				accountInfo.available += nowStockData.priceArr[systime]*v.num;
				if (ha.num<=0){
					delete myStock[ha.code];
				}
			}
			delete willStock[key];
		}else if('buy'==v.action & nowStockData.priceArr[systime] <= v.costPrice){
			if (ha){
				let sum = ha.num*ha.costPrice + nowStockData.priceArr[systime]*v.num;
				ha.num +=parseInt(v.num);
				ha.costPrice = sum/ha.num;
				ha.cannum +=parseInt(v.num);
			}else {
				myStock[v.code]={
					code:v.code,
					costPrice:v.costPrice,
					num:parseInt(v.num),
					cannum:parseInt(v.num)
				}
			}
			accountInfo.lave -= nowStockData.priceArr[systime]*v.num;
			delete willStock[key];
		}

	}
}


function addline () {
	systime++;
	re.priceArr.push(nowStockData.priceArr[systime]);
	re.avgPrice.push(nowStockData.avgPrice[systime]);
	re.vol.push(nowStockData.vol[systime]);
	gapt = Math.abs(re.yestclose-nowStockData.priceArr[systime]);
	if(gapt>re.gap){
		re.gap=gapt;
	}
	show(re);
	// 检测交易是否完成
	checkTransaction()

	if (systime>240){
		clearInterval(showterval);//停止
		document.getElementById('start').innerHTML ='开始';
		document.getElementById('start').disabled = true;
		document.getElementById('slow').disabled = true;
	 	document.getElementById('speed').disabled = true;
	}
}



function updateAccountInfo() {
	let stocksum = 0;
	let stocklist = document.getElementById("stocklist");
	let size = stocklist.rows.length;
	for (let i = 1; i <size; i++) {
		stocklist.deleteRow(i);
	}
	for (let key in myStock) {
		let v = myStock[key];
		stocksum +=nowStockData.priceArr[systime] * v.num;

		var newRow =stocklist.insertRow(1) ;
		newRow.insertCell(0).innerHTML=v.code;
		newRow.insertCell(1).innerHTML=parseFloat(v.costPrice).toFixed(2);
		newRow.insertCell(2).innerHTML=parseFloat(nowStockData.priceArr[systime]).toFixed(2);
		newRow.insertCell(3).innerHTML=v.num;
		newRow.insertCell(4).innerHTML=v.cannum;
		newRow.insertCell(5).innerHTML=parseFloat(v.num*nowStockData.priceArr[systime]).toFixed(2);
	}



	// displayList.forEach(function (obj, i) {
	// 	customers.rows[i + 1].cells[0].innerHTML = obj.id;
	// 	customers.rows[i + 1].cells[1].innerHTML = obj.name;
	// 	customers.rows[i + 1].cells[2].innerHTML = obj.num;
	// })

	var val = "余额："+accountInfo.lave.toFixed(2)+
		"　可用："+accountInfo.available.toFixed(2)+
		"　市值："+stocksum.toFixed(2)+
		"　仓位："+(stocksum/(stocksum+accountInfo.lave)*100).toFixed(2)+
		"%　帐面资产："+(stocksum+accountInfo.lave).toFixed(2)+"　";
	document.getElementById('account_info').innerHTML  =val;
}

//更新用户信息
setInterval(updateAccountInfo,1*1000);










