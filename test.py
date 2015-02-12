# coding: utf-8
from api.bustime import BusTime

if __name__ == '__main__':
    # stop names in an line
    line_orders = BusTime.get_line_orders('022-610-0', '006')
    for _, stopname in iter(line_orders):
        print stopname
    # cities
    cities = BusTime.get_cities()
    for city in cities:
        print u'城市=%s 城市id=%s' % (city, cities[city])
    # line_infos
    # lineinfo = BusTime.get_line_infos('610', '006')
    lineinfo = BusTime.get_line_infos('611', '006')
    if lineinfo and isinstance(lineinfo, dict):
        print u'%s->%s\n首:%s  终:%s' % (lineinfo['startStopName'], lineinfo['endStopName'], lineinfo['firstTime'], lineinfo['lastTime'])
    elif lineinfo and isinstance(lineinfo, list):
        print u'亲 没找到呢。猜你想查找的是下面的线路:\n' + '\n'.join([line['lineId'] for line in lineinfo])
    else:
        print u'没有查到该线路相关信息'
    
    # realtime bus
    # bus_realtime_result = BusTime.get_bus_realtime('022-610-0', '006', u'化工大楼')
    bus_realtime_result = BusTime.get_bus_realtime('022-610-0', '006', '22')
    print bus_realtime_result
    # 简单的返回按照站点搜索经过该站点的公交车情况
    search = BusTime.search_by_stopname(u'南市', '006')
    print search