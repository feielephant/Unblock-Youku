#!/usr/bin/env pypy

"""
    Unblock Youku Server. A redirecting proxy server for Unblock-Youku
    Copyright (C) 2012 Bo Zhu http://zhuzhu.org

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

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
    'ip.kankan.xunlei.com',

    'v.youku.com',
    'v.iask.com',
#    'http://*.gougou.com/*',

    'zhuzhu.org',  # for debug
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
