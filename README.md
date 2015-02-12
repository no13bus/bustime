# bustime
提供实时的公交车信息查询以及api接口 支持微信公共号查询


## 接口 (see api folder)
- 根据城市区号, 公交路线的号码, 正逆向, 站点序号或者名字来查询当前距离你最近的公交车的实时跟踪情况 (get_bus_realtime)
- 提供支持实时查询的城市列表 (get_cities)
- 单个路线的详细信息查询(起点 终点 首发时间和终点时间) (get_line_infos and get_real_line_infos)
- 单个路线的各个站点的名称查询 (get_line_orders)
- 具体使用方法见 test.py里面的例子

## 提供一个简单命令行查询接口。
- 直接执行 `python query.py`

## 提供一个查询实时公交信息的微信公共号
- ![image](https://raw.githubusercontent.com/no13bus/bustime/master/weixin.jpg)

## 欢迎fork star和提issue
