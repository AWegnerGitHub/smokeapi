import requests
from itertools import chain


class SmokeAPIError(Exception):
    """
    The Exception that is thrown when ever there is an API error.

    :param url: (string) The URL that was called and generated an error
    :param code: (int) The `error_code` returned by the API
    :param name: (string) The `error_name` returned by the API and is human friendly
    :param message: (string) The `error_message` returned by the API
    """

    def __init__(self, url, code, name, message):
        self.url = url
        self.error_name = name
        self.error_code = code
        self.error_message = message


class SmokeAPI(object):
    def __init__(self, key=None, **kwargs):
        """
            The object used to interact with the MetaSmoke API

            :param key: (string) **(Required)** A valid API key. An API key can be received by following the
                current instructions in the `API Documentation <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__.
            :param token: (string) **(Required for write access/Optional is no write routes are called)**
                This is a valid write token retreived by following instructions in the `API Documentation <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__.
                If this is not set, calls to `send_data` will fail.
            :param proxy: (dict) (optional) A dictionary of http and https proxy locations
                Example:

                .. code-block:: python

                    {'http': 'http://example.com',
                     'https': 'https://example.com'}

                By default, this is ``None``.
            :param max_pages: (int) (optional) The maximum number of pages to retrieve (Default: ``5``)
            :param per_page: (int) (optional) The number of elements per page. The API limits this to
                a maximum of 100 items on all end points (Default: ``100``)

            :param access_token: (string) (optional) An access token associated with an application and
                a user, to grant more permissions (such as write access)
            """
        if not key:
            raise ValueError('No API Key provided. This is required for all MetaSmoke API routes.')

        self.proxy = kwargs.get('proxy', None)
        self.max_pages = kwargs.get('max_pages', 5)
        self.per_page = kwargs.get('per_page', 100)
        self._api_key = key
        self.token = kwargs.get('token', None)
        self._endpoint = None
        self._previous_call = None
        self._base_url = 'https://metasmoke.erwaysoftware.com/api/'

    def __repr__(self):
        return "<SmokeAPI> endpoint: {}  Last URL: {}".format(self._endpoint, self._previous_call)

    def fetch(self, endpoint=None, page=1, **kwargs):
        """Returns the results of an API call.

            This is the main work horse of the class. It builds the API query
            string and sends the request to MetaSmoke. If there are multiple
            pages of results, and we've configured `max_pages` to be greater than
            1, it will automatically paginate through the results and return a
            single object.

            Returned data will appear in the `items` key of the resulting
            dictionary.

            :param endpoint: (string) The API end point being called. Available endpoints are listed on
                the official `API Documentation <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__.

                This can be as simple as ``fetch('posts/feedback')``, to call feedback end point

                If calling an end point that takes additional parameter, such as `id`s
                pass the ids as a list to the `ids` key:

                    .. code-block:: python

                        fetch('posts/{ids}', ids=[1,2,3])

                This will attempt to retrieve the posts for the three listed ids.

                If no end point is passed, a ``ValueError`` will be raised
            :param page: (int) The page in the results to start at. By default, it will start on
                the first page and automatically paginate until the result set
                reaches ``max_pages``.
            :param kwargs: Parameters accepted by individual endpoints. These parameters
                **must** be named the same as described in the endpoint documentation
            :rtype: (dictionary) A dictionary containing wrapper data regarding the API call
                and the results of the call in the `items` key. If multiple
                pages were received, all of the results will appear in the
                ``items`` tag.
            """

        if not endpoint:
            raise ValueError('No endpoint provided.')

        self._endpoint = endpoint

        params = {"per_page": self.per_page,
                  "page": page,
                  "key": self._api_key
                  }

        # This block will replace {ids} placeholds in end points
        # converting .fetch('posts/{ids}', ids=[222, 1306, 99999]) to
        #   posts/222;1306;99999
        for k, value in kwargs.items():
            if "{" + k + "}" in endpoint:
                endpoint = endpoint.replace("{" + k + "}", ';'.join(str(x) for x in value))
                kwargs.pop(k, None)

        # This block will see if there there are ids remaining
        # This would occur if the developer passed `posts` instead of `posts/{ids}` to `fetch`
        # If this is the case, then convert to a string and assume this goes at the end of the endpoint

        if 'ids' in kwargs:
            ids = ';'.join(str(x) for x in kwargs['ids'])
            kwargs.pop('ids', None)
            endpoint += "/{}".format(ids)

        params.update(kwargs)

        data = []
        run_cnt = 1
        while run_cnt <= self.max_pages:
            run_cnt += 1

            base_url = "{}{}/".format(self._base_url, endpoint)

            try:
                response = requests.get(base_url, params=params, proxies=self.proxy)
            except requests.exceptions.ConnectionError as e:
                raise SmokeAPIError(self._previous_call, str(e), str(e), str(e))

            self._previous_call = response.url

            try:
                response.encoding = 'utf-8-sig'
                response = response.json()
            except ValueError as e:
                raise SmokeAPIError(self._previous_call, str(e), str(e), str(e))

            try:
                code = response["error_code"]
                name = response["error_name"]
                message = response["error_message"]
                raise SmokeAPIError(self._previous_call, code, name, message)
            except KeyError:
                pass  # This means there is no error

            data.append(response)

            if len(data) < 1:
                break

            if 'has_more' in response and response['has_more']:
                params["page"] += 1
            else:
                break

        r = []
        for d in data:
            r.extend(d['items'])
        items = list(chain(r))
        result = {'has_more': data[-1]['has_more'],
                  'page': params['page'],
                  'total': len(items),
                  'items': items}

        return result

    def send_data(self, endpoint=None,  **kwargs):
        """Sends data to the API.

        This call is similar to ``fetch``, but **sends** data to the API instead
        of retrieving it.

        Returned data will appear in the ``items`` key of the resulting
        dictionary.

        Sending data **requires** that the ``token`` is set.

        :param endpoint: (string) **(Required)** The API end point being called. Available endpoints are listed on
            the official `API Documentation <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__.

            If no end point is passed, a ``ValueError`` will be raised
        :param kwargs: Parameters accepted by individual endpoints. These parameters
            **must** be named the same as described in the endpoint documentation
        :rtype: (dictionary) A dictionary containing wrapper data regarding the API call
            and the results of the call in the `items` key. If multiple
            pages were received, all of the results will appear in the
            ``items`` tag.
        """
        if not endpoint:
            raise ValueError('No end point provided.')

        if not self.token:
            raise ValueError('A write token has not been set. This is required for all MetaSmoke API routes. This can\n'
                             'be set by setting the "token" parameter of your SmokeAPI object.')

        self._endpoint = endpoint

        params = {
            "key": self._api_key,
            "token": self.token
        }

        if 'ids' in kwargs:
            ids = ';'.join(str(x) for x in kwargs['ids'])
            kwargs.pop('ids', None)
        else:
            ids = None

        params.update(kwargs)

        data = []

        base_url = "{}{}/".format(self._base_url, endpoint)
        response = requests.post(base_url, data=params, proxies=self.proxy)
        self._previous_call = response.url
        response = response.json()

        try:
            code = response["error_code"]
            name = response["error_name"]
            message = response["error_message"]
            raise SmokeAPIError(self._previous_call, code, name, message)
        except KeyError:
            pass  # This means there is no error

        data.append(response)
        r = []
        for d in data:
            r.extend(d['items'])
        items = list(chain(r))
        result = {'has_more': data[-1]['has_more'],
                  'page': params['page'],
                  'total': len(items),
                  'items': items}

        return result