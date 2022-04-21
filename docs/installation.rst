############
Installation
############

You can install :mod:`cfig` in multiple ways!

.. note::

    The CLI tools are not included by default in the package, but are distributed as an `extra <https://stackoverflow.com/questions/52474931/what-is-extra-in-pypi-dependency>`_.

    This page refers to the installation with the ``[cli]`` extra, but you may omit to install it if you do not intend to provide the CLI to users.

.. warning::

    Never install packages outside :mod:`venv`\ s, unless you know very well what you're doing!


From PyPI
=========

:mod:`cfig` is distributed through the `Python Package Index`_, and you can install it with your favourite dependency manager!

.. _Python Package Index: https://pypi.org/


Using pip
---------

You can install :mod:`cfig` through :mod:`pip`:

.. code-block:: console

    $ pip install cfig[cli]

.. note::

    If you're working on a project, remember to add it to your ``requirements.txt`` file!


Using Poetry
------------

You can install :mod:`cfig` through :mod:`poetry`:

.. code-block:: console

    $ poetry add cfig[cli]


From source
===========

If you have the source of :mod:`cfig`, you can install it from its own folder!


Using PEP 518
-------------

Introduced with :pep:`518`, :mod:`pip` supports automatic build and installation:

.. code-block:: console

    $ cd cfig
    $ pip install .[cli]


For development
===============

If you want to contribute to :mod:`cfig`, you can use :mod:`poetry` to install the project in "development" mode in an isolated environment:

.. code-block:: console

    $ cd cfig
    $ poetry install -E cli

.. hint::

    Setting ``virtualenvs.in-project`` to :data:`True` is recommended!

    .. code-block:: console

        $ poetry config virtualenvs.in-project true
