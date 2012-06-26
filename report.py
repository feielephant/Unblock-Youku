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

from google.appengine.api import mail
import datetime


def report(title, body):
    current_time = datetime.datetime.now().ctime()
    mail.send_mail(
        sender='unblock.youku@gmail.com',
        to='unblock-youku-autotest-report@zhuzhu.org',
        subject=title + ' (' + current_time + ')',
        body=body + '\n\n' + current_time
    )
