#coding: utf-8
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
    print lineinfo
    lineinfo1 = BusTime.get_line_infos(u'611', '006')
    print lineinfo1