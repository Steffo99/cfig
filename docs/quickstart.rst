##########
Quickstart
##########

.. note::

    This page assumes you have already :ref:`installed <Installation>` :mod:`cfig`.

This page describes how to use :mod:`cfig` in an application.


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

* the **name** of the function is used as key of the configurable value;
* the ``@config.required()`` **decorator** marks the value as required, preventing your application from launching if it is not set;
* the **function parameters** consist of a single :class:`str` parameter named ``val``, which is the string read from the environment variable having the same name of the function;
* the **docstring** defines the meaning of the configuration value in natural language;
* the **contents of the function** are used to process the input string into more refined Python objects;
* the **return annotation** of the function is used to let IDEs know what type this configuration value will be.


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


Processing and validation
-------------------------

The function defining a new configurable variable is also called a resolver: it will be executed only once, when its value is first requested, then the result is cached in a special object called proxy.

This allows us to perform some expensive operations inside, such as connecting to a database, or performing API requests to validate tokens and passwords.

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
        except (ValueError, TypeError):
            raise cfig.InvalidValueError("Not an int.")

We can see that the new ``MAX_USERS`` configurable value processes the input string by trying to cast it into an :class:`int`, and raises a :exc:`~cfig.errors.InvalidValueError` containing the error message to display to the user if the cast fails.

Ideally, errors happening in resolvers should be caught by the programmer and re-raised as :exc:`~cfig.errors.InvalidValueError`, so that users can distinguish them from bugs.


Adding CLI support
==================

.. note::

    This requires the CLI extra to be installed. See :ref:`Installation` for more details.

To facilitate configuration on the users' part, :mod:`cfig` provides an integrated command line interface previewing the values of variables, triggered by a call to :meth:`~cfig.config.Configuration.cli`:


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
        except (ValueError, TypeError):
            raise cfig.InvalidValueError("Not an int.")

    if __name__ == "__main__":
        config.cli()

By adding the :meth:`~cfig.config.Configuration.cli` call to a :mod:`__main__` clause, we allow users to access the CLI by manually running this module, but we prevent the CLI from starting when this module is accessed from another location.

Given our current configuration, something similar to this will be displayed:

.. code-block:: console

    $ python -m myproject.mydefinitionmodule
    ===== Configuration =====

    SECRET_PASSWORD → Required, but not set.
    The secret password required to use this application!

    SECRET_USERNAME = 'root'
    The username to require users to login as. If unset, defaults to `root`.

    MAX_USERS       → Required, but not set.
    The maximum number of users that will be able to login to this application.

    ===== End =====


Use the configuration
=====================

Finally, it is time to use in our application the configurable variables we defined!

In the modules of your application, you can import and use the variables directly from the definition module:

.. code-block:: python
    :emphasize-lines: 1,4,7,11,12

    from .mydefinitionmodule import SECRET_PASSWORD, SECRET_USERNAME, MAX_USERS

    if __name__ == "__main__":
        if username := input("Username: ") != SECRET_USERNAME:
            print("error: invalid username")
            sys.exit(1)
        if password := input("Password: ") != SECRET_PASSWORD:
            print("error: invalid password")
            sys.exit(2)

        print("Welcome, " + SECRET_USERNAME + "!")
        print(f"The current user limit is: {MAX_USERS}")

.. warning::

    Since the values imported from the definition module are proxies to the real value, ``is`` comparisions won't work with them, but you can do ``==`` comparsions with them:

    .. code-block:: python
        :emphasize-lines: 6,7

        @config.optional()
        def ALWAYS_NONE(val: t.Optional[str]) -> None:
            """This configuration value will always be None."""
            return None

        assert ALWAYS_NONE is not None
        assert ALWAYS_NONE == None


Validate all variables at once
==============================

For a better user experience, you might want to ensure that all variables are correctly configured when your application is started.

For that goal, :mod:`cfig` provides the :meth:`~cfig.config.Configuration.ProxyDict.resolve` method, which immediately tries to resolve and cache all configurable values defined in the :class:`~cfig.config.Configuration`:

.. code-block:: python
    :emphasize-lines: 1,4

    from .mydefinitionmodule import config

    if __name__ == "__main__":
        config.proxies.resolve()

The method will gather all errors occurring during the resolution, and will raise all of them at once with a :exc:`~cfig.errors.BatchResolutionFailure`, which you may want to handle in a custom way:

.. code-block:: python
    :emphasize-lines: 4,5,6,7

    from .mydefinitionmodule import config

    if __name__ == "__main__":
        try:
            config.proxies.resolve()
        except cfig.BatchResolutionFailure as failure:
            ...

And that's it! You're using :mod:`cfig` in the best way possible :)

See :doc:`advanced` for more features that may be useful in specific cases.