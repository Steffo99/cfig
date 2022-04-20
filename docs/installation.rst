############
Installation
############

You can install :mod:`cfig` in multiple ways!

.. note::

    Never install packages outside :mod:`venv`, unless you know very well what you're doing!


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
