SmokeAPI: A Python wrapper for the MetaSmoke API
=====================================================

Release v\ |version|. (:ref:`Installation <install>`)

SmokeAPI is a simple Python wrapper for the `MetaSmoke API
<https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__ .

Retrieving data from the API is simple:

::

    from smokeapi import SmokeAPI
    SMOKE = SmokeAPI('your_api_key')
    posts = SMOKE.fetch('posts/feedback', type="naa-")

The above, will issue a call to the
|PostsFeedback|_. end point on MetaSmoke.

.. |PostsFeedback| replace:: ``Posts Feedback``
.. _PostsFeedback: https://github.com/Charcoal-SE/metasmoke/wiki/Posts-by-Feedback

Supported Features
------------------

-  Read and write functionality via the API.
-  Retrieve multiple pages of results with a single call and merge
   all the results into a single response.
-  Throw exceptions returned by the API for easier troubleshooting.
-  Utilize `Requests <http://docs.python-requests.org/>`__.

SmokeAPI is supported on Python 2.7 - 3.5.

User Guide
----------

This portion of documentation provides details on how to utilize the
library, and provides advanced examples of various use cases.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/quickstart
   user/advanced
   user/complex

The API Documentation
---------------------

Information about specific functions, classes, and methods are available
in this portion of documentation.

.. toctree::
   :maxdepth: 2

   api

Contributor Guidelines
----------------------

Information about how to contribute to the project is available in this
portion of the documentation.

.. toctree::
   :maxdepth: 2

   dev/contributing
   dev/todo
   dev/authors



