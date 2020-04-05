#coding=utf8

'''
/*
 * 计算EMA指数平滑移动平均线，用于MACD
 * @param {number} n 时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
'''
def calcEMA(n,data,field=None):
    a=2/(n+1)
    if(field):
        #二维数组
        ema=[data[0][field]]
        for i in range(1, len(data)):
            ema.append((a*data[i][field]+(1-a)*ema[i-1]))
    else:
        #普通一维数组
        ema=[data[0]]
        for i in range(1, len(data)):
            ema.append((a*data[i]+(1-a)*ema[i-1]))
    return ema


'''
/*
 * 计算DIF快线，用于MACD
 * @param {number} short 快速EMA时间窗口
 * @param {number} long 慢速EMA时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
'''
def calcDIF(short,long,data,field):
    dif=[]
    emaShort=calcEMA(short,data,field)
    emaLong=calcEMA(long,data,field)
    for i in range(0,len(data)):
        dif.append((emaShort[i]-emaLong[i]))

    return dif

'''
/*
 * 计算DEA慢线，用于MACD
 * @param {number} mid 对dif的时间窗口
 * @param {array} dif 输入数据
 */
'''

def calcDEA(mid,dif):
    return calcEMA(mid,dif)



'''
/*
 * 计算MACD
 * @param {number} short 快速EMA时间窗口
 * @param {number} long 慢速EMA时间窗口
 * @param {number} mid dea时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
'''
def calcMACD (short,long,mid,data,field):
    result={}
    macd=[]
    dif=calcDIF(short,long,data,field)
    dea=calcDEA(mid,dif)
    for i in range(0,len(data)):
        macd.append(((dif[i]-dea[i])*2))

    result['dif']=dif
    result['dea']=dea
    result['macd']=macd
    return result
