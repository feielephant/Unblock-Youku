#!/usr/bin/env python

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


class ProxyHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST']

    def _get_real_domain(self, num_removed_roots=NUM_REMOVED_ROOTS):
        # e.g., httpbin.org.127.0.0.1.xip.io will return httpbin.org
        d = self.request.host.split(':')[0]
        if d.endswith('.127.0.0.1.xip.io'):
            return d[:-17]

        l = d.split('.')
        assert len(l) > num_removed_roots
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
    def get(self, uri):
        real_domain = self._get_real_domain()
        #if not validate_hostname(real_domain):
        #    self.send_error(403)  # forbidden
        #    return

        real_url = 'http://' + real_domain + uri
        timestamp = hex(int(time.time()))[2:]
        sogou_tag = compute_sogou_tag(timestamp, real_domain)

        #print real_domain
        #print real_url
        #print timestamp
        #print sogou_tag

        headers = self.request.headers
        if 'Host' in headers:
            headers['Host'] = real_domain
        #headers = {(h, v) for h, v in headers.items()
        #        if not h.startswith('X-')}
        headers['X-Sogou-Auth'] = \
                '9CD285F1E7ADB0BD403C22AD1D545F40/30/853edc6d49ba4e27'
        headers['X-Sogou-Timestamp'] = timestamp
        headers['X-Sogou-Tag'] = sogou_tag
        headers['X-Forwarded-For'] = '114.114.114.114'

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
        [(r'(.*)', ProxyHandler)],
        debug=True  # please set to false in production environments
)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
