#!/usr/bin/env python

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

NUM_REMOVED_ROOTS = 3

import tornado.web
import tornado.ioloop
import tornado.httpclient

import time
import random
from sogou import compute_sogou_tag
from hostname import validate_hostname

tornado.httpclient.AsyncHTTPClient.configure(
        "tornado.curl_httpclient.CurlAsyncHTTPClient"
)

#from pprint import pprint


disallowed_response_headers = frozenset([
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade',
    # all above are hop-by-hop headers
    'content-encoding',  # may cause decoding errors
    'content-length',
])

allowed_request_headers = frozenset([
    'accept',
    'accept-charset',
    'accept-encoding',
    'accept-language',
    'accept-datetime',
    'authorization',
    'cache-control',
    'cookie',
    'connection',
    'content-type',
    'host',
    'if-match',
    'if-modified-since',
    'if-none-match',
    'if-range',
    'if-unmodified-since',
    'pragma',
    'range',
    'referer',
    'user-agent',
])


class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST']

    def _get_real_domain(self, num_removed_roots=NUM_REMOVED_ROOTS):
        # e.g., httpbin.org.127.0.0.1.xip.io will return httpbin.org
        d = self.request.host.split(':')[0]
        if d.endswith('.127.0.0.1.xip.io'):
            return d[:-17]

        l = d.split('.')
        if len(l) <= num_removed_roots:
            return None
        return '.'.join(l[:(-num_removed_roots)])

    def _handle_response(self, response):
        self.set_status(response.code)

        #print
        #print self.request.uri
        #pprint(response.headers)

        # check the last comment of http://goo.gl/4w5yj
        for h in response.headers.keys():
            if h.lower() not in disallowed_response_headers:
                list_values = response.headers.get_list(h)
                # set_header should always be preferred
                # using only add_header will cause some problems
                # e.g. _clear_headers_for_304 doesn't work for _list_headers
                if len(list_values) == 1:
                    #print h, list_values[0]
                    self.set_header(h, list_values[0])
                else:
                    for v in list_values:
                        #print h, v
                        self.add_header(h, v)

        if response.body:
            self.write(response.body)

        #self.flush()
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        real_domain = self._get_real_domain()
        if not real_domain:
            self.send_error(403)
            return
        if not validate_hostname(real_domain):
            self.send_error(403)  # forbidden
            return

        real_url = 'http://' + real_domain + self.request.uri
        timestamp = hex(int(time.time()))[2:]
        # print '\n' + real_url

        headers = {}
        for h, v in self.request.headers.items():
            if h.lower() in allowed_request_headers:
                # print h, v
                headers[h] = v
        headers['Host'] = real_domain
        # print 'Host', real_domain
        # import sys
        # sys.stdout.flush()

        headers['X-Sogou-Auth'] = \
                hex(random.getrandbits(128))[2:-1].upper() + \
                '/30/853edc6d49ba4e27'
        headers['X-Sogou-Timestamp'] = timestamp
        headers['X-Sogou-Tag'] = compute_sogou_tag(timestamp, real_domain)

        #headers['X-Forwarded-For'] = '114.114.' + str(random.randrange(256)) \
        #        + '.' + str(random.randrange(1, 255))
        headers['X-Forwarded-For'] = '220.181.111.' \
                + str(random.randrange(1, 255))
        #print headers['X-Forwarded-For']

        rand_num = random.randrange(16 + 16)
        if rand_num < 16:
            proxy_host = 'h' + str(rand_num) + '.dxt.bj.ie.sogou.com'
        else:
            proxy_host = 'h' + str(rand_num - 16) + '.edu.bj.ie.sogou.com'

        http_req = tornado.httpclient.HTTPRequest(
            url=real_url,
            method=self.request.method,
            body=self.request.body,
            headers=headers,
            follow_redirects=False,
            allow_nonstandard_methods=True,
            proxy_host=proxy_host,
            proxy_port=80,
        )

        http_client = tornado.httpclient.AsyncHTTPClient()
        try:
            http_client.fetch(http_req, self._handle_response)

        except tornado.httpclient.HTTPError, err:
            self.handle_response(err.response)

        except Exception, err:
            self.set_status(500)
            self.write('Internal Server Error: ' + str(err))
            self.finish()

    # def self.post() as self.get()
    post = get


application = tornado.web.Application(
        [(r'.*', ProxyHandler)]
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
