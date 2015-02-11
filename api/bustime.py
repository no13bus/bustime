#coding: utf-8
import time
import datetime
import json
from itertools import groupby
import requests
from cachecore import RedisCache
from .cache import cache_func

APIPREFIX = 'http://api.chelaile.net.cn:7000/'
rediscache = RedisCache(default_timeout=3600*24*30)

class BusTime(object):
    @classmethod
    def _req_data(cls, url):
        try:
            r = requests.get('%s%s' % (APIPREFIX, url), timeout=20)
        except Exception as ex:
            print 'url=%s, error is %s' % (url, ex.message)
            return None
        c = r.content
        c = c.replace('**YGKJ','').replace('YGKJ##','')
        j = json.loads(c)
        if j['jsonr']['data']:
            return j['jsonr']['data']
        else:
            print 'wrong message is %s' % j['jsonr']['errmsg']
            return None

    @classmethod
    @cache_func(rediscache, None)
    def get_cities(cls):
        url = 'wow/city!morecities.action?sign=&s=android&v=1.3.2'
        data = cls._req_data(url)
        data_cities = data['cities']
        if data and data_cities:
            return [(city['cityName'], city['cityId']) for city in data_cities]
        else:
            return None

    '''根据站点名字查找公交车路线 返回的是字典数据格式 {开往方向:线路list}
       每个线路的属性包括下面的属性
        "direction": 0, 方向 1为反方向
        "endStopName": "杨村客运站", 终点站
        "leftStop": 3,
        "leftStopNum": 3, leftStopNum意思是说该线路上面的最近的一个车距离本站还有多少站 -2暂无数据 -1尚未发车 1 即将到站
        "lineId": "022-607-0",
        "lineName": "607", 公交车的名字
        "lineNo": "607",
        "nextStop": "九十二中", 下一站名称 也就是开往何方向的意思
        "proTime": -1,
        "startStopName": "天津站后广场" 始发站
    '''
    @classmethod
    def search_by_stopname(cls, stopname, cityid):
        result = {}
        url = 'bus/stop!stoplist.action?stopName=%s&s=android&v=1.3.2&cityId=%s&sign=' % (stopname, cityid)
        data = cls._req_data(url)
        
        data_has_lines = 'lines' in data
        if data and data_has_lines:
            lines = data['lines']
            sortkeyfn = lambda s:s['nextStop']
            lines.sort(key=sortkeyfn)
            for k, v in groupby(lines, key=sortkeyfn):
                print v
                result[k] = list(v)
            return result
        else:
            return None

    '''
        examples:
        LsName: 610
    '''
    @classmethod
    @cache_func(rediscache, None)
    def get_line_infos(cls, lineNo, cityid):
        url = 'bus/query!search.action?LsName=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineNo, cityid)
        data = cls._req_data(url)
        data_has_line = 'line' in data
        line_list = data['linelist']
        if data and data_has_line:
            line_info = data['line']
            return line_info
        elif data and (not data_has_line) and len(line_list) > 0:
            lineId = line_list[0]['lineId']
            lineNo = lineId.split('-')[1]
            url = 'bus/query!search.action?LsName=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineNo, cityid)
            print url
            data = cls._req_data(url)
            line_info = data['line']
            return line_info
        else:
            return None

    @classmethod
    def get_bus_realtime(cls, lineId, cityid, search_stop_name):
        url = 'bus/line!map2.action?lineId=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineId, cityid)
        data = cls._req_data(url)
        result = {}
        if data:
            line_orders = cls.get_line_orders(lineId, cityid)
            if line_orders:
                pass
            search_stop_name

        if data['bus']:
            bus_list = filter(lambda x: x['order'] <= order, data['bus'])
            if bus_list:
                max_order = max(bus_list, key=lambda x:x['order'])
                if max_order == order:
                    print u'即将到站'
                    print u'距离为%s'
                else:
                    remaining_num = order - max_order
                    print u'还有%s站' % remaining_num

    @classmethod
    @cache_func(rediscache, None)
    def get_line_orders(cls, lineId, cityid):
        url = 'bus/line!map2.action?lineId=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineId, cityid)
        data = cls._req_data(url)
        data_map = data['map']
        if data and data_map:
            return [(i['order'], i['stopName']) for i in data_map]
        else:
            return None