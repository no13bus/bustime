#coding: utf-8
import click
from api.bustime import BusTime
from api.config import DISTRICT



if __name__ == '__main__':
     lineid = click.prompt(u'请输入线路id。格式为 城市区号-线路号-0 或者 城市区号-线路号-1. 1正向行使，0逆向行驶', value_proc=str)
     city = DISTRICT['022']
     search_stop_name_or_id = click.prompt(u'请输入需要查询的站点的名称或者在线路上的序号')
     city_dict = dict(BusTime.get_cities())
     cityid = city_dict[city]
     print BusTime.get_bus_realtime(lineid, cityid, search_stop_name_or_id.encode('utf-8'))
