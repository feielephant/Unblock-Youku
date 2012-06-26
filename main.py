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

import webapp2
import logging
from autotest import test_all
from report import report


logging.getLogger().setLevel(logging.INFO)


class TestHandler(webapp2.RequestHandler):
    def get(self):
        try:
            test_status, test_details = test_all()
            report('Unblock Youku Autotest [' + test_status + ']',
                    test_details)
        except Exception as detail:
            logging.exception(str(detail))
            import traceback
            report(str(detail).splitlines()[0], traceback.format_exc())


app = webapp2.WSGIApplication([
    ('/autotest', TestHandler),
])
