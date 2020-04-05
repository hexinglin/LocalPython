#coding=utf8

import json

from django.http import HttpResponse


def get_account_info(request):

    redata ={
        'lave':0,
        'available': 0,
        'market_value': 0,
        'percentage':0,
        'book_assets': 0,
    }
    return HttpResponse(json.dumps(redata),content_type='application/json')
