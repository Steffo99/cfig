##############
Advanced usage
##############

This page describes some more advanced :mod:`cfig` features that you might be interested in using.


Fail-fast
=========

If your variables are very slow to be resolved, you may want for the :meth:`~cfig.config.Configuration.ProxyDict.resolve` method to raise as soon as a single value fails to resolve.

For that purpose, the :meth:`~cfig.config.Configuration.ProxyDict.resolve_failfast` method is provided:

.. code-block:: python
    :emphasize-lines: 4

    from .mydefinitionmodule import config

    if __name__ == "__main__":
        config.proxies.resolve_failfast()

Please note that the :meth:`~cfig.config.Configuration.ProxyDict.resolve_failfast` method does not raise :exc:`~cfig.errors.BatchResolutionFailure`, but raises the first occurring error instead, so you might want to catch it in this way:

.. code-block:: python
    :emphasize-lines: 4,5,6,7

    from .mydefinitionmodule import config

    if __name__ == "__main__":
        try:
            config.proxies.resolve_failfast()
        except cfig.ConfigurationError as err:
            ...


Reloading variables
===================

You might want for the configuration to be reloaded without restarting your application.

In that case, you may use the :meth:`~cfig.config.Configuration.ProxyDict.unresolve` method to clear the cached values, and then call :meth:`~cfig.config.Configuration.ProxyDict.resolve` again.

.. code-block:: python
    :emphasize-lines: 2,3

    ...
    config.proxies.unresolve()
    config.proxies.resolve()
    ...

To reload a single variable, you may use the ``del`` keyword:

.. code-block:: python
    :emphasize-lines: 2

    ...
    del MY_VARIABLE.__wrapped__
    ...


Sources selection
=================

If you need further fine-tuning of the places to gather configuration values from, you may specify them via the :attr:`cfig.config.Configuration.sources` collection:

.. code-block:: python
    :emphasize-lines: 2,3,5,6,7,8,9,10

    import cfig
    import cfig.sources.env
    import cfig.sources.envfile

    config = cfig.Configuration(sources=[
        cfig.source.env.EnvironmentSource(),
        cfig.source.env.EnvironmentSource(prefix="PROD_"),
        cfig.source.envfile.EnvironmentFileSource(),
        cfig.source.envfile.EnvironmentFileSource(suffix="_PATH"),
    ])

The specified sources are used in the order they are specified.

They may also be altered at runtime, if for some *crazy reason* you need that feature:

.. code-block:: python
    :emphasize-lines: 6,7,8

    import cfig
    import cfig.sources.env

    config = cfig.Configuration()

    config.sources.append(
        cfig.source.env.EnvironmentSource()
    )

.. note::

    Already cached variables **won't** be automatically reloaded after changing the sources!


Sources customization
---------------------

If the provided sources aren't enough, you may create a custom class inheriting from :class:`~cfig.sources.base.Source`.

.. hint::

    Since :mod:`cfig.sources` is a namespace package, if you intend to distribute your custom source, you may want to do it by extending the namespace, for an easier developer workflow.


