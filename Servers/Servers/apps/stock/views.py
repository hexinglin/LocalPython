#coding=utf8
import numpy as np
import pandas as pd

from django.http import HttpResponse

import tushare as ts
ts.set_token('cf3228b45527b18b17e20f2266d5abbdeb4600bcebf4a8b64c545176')
def get_test_data(request):
    df = ts.pro_bar(ts_code='000001.SZ', start_date='20180101', end_date='20181011', ma=[5, 20, 50])
    return HttpResponse(df.values,content_type='application/json')