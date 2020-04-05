var num =10
var dealtime = 500;
var systime = 0;
var showterval;
let re={};
let accountInfo ={}
mdata1 = [];




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


window.onload = function(){
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
			 console.log(data.priceArr.length)
			 document.getElementById('start').disabled = false;
			 show(re);


		 }
	 });
		accountInfo={
			lave:0.0,
			available:0.0,
			market_value:0.0,
			percentage:0.0,
			book_assets:0.0,
		}
		updateAccountInfo(accountInfo);
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



function addline () {
	re.priceArr.push(mdata1.priceArr[systime]);
	re.avgPrice.push(mdata1.avgPrice[systime]);
	re.vol.push(mdata1.vol[systime]);
	gapt = Math.abs(re.yestclose-mdata1.priceArr[systime]);
	if(gapt>re.gap){
		re.gap=gapt;
	}

	show(re);
	updateAccountInfo(accountInfo);

	systime++;
	if (systime>240){
		clearInterval(showterval);//停止
		document.getElementById('start').innerHTML ='开始';
		document.getElementById('start').disabled = true;
		document.getElementById('slow').disabled = true;
	 	document.getElementById('speed').disabled = true;
	}
}



function updateAccountInfo(accountInfo) {
	var val = "余额："+accountInfo.lave+"万　可用："+accountInfo.lave+"万　市值："+accountInfo.lave+"万　仓位："+"%　帐面资产："+accountInfo.lave+"万　";


	document.getElementById('account_info').innerHTML  =val;
}











