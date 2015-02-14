# coding: utf-8
import json
from itertools import groupby
import requests
from cachecore import RedisCache
from .cache import cache_func


APIPREFIX = 'http://test_cheche.com/'
rediscache = RedisCache(default_timeout=3600 * 24 * 30)


class BusTime(object):
    @classmethod
    def _req_data(cls, url):
        try:
            r = requests.get('%s%s' % (APIPREFIX, url), timeout=20)
        except Exception as ex:
            print 'url=%s, error is %s' % (url, ex.message)
            return None
        c = r.content
        j = json.loads(c)
        if j['jsonr']['data']:
            return j['jsonr']['data']
        else:
            print 'wrong message is %s' % j['jsonr']['errmsg']
            return None

    @classmethod
    @cache_func(rediscache, None)
    def get_cities(cls):
        '''独上西楼 望断天涯路'''
        url = 'wowwow/city!more.action?v=1.3.2'
        data = cls._req_data(url)
        data_cities = data['cities']
        if data and data_cities:
            return {city['cn']:city['cd'] for city in data_cities}
        else:
            return None

    @classmethod
    def search_by_stopname(cls, stopname, cityid):
        url = 'busno/stop!slist.action?stop={0}&cityId={1}'.format(stopname.encode('utf-8'), cityid)
        data = cls._req_data(url)
        data_has_lines = 'lines' in data
        if data and data_has_lines:
            lines = data['lines']
            sortkeyfn = lambda s: s['nextStop']
            lines.sort(key=sortkeyfn)
            result_list = [u'开往{0}方向的线路有{1}条'.format(k, len(list(v))) for k, v in groupby(lines, key=sortkeyfn)]
            return '\n'.join(result_list)
        else:
            return None

    @classmethod
    @cache_func(rediscache, timeout=3600)
    def get_line_infos(cls, lineno, cityid):
        url = 'busno/query!q.action?ln=%s&v=1.3.2&cityId=%s' % (lineno, cityid)
        data = cls._req_data(url)
        data_has_line = 'line' in data
        line_list = data['linelist']
        if data and data_has_line:
            line_info = data['line']
            return line_info
        elif data and (not data_has_line) and len(line_list) > 0:
            return line_list
        else:
            return None

    @classmethod
    @cache_func(rediscache, None)
    def get_real_line_infos(cls, lineid, cityid):
        url = 'busno/line!m2.action?lineId=%s&cd=%s' % (lineid, cityid)
        data = cls._req_data(url)
        data_has_line = 'line' in data
        if data and data_has_line:
            line_info = data['line']
            return line_info
        else:
            return None

    @classmethod
    def get_bus_realtime(cls, lineid, cityid, search_stop_name_or_id):
        if isinstance(search_stop_name_or_id, int):
            search_stop_name_or_id = str(search_stop_name_or_id)
        url = 'bus/line!m2.action?ld=%s&cityId=%s' % (lineid, cityid)
        data = cls._req_data(url)
        line_orders = cls.get_line_orders(lineid, cityid)
        order = 0
        if data and line_orders and ('bus' in data) and data['bus']:
            for k, v in iter(line_orders):
                if str(k) == search_stop_name_or_id or v == search_stop_name_or_id:
                    order = k
                    break
            if not order:
                print u'找不到该站点'
                return None
            bus_list = filter(lambda x: x['order'] <= order, data['bus'])
            if not bus_list:
                return u'距离上次发车时间为{0}分钟'.format(data['busBehindTime'])

            max_order_dict = max(bus_list, key=lambda x: x['order'])
            max_order = max_order_dict['order']
            if order > max_order:
                remaining_num = order - max_order
                return u'最近一辆车{0}秒前报告位置, 距离本站{1}站'.format(max_order_dict['lastTime'], remaining_num)
            elif order == max_order:
                return u'最近一辆车{0}秒前报告位置, 即将到站. 距离{1}米'.format(max_order_dict['lastTime'], max_order_dict['distance'])
        elif data['nobustip']:
            return data['nobustip']
        else:
            return None

    @classmethod
    @cache_func(rediscache, None)
    def get_line_orders(cls, lineid, cityid):
        url = 'busno/line!m2.action?&cd=%s' % (lineid, cityid)
        data = cls._req_data(url)
        data_map = data['map']
        if data and data_map:
            return [(i['order'], i['stopName']) for i in data_map]
        else:
            return None
