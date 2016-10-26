.. _quickstart:

.. automodule:: smokeapi

Quickstart
==========

Ready to start talking to the Meta Smoke API? This page gives an
introduction on how to get started with SmokeAPI.

First, you need to:

* :ref:`Install <install>` SmokeAPI

.. _basic-retrieval:

Basic Data Retrieval
--------------------

Retrieving data is very simple. First, though, you will need an
`API Key <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation#getting-started>`__.
This key will be used every place you see the variable ``your_api_key``.

**Note:** This is an API *key*. It is a unique identifier for your application. It's not a disaster if you end up sharing it with other people unintentionally, but generally try to keep it protected. When you start making use of write capabilities, you'll be issued with API *tokens* that provide authorization on an app-user-pair basis; these tokens are sensitive information and should be protected no matter what.

First, import the SmokeAPI module::

    >>> from smokeapi import SmokeAPI

Now we want to retrieve a list of posts that have been marked as "Not an Answer" by users::

    >>> SMOKE = SmokeAPI('your_api_key')
    >>> posts = SMOKE.fetch('posts/feedback', type="naa-")

This will return the 500 most recent posts that have been classified as "Not an Answer". The value passed to
:meth:`fetch <smokeapi.SmokeAPI.fetch>` is an end point defined in the
`MetaSmoke API Documentation <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation/>`__.

If you are looking for more information on how to tailor the results of your
queries. Take a look at the :ref:`Advanced Usage <advanced>` examples.

.. _change-num-results:

Change number of results
------------------------

By default, SmokeAPI will return up to 500 items in a single call. It may be
less than this, if there are less than 500 items to return.

The number of results can be modified by changing the ``per_page``
and ``max_pages`` values. These are multiplied together to get the maximum
total number of results. The API paginates the results and SmokeAPI recombines
those pages into a single result.

The number of API calls that are made is dependant on the ``max_pages`` value.
This will be the maximum number of calls that is made for this particular
request.

All of these changes to ``per_page`` and ``max_pages`` need to occur before
calls to ``fetch`` or ``send_data``.

Let's walk through a few examples::

    >>> SMOKE.per_page = 10
    >>> SMOKE.max_pages = 10

This will return up to 100 results. However, it will hit the API up to 10 times.

    >>> SITE.SMOKE = 100
    >>> SITE.max_pages = 1

This will result up to 100 results as well, but it will only hit the API
one time.

MetaSmoke limits the number of results per page to 100. If you want more
than 100 results, you need to increase the ``max_pages``.

    >>> SITE.per_page = 100
    >>> SITE.max_pages = 2

This will return up to 200 results and hit the API up to twice.

.. _get-exact-num-results:

Getting exact number of results
-------------------------------

If you want a specific number of results, but no more than that, you need to
perform some manipulations of these two values.

    >>> SITE.per_page = 50
    >>> SITE.max_pages = 3

This will return up to 150 results. It will also hit the API 3 times to get
these results. You can save an API hit by changing the values to::

    >>> SITE.per_page = 75
    >>> SITE.max_pages = 2

This will also return up to 150 results, but do so in only 2 API hits.

**Note:** Each "page" in an API call can have up to 100 results. In the first
scenario, above, we are "wasting" 150 results because we only allow each page
50 results. In the second scenario, we are wasting 50 results. If you do not
need an exact number of results, it is more efficient - number of API calls-wise - to set
the ``per_page`` to 100 and return the highest number of results per page that
the system allows.

.. _quick-errors:

Errors
------

SmokeAPI will throw an error if the MetaSmoke API returns an error. This
can be caught in an exception block by catching :class:`smokeapi.SmokeAPIError`.
The exception has several values available to help troubleshoot the underlying
issue::

    except smokeapi.SmokeAPIError as e:
        print("   Error URL: %s" % (e.url))
        print("   Error Code: %s" % (e.error_code))
        print("   Error Name: %s" % (e.error_name))
        print("   Error Message: %s" % (e.error_message))

This will print out the URL that was being accessed, the error code that the
API returns, the error name the API returns and the error message the API
returns. Using these values, it should be possible to determine the cause of
the error.

