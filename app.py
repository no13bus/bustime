# coding: utf-8
from flask import Flask, render_template, request
from flask_weixin import Weixin
from api.bustime import BusTime


app = Flask(__name__)
app.config.from_object('config')
weixin = Weixin(app)
app.add_url_rule('/wechat', view_func=weixin.view_func)
Tip_MESSAGE = u'查询格式为 "城市区号-线路号-正逆向-站点序号或者站点名字".\n1代表正向行使，0代表逆向行驶\n例子: 022-610-0-12 或 022-610-1-马庄'
ERROR_MESSAGE = u'亲 请输入正确的格式呦\n' + Tip_MESSAGE

@weixin.register('*')
def query(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content')
    if message_type == 'event' and kwargs.get('event') == 'subscribe':
        return weixin.reply(username, type='news', sender=sender, content=Tip_MESSAGE)
    if message_type != 'text' or (not content):
        return weixin.reply(username, sender=sender, content=ERROR_MESSAGE)
    cs = content.split('-')
    if len(cs) != 4:
        return weixin.reply(username, sender=sender, content=ERROR_MESSAGE)
    elif not cs[0] in app.config.get('DISTRICT'):
        reply = u"目前不支持此城市的查询"
        return weixin.reply(username, sender=sender, content=reply)
    cityname = app.config.get('DISTRICT')[cs[0]]
    cityid = BusTime.get_cities()[cityname]
    lineinfo = BusTime.get_line_infos(cs[1], cityid)
    if not lineinfo:
        reply = u'目前查询不到该线路的信息, 稍后试试呢'
        return weixin.reply(username, sender=sender, content=reply)
    elif lineinfo and isinstance(lineinfo, list):
        reply = u'亲 没找到呢。猜你想查找的是下面的线路id:\n' + '\n'.join([line['lineId'] for line in lineinfo])
        return weixin.reply(username, sender=sender, content=reply)

    lineid = '-'.join.(cs[0:3])
    search_stop_name_or_id = cs[-1]
    reply_businfo = u'%s->%s\n首:%s  终:%s\n' % (lineinfo['startStopName'], lineinfo['endStopName'], lineinfo['firstTime'], lineinfo['lastTime'])
    reply_realtime_info = BusTime.get_bus_realtime(lineid, cityid, search_stop_name_or_id)
    if not reply_realtime_info:
        reply_realtime_info = u'获取不到实时公交信息, 稍后试试呢'
    print reply_businfo, reply_realtime_info
    reply = '%s  %s' % (reply_businfo, reply_realtime_info)
    return weixin.reply(username, sender=sender, content=reply)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)