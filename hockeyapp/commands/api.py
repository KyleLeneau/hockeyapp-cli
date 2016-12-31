"""
Extended by all API classes for communicating with the hockeyapp API
"""
import re
import requests


class APIError(Exception):
    """Raised when the Hockeyapp API returns an error for a request"""

    def __repr__(self):
        """Return a representation of the exception
        :rtype: str
        """
        return '<%s [%s]>' % (self.__class__.__name__,
                              ', '.join(sorted(self.args[0].keys())))

    def __str__(self):
        """ Format exception data
        :returns: the string representation of the error
        """
        return ', '.join(sorted(['[%s]: %s' %
                                 (key, self.args[0][key])
                                 for key in self.args[0]]))


class APIRequest(object):
    """Base class for all API requests. Set Class.PATH to the part of the path
    specific to the request.
    """
    BASE_URL = 'https://rink.hockeyapp.net/api/2'
    TOKEN_PATTERN = re.compile('[a-f0-9]{32}')

    def __init__(self, token, log=None):
        """Construct the APIRequestObject
        :param str token: The API token for the request
        """
        if not self.TOKEN_PATTERN.match(token):
            raise ValueError('The API token should be a 32 char hex digest')

        self.headers = {
            'Accept': 'application/json; text/plain;',
            'X-HockeyAppToken': token
        }

        # Abstract our call to logger her to hide what might not be passed in
        def _log(msg, *args):
            if log is not None:
                log(msg, *args)

        self.log = _log

    def get(self, path, data=None):
        """GET data from the API
        :param str path: The path for the API call
        :param dict data: Optional query parameters for the GET
        :rtype: list or dict
        """
        uri = self._build_uri(path)
        self.log('Performing HTTP GET to %s', uri)
        return self._response(requests.get(uri, headers=self.headers, data=data))

    def post(self, path, data=None, files=None):
        """POST data to the API
        :param str path: The path for the API call
        :param dict data: Optional query parameters for the POST
        :param dict files: A dictionary of field name and open file handles
        :rtype: list or dict
        """
        uri = self._build_uri(path)
        self.log('Performing HTTP POST to %s', uri)
        return self._response(requests.post(uri, headers=self.headers, data=data, files=files))

    def put(self, path, data=None, files=None):
        """PUT data to the API
        :param str path: The path for the API call
        :param dict data: Optional query parameters for the POST
        :param dict files: A dictionary of field name and open file handles
        :rtype: list or dict
        """
        uri = self._build_uri(path)
        self.log('Performing HTTP PUT to %s', uri)
        return self._response(requests.put(uri, headers=self.headers, data=data, files=files))

    def delete(self, path, data=None):
        """DELETE data from the API
        :param str path: The path for the API call
        :param dict data: Optional query parameters for the DELETE
        :rtype: list or dict
        """
        uri = self._build_uri(path)
        self.log('Performing HTTP DELETE to %s', uri)
        return self._response(requests.delete(uri, headers=self.headers, data=data))

    def _build_uri(self, path):
        """Return the URI for the request
        :rtype: str
        """
        if path is None:
            raise ValueError('The Path for the API call can not by null')

        return '{}{}'.format(self.BASE_URL, path)

    def _response(self, response):
        """Process the API response
        :param requests.Response response: The request response
        :rtype: list
        :raise: hockeyapp.app.APIError
        """
        self.log('Response status code: %s', response.status_code)
        self.log('Headers: %r', response.headers)

        if 200 <= response.status_code <= 300:
            json = None
            if 'application/json' in response.headers['Content-Type']:
                json = response.json()

            if json is not None:
                return json
            elif len(response.content) == 1:
                return {'success': True}
            else:
                return response.content

        if response.status_code == 404:
            raise APIError({'404': 'URL Not Found: %s' % response.url})

        if 'application/json' in response.headers['Content-Type']:
            raise APIError(response.json().get('errors'))

        self.log(response.content)
        raise APIError('Not JSON')
