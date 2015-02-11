# bustime
提供实时的公交车信息查询以及api接口 支持微信公共号查询


get_line_infos
# return
# "line": {
#     "direction": 1,
#     "endStopName": "唐山道",
#     "firstTime": "5:30",
#     "lastTime": "20:40",
#     "lineId": "022-610-1",
#     "lineName": "610",
#     "lineNo": "610",
#     "startStopName": "柴楼新庄园公交站",
#     "stopsNum": "32"
# },

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