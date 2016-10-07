This is a Python wrapper for the `MetaSmoke API <https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation>`__.

.. image:: https://travis-ci.org/AWegnerGitHub/smokeapi.svg?branch=master
  :target: https://travis-ci.org/AWegnerGitHub/smokeapi
  :alt: Build Status

.. image:: https://readthedocs.org/projects/smokeapi/badge/?version=latest
  :target: http://smokeapi.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

This library has support for:

-  Read and (soon) write functionality via the API.
-  Can retrieve multiple pages of results with a single call and merges
   all the results into a single response.
-  Throws exceptions returned by the API for easier troubleshooting.
-  Utilizes `Requests <http://docs.python-requests.org/>`__.


Example usage:
==============

Establish a connection to MetaSmoke and retreive some posts that have been marked "Not an answer"
-------------------------------------------------------------------------------------------------

::

    from smokeapi import SmokeAPI
    SITE = SmokeAPI('stackoverflow')
    comments = SITE.fetch('comments')

The above, will issue a call to the
|comments|_. end point on Stack Overflow.

.. |comments| replace:: ``comments``
.. _comments: http://api.stackexchange.com/docs/comments

Much more detailed documentation is available on
`ReadTheDocs <http://smokeapi.readthedocs.io/>`__.