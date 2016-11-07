.. _advanced:

.. automodule:: smokeapi

Advanced Usage
==============

This portion of the documentation covers some of the more advanced features of
SmokeAPI.

.. _query-ids:

Calling ``fetch`` for specific IDs
----------------------------------

Some of the end points accept IDs. The documentation says these are semicolon
delimited lists of values. SmokeAPI, however, can handle this for you. You
just need to pass a ``list`` to the ``ids`` keyword argument::

    >>> from smokeapi import SmokeAPI
    >>> SMOKE = SmokeAPI('your_api_key')
    >>> post_ids = [44800, 44799, 800000]
    >>> posts = SMOKE.fetch('posts', ids=post_ids)
    >>> posts
    {'has_more': False,
     'items': [{u'body': u'<p>You schould remove your redirection.\nAnd put a CName on mydomain.co with value mydomain.herokuapp.com.</p>\n',
                u'created_at': u'2016-10-26T12:51:51.000Z',
                u'downvote_count': None,
                u'id': 44800,
                u'is_fp': True,
                u'is_naa': False,
                u'is_tp': False,
                u'link': u'//stackoverflow.com/a/40262819',
                u'post_creation_date': None,
                u'score': None,
                u'site_id': 1,
                u'stack_exchange_user_id': 37856,
                u'title': u'Heroku - custom domain DNS',
                u'updated_at': u'2016-10-26T12:52:13.000Z',
                u'upvote_count': None,
                u'user_link': u'//stackoverflow.com/u/4720079',
                u'user_reputation': 1,
                u'username': u'Lars Skogshus',
                u'why': u'Body - Position 1-111: <p>You schould remove your redirection.\nAnd put a CName on mydomain.co with value mydomain.herokuapp.com.</p>'},
               {u'body': u"<p>BUT IF YOU WANT TO CROSS ITALIN BORDER WITH CARTA D'IDENTITA FROM NON SCHENGEN AREA IS IT POSSIBLE ?</p>\n",
                u'created_at': u'2016-10-26T12:50:11.000Z',
                u'downvote_count': None,
                u'id': 44799,
                u'is_fp': False,
                u'is_naa': True,
                u'is_tp': False,
                u'link': u'//travel.stackexchange.com/a/81481',
                u'post_creation_date': None,
                u'score': None,
                u'site_id': 108,
                u'stack_exchange_user_id': 37855,
                u'title': u"Travel in the Schengen area with only carta d'identita italiana and permesso di soggiorno",
                u'updated_at': u'2016-10-26T12:51:23.000Z',
                u'upvote_count': None,
                u'user_link': u'//travel.stackexchange.com/u/52978',
                u'user_reputation': 1,
                u'username': u'IRINA',
                u'why': u'Post - All in caps'}],
     'page': 1,
     'total': 2}

Notice that we searched for 3 posts and only 2 results were returned. This is
how the API operates. If an ID doesn't exist, a result will not be returned or
indicated that it has been missed. It may be important for you to compare
results to what you searched for to see if any values are missing.

Another thing to notice here is that only ``posts`` was passed as the end
point. This works because the official end point is ``posts/{ids}``. If you
leave the ``{ids}`` off and it is the last part of the end point, SmokeAPI will
automatically add it for you. An identical call would look like this, with
``{ids}`` included in the end point declaration.

    >>> posts = SMOKE.fetch('posts/{ids}', ids=post_ids)

If ``{ids}`` is not at the end of the end point, then leaving it out of the
target end point is **not** optional. This will **not work**::

    >>> posts = SMOKE.fetch('reason/posts', ids=reason_ids)

However, this will work and will return posts associated with the selected
close reasons::

    >>> posts = SMOKE.fetch('reason/{ids}/posts', ids=reason_ids)

.. _proxy-usage:

Proxy Usage
-----------

Some users sit behind a proxy and need to get through that before accessing
the internet at large. SmokeAPI can handle this workflow.

A failure due to a proxy may look like this::

    >>> from smokeapi import SmokeAPI, SmokeAPIError
    >>> try:
    ...     SMOKE = SmokeAPI('your_api_key')
    ... except SmokeAPIError as e:
    ...     print(e.message)
    ...
    ('Connection aborted.', error(10060, 'A connection attempt failed
    because the connected party did not properly respond after a period of
    time, or established connection failed because connected host has failed
    to respond'))

This can be fixed, by passing a dictionary of http and https proxy addresses
when creating the :class:`SmokeAPI <smokeapi.SmokeAPI>` class::

    >>> from smokeapi import SmokeAPI, SmokeAPIError
    >>> proxies = {'http': 'http://proxy.example.com', 'https': 'http://proxy.example.com'}
    >>> try:
    ...     SMOKE = SmokeAPI('your_api_key', proxy=proxies)
    ... except SmokeAPIError as e:
    ...     print(e.message)
    ...

The two important lines are where ``proxies`` is defined and the
modified :class:`SmokeAPI <smokeapi.SmokeAPI>` initialization, which passes the
``proxies`` dictionary to the ``proxy`` argument.


.. _more-parameters-fetch:

Calling ``fetch`` with various API parameters
---------------------------------------------

Some end points take multiple arguments to help filter the number of results you return. SmokeAPI
will accept all of these as parameters.

As an example, lets look at the `search <https://github.com/Charcoal-SE/metasmoke/wiki/Search-Posts>`__
end point. This end point will accept the following parameters:

- feedback_type
- from_date
- to_date
- site

``page`` and ``per_page`` are handled by SmokeAPI through usage of the
``max_pages`` and ``per_page`` values of the :class:`SmokeAPI <smokeapi.SmokeAPI>`
class. The others, are part of the ``kwargs`` accepted by
:meth:`fetch <smokeapi.SmokeAPI.fetch>`.

Let's create an example using all of these. This should return a list of posts
created between October 28, 2016 and October 29, 2016 that have a feedback type of
``naa-`` and were on Stack Overflow.

