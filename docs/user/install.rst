.. _install:

Installation
============

This part of the documentation provides an overview of how to install SmokeAPI.

Pip Install
-----------

SmokeAPI can be installed by simply running this command in your terminal::

    $ pip install smokeapi

If you don't have `pip <https://pip.pypa.io>`_ installed, this Python
`installation guide <http://docs.python-guide.org/en/latest/starting/installation/>`_
can guide you through the process.

Source Code
-----------

SmokeAPI is developed on GitHub where the code is
`always available <https://github.com/AWegnerGitHub/smokeapi>`_.

You can close the repository::

    $ git clone git://github.com/AWegnerGitHub/smokeapi.git

Or download the `tarball <https://github.com/AWegnerGitHub/smokeapi/tarball/master>`_::

    $ curl -OL https://github.com/AWegnerGitHub/smokeapi/tarball/master
      # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python
package or install it into your site-packages easily::

    $ python setup.py install