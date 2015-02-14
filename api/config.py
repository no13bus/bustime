# coding: utf-8
__author__ = 'no13bus'


DISTRICT = {
    '0571': u'杭州',
    '022': u'天津',
    '023': u'重庆',
    '028': u'成都',
    '0931': u'兰州',
    '0791': u'南昌',
    '0371': u'郑州',
    '0769': u'东莞',
    '0532': u'青岛',
    '0512': u'苏州',
    '0991': u'乌鲁木齐',
    '0577': u'瑞安',
    '0757': u'佛山',
    '0755': u'深圳',
    '0411': u'中山',
    '0351': u'太原',
    '0752': u'惠州',
    '027': u'武汉',
    '0374': u'许昌',
    '0310': u'邯郸',
    '0391': u'焦作',
}

# weixin api setting
WEIXIN_TOKEN = ''
WEIXIN_SENDER = ''
WEIXIN_EXPIRES_IN = ''



try:
    from config_dev import *
except Exception, e:
    pass