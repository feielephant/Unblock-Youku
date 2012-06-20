#!/usr/bin/env pypy

_valid_hostnames = frozenset([
    'hot.vrs.sohu.com',
    'hot.vrs.letv.com',
    'data.video.qiyi.com',
    'vv.video.qq.com',
    'geo.js.kankan.xunlei.com',
    'v2.tudou.com',
    'web-play.pptv.com',
    'dyn.ugc.pps.tv',
    's.plcloud.music.qq.com',
    'inner.kandian.com',
    'ipservice.163.com',
    'zb.s.qq.com',

    'v.youku.com',
    'v.iask.com',
#    'http://*.gougou.com/*',
])


def validate_hostname(h):
    if h in _valid_hostnames:
        return True
#    elif h.endswith('.gougou.com'):
#        return True
    else:
        return False


if __name__ == '__main__':
    hostnames = (
        'v.youku.com',
        'vv.youku.com',
    )

    for h in hostnames:
        print h, validate_hostname(h)
