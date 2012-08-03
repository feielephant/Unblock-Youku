#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

"""
    Automatic testing of the basic methods of Unblock Youku
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

import urlparse
import logging
import base64

try:
    from google.appengine.api import urlfetch
    is_GAE = True
except:
    import urllib2
    is_GAE = False


test_suite = [
    {
        'name': 'youku',
        'url': 'http://v.youku.com/player/getPlayList/VideoIDS/XMzkzMzkzNDYw/timezone/-04/version/5/source/out?ran=6042&password=&n=3',
        'bad': 'error',
    }, {
        'name': 'tudou',
        'url': 'http://v2.tudou.com/v.action?si=10000&ui=0&refurl=http%3A%2F%2Fwww%2Etudou%2Ecom%2Falbumplay%2FCXh6vSynthY%2FoKEKyVfvEPo%2Ehtml&sid=10000&vn=02&noCache=98333&it=122928578&st=1%2C2%2C3%2C99&hd=2&pw=',
        'bad': 'error',
        'good': 'st',
    }, {
        'name': 'pptv',
        'url': 'http://web-play.pptv.com/webplay3-110-15381505.xml&ft=0&zone=0&vvid=&type=web&rnd=0.36283910693600774',
        'bad': 'error',
        'good': 'channel',
    }, {
        'name': 'pps',
        'url': 'http://dyn.ugc.pps.tv/ip/q.php',
        'bad': '海外',
    }, {
        'name': 'sohu',
        'url': 'http://hot.vrs.sohu.com/vrs_flash.action?vid=517980&af=1&g=0&referer=http%3A//tv.sohu.com/20111223/n330048227.shtml&t=0.6285748523660004',
        'bad': '"data": null',
        'good': 'ipLimit',
    }, {
        'name': 'xunlei',
        'url': 'http://geo.js.kankan.xunlei.com/country/ip.js',
        'bad': 'kkarea = 100',
        'good': '1;',
    }, {
        'name': 'letv',
        'url': 'http://hot.vrs.letv.com/json?vid=1577735',
        'bad': '"ip":0',
        'good': '"ip":1',
    }, {
        'name': 'qiyi',
        'url': 'http://data.video.qiyi.com/v.f4v?tn=0.08166731987148523',
        'bad': 'OVERSEA',
    }, {
        'name': '163',
        'url': 'http://ipservice.163.com/isFromMainland',
        'bad': 'false',
        'good': 'true',
    }, {
        'name': 'qq',
        'url': 'http://vv.video.qq.com/getinfo?vids=4V8tKxnyAxj&platform=1&speed=0&charge=0&ran=0%2E9129553600214422&otype=xml',
        'bad': 'not authorized',
        'good': 'url',
    }, {
        'name': 'sina',
        'url': 'http://v.iask.com/v_play.php?vid=79978948&uid=6&pid=0&tid=0&plid=4004&prid=ja_7_1372464632&isAuto=1&referrer=&ran=0.5966448043473065&r=p.you.video.sina.com.cn',
        'bad': 'error',
        'good': 'timelength',
    }, {
        'name': 'cntv',
        'url': 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid=04730ed1d5d748d88e8e7f5ce23baa2c&tz=4&from=000smallWindow&url=http://player.cntv.cn/flashplayer/players/htmls/smallwindow.html?pid=04730ed1d5d748d88e8e7f5ce23baa2c&time=0&idl=32&idlr=32&modifyed=false',
        'bad': '"is_invalid_copyright":"0"',
        'good': '"is_invalid_copyright":"1"'
    }
]


def _convert_url(url):
    return 'http://yo.uku.im/?url=' + base64.b64encode(url)


def test_one(test):
    if is_GAE:
        result = urlfetch.fetch(_convert_url(test['url']), deadline=60)
        d = result.content
    else:
        result = urllib2.urlopen(_convert_url(test['url']))
        d = result.read()

    if 'bad' in test:
        if test['bad'] in d:
            return test['name'], 'failed, single bad target is enough!'
        else:
            if 'good' in test:
                if test['good'] in d:
                    return test['name'], 'passed (both targets)'
                else:
                    return test['name'], 'failed! both targets went wrong!'
            else:
                return test['name'], 'passed (single bad target)'
    elif 'good' in test:
        if test['good'] in d:
            return test['name'], 'passed (single good target)'
        else:
            return test['name'], 'failed (single good target)'
    else:
        return test['name'], 'missing both good and bad targets'


def test_all():
    num_passed = 0
    details = ''
    for t in test_suite:
        site, result = test_one(t)
        logging.info(site + ': ' + result)  # logging

        if 'passed' in result:
            num_passed += 1
        details += site + '\t' + result + '\n'

    if num_passed == len(test_suite):
        status = 'all passed'
    else:
        status = 'some failed'

    return status, details


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    print test_all()
    #print test_one(test_suite[3])
