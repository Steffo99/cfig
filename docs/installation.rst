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

    $ pip install cfig
    Collecting cfig
      Downloading cfig-0.2.1-py3-none-any.whl (12 kB)
    Collecting lazy-object-proxy<2.0.0,>=1.7.1
      Downloading lazy_object_proxy-1.7.1-cp310-cp310-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (62 kB)
         ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.3/62.3 KB 2.3 MB/s eta 0:00:00
    Installing collected packages: lazy-object-proxy, cfig
    Successfully installed cfig-0.2.1 lazy-object-proxy-1.7.1

.. note::

    If you're working on a project, remember to add it to your ``requirements.txt`` file!


Using Poetry
------------

You can install :mod:`cfig` through :mod:`poetry`:

.. code-block:: console

    $ poetry add cfig
    Using version ^0.2.1 for cfig

    Updating dependencies
    Resolving dependencies... (0.3s)

    Writing lock file

    Package operations: 2 installs, 0 updates, 0 removals

      • Installing lazy-object-proxy (1.7.1)
      • Installing cfig (0.2.1)


From source
===========

If you have the source of :mod:`cfig`, you can install it from its own folder!


Using PEP 518
-------------

Introduced with :pep:`518`, :mod:`pip` supports automatic build and installation:

.. code-block:: console

    $ cd cfig
    $ pip install .


For development
===============

If you want to contribute to :mod:`cfig`, you can use :mod:`poetry` to install the project in "development" mode in an isolated environment:

.. code-block:: console

    $ cd cfig
    $ poetry install

.. hint::

    Setting ``virtualenvs.in-project`` to :data:`True` is recommended!

    .. code-block:: console

        $ poetry config virtualenvs.in-project true
