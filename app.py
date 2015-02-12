# coding: utf-8
from flask import Flask, render_template, request
from flask_weixin import Weixin
from api.bustime import BusTime


app = Flask(__name__)
app.config.from_object('config')
weixin = Weixin(app)
app.add_url_rule('/wechat', view_func=weixin.view_func)


@weixin.register('*')
def query(**kwargs):
    username = kwargs.get('sender')
    sender = kwargs.get('receiver')
    message_type = kwargs.get('type')
    content = kwargs.get('content')

    if message_type == 'event' and kwargs.get('event') == 'subscribe':
        msg = app.config.get('ON_FOLLOW_MESSAGE')
        if not msg:
            return ''

        return weixin.reply(
                   username, type='news', sender=sender, articles=[msg]
               )


    if not content:
        reply = u'我好笨笨哦，还不懂你在说什么'
        return weixin.reply(username, sender=sender, content=reply)
    cs = content.split('-')
    if len(cs) != 4:
        reply = "not fit the format. it need 3 '-'"
        return weixin.reply(username, sender=sender, content=reply)
    elif not cs[0] in app.config.get('DISTRICT'):
        reply = "this city I can not find"
        return weixin.reply(username, sender=sender, content=reply)
    cityname = app.config.get('DISTRICT')[cs[0]]
    cityid = BusTime.get_cities()[cityname]
    lineinfo = BusTime.get_line_infos(cs[1], cityid)
    if not lineinfo:
        reply = 'can not find this bus line'
        return weixin.reply(username, sender=sender, content=reply)
    elif lineinfo and isinstance(lineinfo, list):
        reply = u'亲 没找到呢。猜你想查找的是下面的线路id:\n' + '\n'.join([line['lineId'] for line in lineinfo])
        return weixin.reply(username, sender=sender, content=reply)
    lineid = lineinfo['lineId']
    search_stop_name_or_id = cs[-1]
    reply_businfo = u'%s->%s\n首:%s  终:%s\n' % (lineinfo['startStopName'], lineinfo['endStopName'], lineinfo['firstTime'], lineinfo['lastTime'])
    reply_realtime_info = BusTime.get_bus_realtime(lineid, cityid, search_stop_name_or_id)
    if not reply_realtime_info:
        reply_realtime_info = 'can not get the realtime info'
    print reply_businfo, reply_realtime_info
    reply = '%s  %s' % (reply_businfo, reply_realtime_info)
    return weixin.reply(username, sender=sender, content=reply)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)