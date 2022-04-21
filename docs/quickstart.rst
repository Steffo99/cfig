##########
Quickstart
##########

This page describes how to use :mod:`cfig` in an application.

.. note::

    This page assumes you have already `installed <installation>` :mod:`cfig`.


Creating a configuration module
===============================

First, create a new ``.py`` file inside your package with the following contents:

.. code-block:: python
    :emphasize-lines: 1,2,4

    import cfig
    import typing as t

    config = cfig.Configuration()

This will:

#. Import :mod:`cfig` into your module
#. Import :mod:`typing` into your module and alias it as ``t`` for ease of use
#. Create a new :class:`~cfig.config.Configuration` with the default parameters, which will be able to be configured from `environment variables`_ and from environment files (files whose path is specified in an environment variable suffixed with ``_FILE``)

.. _environment variables: https://wiki.archlinux.org/title/Environment_variables


Creating configurable variables
===============================

Basics
------

To make use of :mod:`cfig`, you'll need to create one or more configurable variables in your module file:

.. code-block:: python
    :emphasize-lines: 6,7,8,9

    import cfig
    import typing as t

    config = cfig.Configuration()

    @config.required()
    def SECRET_PASSWORD(val: str) -> str:
        """The secret password required to use this application!"""
        return val

The newly added lines create a new configurable value named ``SECRET_PASSWORD``:

* the **name** of the function is used as :term:`key` of the configurable value;
* the ``@config.required()`` **decorator** marks the value as required, preventing your application from launching if it is not set;
* the **function parameters** consist of a single :class:`str` parameter named ``val``, which is the string read from the environment variable having the same name of the function;
* the **docstring** defines the meaning of the configuration value in natural language;
* the **contents of the function** are used to process the input string into more refined Python objects;
* the **return annotation** of the function is used to let IDEs know what type this configuration value will be.

.. todo::

    Maybe say that it is called a :term:`resolver`?


Optional
--------

Configuration values can be optional:

.. code-block:: python
    :emphasize-lines: 11,12,13,14,15,16

    import cfig
    import typing as t

    config = cfig.Configuration()

    @config.required()
    def SECRET_PASSWORD(val: str) -> str:
        """The secret password required to use this application!"""
        return val

    @config.optional()
    def SECRET_USERNAME(val: t.Optional[str]) -> str:
        """The username to require users to login as. If unset, defaults to `root`."""
        if val is None:
            return "root"
        return val

Optional values differ from required ones in their decorator and signature:

#. The decorator is ``@config.optional()`` instead of ``@config.required()``;
#. Since the passed ``val`` can be :data:`None`, it is given a signature of :data:`typing.Optional`.


Processing
----------

.. todo::

    A few words about value processing.

.. code-block:: python
    :emphasize-lines: 18,19,20,21,22,23,24

    import cfig
    import typing as t

    config = cfig.Configuration()

    @config.required()
    def SECRET_PASSWORD(val: str) -> str:
        """The secret password required to use this application!"""
        return val

    @config.optional()
    def SECRET_USERNAME(val: t.Optional[str]) -> str:
        """The username to require users to login as. If unset, defaults to `root`."""
        if val is None:
            return "root"
        return val

    @config.required()
    def MAX_USERS(val: str) -> int:
        """The maximum number of users that will be able to login to this application."""
        try:
            return int(val)
        except ValueError:
            raise cfig.InvalidValueError("Not an int.")

.. todo::

    A few words about slower resolvers.


Adding CLI support
==================

.. todo::

    What is the CLI and why is it useful?

.. code-block:: python
    :emphasize-lines: 26,27

    import cfig
    import typing as t

    config = cfig.Configuration()

    @config.required()
    def SECRET_PASSWORD(val: str) -> str:
        """The secret password required to use this application!"""
        return val

    @config.optional()
    def SECRET_USERNAME(val: t.Optional[str]) -> str:
        """The username to require users to login as. If unset, defaults to `root`."""
        if val is None:
            return "root"
        return val

    @config.required()
    def MAX_USERS(val: str) -> int:
        """The maximum number of users that will be able to login to this application."""
        try:
            return int(val)
        except ValueError:
            raise cfig.InvalidValueError("Not an int.")

    if __name__ == "__main__":
        config.cli()

.. todo::

    What will be displayed here?


Use the configuration
=====================

.. todo::

    How do I use the created values in my application?

.. todo::

    Why does ``is None`` not work?