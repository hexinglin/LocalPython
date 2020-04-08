#coding=utf8
import pandas as pd

from Servers.apps.stock.service.MACDUtil import calcMACD
import json
import os
from django.http import HttpResponse
import tushare as ts
from django.conf import settings
from datetime import datetime,timedelta

ts.set_token('cf3228b45527b18b17e20f2266d5abbdeb4600bcebf4a8b64c545176')
def get_test_data(request):
    df = ts.pro_bar(ts_code='002455.SZ', start_date='20180501', end_date='20181051', ma=[5,10, 20, 30])
    df =df.dropna(axis=0,how='any')
    df = df.sort_values(by='trade_date',ascending=True)

    order = ['ts_code','trade_date' ,'open', 'close', 'low', 'high', 'pre_close', 'change','pct_chg', 'vol', 'amount', 'ma5', 'ma_v_5','ma10', 'ma_v_10' ,'ma20' ,'ma_v_20', 'ma30', 'ma_v_30']
    df = df[order]

    macd = calcMACD(12,26,9,df.values[:, 2:6].tolist(),1)

    redata ={
        'code':'002455.SZ',
        'times':df.values[:,1].tolist(),
        'datas': df.values[:, 2:6].tolist(),
        'vols': df.values[:, 9].tolist(),
        'ma5': df.values[:, 11].tolist(),
        'ma10': df.values[:, 13].tolist(),
        'ma20': df.values[:, 15].tolist(),
        'ma30': df.values[:, 17].tolist(),
        'dif': macd['dif'],
        'dea': macd['dea'],
        'macd': macd['macd']
    }
    return HttpResponse(json.dumps(redata),content_type='application/json')


def getMinData(stockcode, stocktime):
    try:
        datadfo = pd.read_csv(settings.BASE_DIR + "/static/stock/"+stockcode.split('.')[0]+"/min-"+stocktime+".csv")
        if datadfo.shape[0] ==241:
            datadfo = datadfo.sort_values(by='trade_time', ascending=True)
            return datadfo
    except:
        pass
    return None


def getMindataByBase(stockcode, stocktime):
    all_e_date = datetime.strptime(stocktime, '%Y%m%d')
    all_s_date = all_e_date - timedelta(days=30)
    datadfo = pd.read_csv(settings.BASE_DIR+"/static/Result1.csv")
    datadfo = datadfo.sort_values(by='trade_time', ascending=True)
    timedf = pd.to_datetime(datadfo['trade_time'], infer_datetime_format=True)

    if not os.path.exists(settings.BASE_DIR + "/static/stock/"+stockcode.split('.')[0]):
        os.makedirs(settings.BASE_DIR + "/static/stock/"+stockcode.split('.')[0])

    for i in range(31):
        s_date = all_s_date +timedelta(days=i)
        e_date = all_s_date + timedelta(days=(i+1))
        datadsave = datadfo[(timedf >= s_date) & (timedf <= e_date)]
        if datadsave.shape[0] ==241:
            datadsave.to_csv(settings.BASE_DIR + "/static/stock/"+stockcode.split('.')[0]+"/min-"+s_date.strftime('%Y%m%d')+".csv")



def get_Min_data(request):
    stockcode =request.GET['code']
    stocktime = request.GET['time']
    #查询是否含有文件
    datadf = getMinData(stockcode,stocktime)
    if datadf is None:
        #如果没有下载文件
        getMindataByBase(stockcode,stocktime)
        datadf = getMinData(stockcode, stocktime)
    if datadf is None:
        return HttpResponse(json.dumps({}), content_type='application/json')

    avgPrice=[]
    Tamount = 0
    Tvol = 0
    for index, row in datadf.iterrows():
        Tamount += row['amount']
        Tvol += row['vol']
        avgPrice.append(round(Tamount / Tvol, 2))
    redata ={
        'date':stocktime,
        'code': '002455.SZ',
        'priceArr': datadf['close'].tolist(),
        'avgPrice': avgPrice,
        'vol': datadf['vol'].tolist(),
        'yestclose':5.06
    }
    return HttpResponse(json.dumps(redata),content_type='application/json')