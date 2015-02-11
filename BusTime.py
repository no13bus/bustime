#coding: utf-8
import time
import datetime
import json
from itertools import groupby
import requests
from cachecore import SimpleCache, MemcachedCache, RedisCache, FileSystemCache
from .cache import cache_func


APIPREFIX = 'http://api.chelaile.net.cn:7000/'
rediscache = RedisCache(default_timeout=3600*24*30)


class BusTime(object):
    @classmethod
    def _req(cls, url, date_type):
        try:
            r = requests.get('%s%s' % (APIPREFIX, url), timeout=20)
        except Exception as ex:
            print 'url=%s, error is %s' % (url, ex.message)
            return None
        c = r.content
        c = c.replace('**YGKJ','').replace('YGKJ##','')
        j = json.loads(c)
        if j['jsonr']['data'] and j['jsonr']['data'][date_type]:
            return j['jsonr']['data'][date_type]
        elif j['jsonr']['data'] and (not j['jsonr']['data'][date_type]):
            print '%s is none' % date_type
            return None
        else:
            print 'req is wrong, message is %s' % j['jsonr']['errmsg']
            return None

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
            print 'req is wrong, message is %s' % j['jsonr']['errmsg']
            return None


    '''得到城市字典 {'004':u'杭州','006',u'天津', ....}'''
    @classmethod
    def get_cities(cls):
        url = 'wow/city!morecities.action?sign=&s=android&v=1.3.2'
        allcities = cls._req(url,'cities')
        result = {}
        if allcities:
            map(lambda x:result.setdefault(x['cityId'],x['cityName']), allcities)
            return result
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
        lines = cls._req(url, 'lines')
        if not lines:
            return None
        sortkeyfn = lambda s:s['nextStop']
        lines.sort(key=sortkeyfn)
        for key,valuesiter in groupby(lines, key=sortkeyfn):
            print valuesiter
            result[key] = list(valuesiter)
        return result

    '''通过公交车的号进行搜索公车 得到该路线的相关的详细信息 如发车 起始点等信息'''
    @classmethod
    def get_bus_infos(cls, busNo):
        url = 'bus/query!search.action?LsName=%s&s=android&v=1.3.2&cityId=%s&sign=' % (busNo, cityid)
        # result = {}
        data = _req_data(url)
        if not data:
            return None
        ## 路线的各个站点的名称和gps信息
        # bus_map = {}
        # if data['map']:
        #     map(lambda x:bus_map.setdefault(x['order'],x['stopName']), data['map'])
        ## 路线的发车 起始点等信息
        line_info = data['line']
        # result['bus_map'] = bus_map
        # result['line_info'] = line_info
        return line_info

    '''通过提供lineid线路id以及你要定位的车站名字来查找当前你定位的车站距离最近的车的距离和时间
       该接口还有该路线的各个站点的id和经纬度 以及站点名称
    '''
    @classmethod
    def get_bus_realtime(cls, lineId, cityid, search_stop_name):
        url = 'bus/line!map2.action?lineId=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineId, cityid)
        data = _req_data(url)
        result = {}
        if not data:
            return None
        if data['otherlines']:
            result['other_line'] = data['otherlines'][0]['lineId']
        bus_map = {}
        if data['map']:
            order_list = filter(lambda x:x['stopName'].index(search_stop_name), data['map'])
            if order_list:
                order = order_list[0]['order']

        if data['bus']:
            bus_list = filter(lambda x: x['order'] <= order, data['bus'])
            if bus_list:
                max_order = max(bus_list, key=lambda x:x['order'])
                if max_order == order:
                    print u'即将到站'
                    # print u'距离为%s' max_order['distance']
                else:
                    remaining_num = order - max_order
                    print u'还有%s站' % remaining_num

    @classmethod
    @cache_func(rediscache, None)
    def get_bus_orders(cls, lineId, cityid):
        url = 'bus/line!map2.action?lineId=%s&s=android&v=1.3.2&cityId=%s&sign=' % (lineId, cityid)
        data = _req_data(url)
        if not data:
            return None
        if data['map']:
            return ((i['order'], i['stopName']) for i in data['map'])
        else:
            return None




       
if __name__ == '__main__':
    # print BusTime.get_cities()
    print BusTime.get_bus_infos(u'化工大楼', '006')
    # print BusTime.search_by_busno('879')

# url = 'http://api.chelaile.net.cn:7000/bus/line!map2.action?lineId=022-610-0&s=IOS&v=2.9&cityId=006&sign'
# r=requests.get(url)
# c=r.content
# cc=c.replace('**YGKJ','').replace('YGKJ##','')
# len(json.loads(cc)['jsonr']['data']['bus'])

# url1='http://api.chelaile.net.cn:7000//bus/line!gps.action?lineId=022-610-0&s=IOS&v=2.9&cityId=006&sign='



# r=requests.get(url2)
# c=r.content
# cc=c.replace('**YGKJ','').replace('YGKJ##','')
# json.loads(cc)['jsonr']['data']['gps']

# {
# "carNo": "10224",
# "jingdu": 117.194007978736,
# "weidu": 39.1667495879065
# },
# {
# "carNo": "11773",
# "jingdu": 117.192327576791,
# "weidu": 39.1554654940316
# },
# {
# "carNo": "11788",
# "jingdu": 117.193738284597,
# "weidu": 39.1567202653248
# },