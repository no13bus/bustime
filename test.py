# coding: utf-8
__author__ = 'no13bus'
from api.bustime import BusTime

if __name__ == '__main__':
    # stop names in an line
    line_orders = BusTime.get_line_orders('022-610-0', '006')
    for _, stopname in iter(line_orders):
        print stopname
    # cities
    cities = BusTime.get_cities()
    for city, cityid in iter(cities):
        print city, cityid
    # line_infos
    lineinfo = BusTime.get_line_infos(u'610', '006')
    if lineinfo:
        print '{0}->{1}\n首:{2}  终:{3}'.format(lineinfo['startStopName'].encode('utf-8'), lineinfo['endStopName'].encode('utf-8'), lineinfo['firstTime'].encode('utf-8'), lineinfo['lastTime'].encode('utf-8'))
    else:
        print u'没有查到该线路相关信息'
    lineinfo1 = BusTime.get_line_infos(u'611', '006')
    if lineinfo1:
        print '{0}->{1}\n首:{2}  终:{3}'.format(lineinfo1['startStopName'].encode('utf-8'), lineinfo1['endStopName'].encode('utf-8'), lineinfo1['firstTime'].encode('utf-8'), lineinfo1['lastTime'].encode('utf-8'))
    else:
        print u'没有查到该线路相关信息'
    # realtime bus
    bus_realtime_result = BusTime.get_bus_realtime('022-610-0', '006', u'南市')
    print bus_realtime_result
    # 简单的返回按照站点搜索经过该站点的公交车情况
    search = BusTime.search_by_stopname(u'南市', '006')
    print search