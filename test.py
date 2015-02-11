#coding: utf-8
__author__ = 'no13bus'
from api.BusTime import BusTime

if __name__ == '__main__':
    print BusTime.get_bus_infos(u'化工大楼', '006')