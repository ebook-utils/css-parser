from __future__ import unicode_literals, division, absolute_import, print_function
from . import errorhandler
from email.message import Message
from google.appengine.api import urlfetch
import sys
"""GAE specific URL reading functions"""


PY3 = sys.version_info[0] >= 3

__all__ = ['_defaultFetcher']
__docformat__ = 'restructuredtext'
__version__ = '$Id: tokenize2.py 1547 2008-12-10 20:42:26Z cthedot $'

# raises ImportError of not on GAE

log = errorhandler.ErrorHandler()


def _defaultFetcher(url):
    """
    uses GoogleAppEngine (GAE)
        fetch(url, payload=None, method=GET, headers={}, allow_truncated=False)

    Response
        content
            The body content of the response.
        content_was_truncated
            True if the allow_truncated parameter to fetch() was True and
            the response exceeded the maximum response size. In this case,
            the content attribute contains the truncated response.
        status_code
            The HTTP status code.
        headers
            The HTTP response headers, as a mapping of names to values.

    Exceptions
        exception InvalidURLError()
            The URL of the request was not a valid URL, or it used an
            unsupported method. Only http and https URLs are supported.
        exception DownloadError()
            There was an error retrieving the data.

            This exception is not raised if the server returns an HTTP
            error code: In that case, the response data comes back intact,
            including the error code.

        exception ResponseTooLargeError()
            The response data exceeded the maximum allowed size, and the
            allow_truncated parameter passed to fetch() was False.
    """
    # from google.appengine.api import urlfetch
    try:
        r = urlfetch.fetch(url, method=urlfetch.GET)
    except urlfetch.Error as e:
        log.warn('Error opening url=%r: %s' % (url, e),
                 error=IOError)
    else:
        if r.status_code == 200:
            # find mimetype and encoding
            mimetype = 'application/octet-stream'
            try:
                m = Message()
                m['content-type'] = r.headers['content-type']
                encoding = m.get_param('charset')
            except KeyError:
                encoding = None
            if mimetype != 'text/css':
                log.error('Expected "text/css" mime type for url %r but found: %r' %
                          (url, mimetype), error=ValueError)
            return encoding, r.content
        else:
            # TODO: 301 etc
            log.warn('Error opening url=%r: HTTP status %s' %
                     (url, r.status_code), error=IOError)
