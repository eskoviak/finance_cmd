=======
finance
=======

This is the main application package, containing the Applicaiton Factory ``create_app()`` function of Flask.  This is also the 
function used as the object for the WSGI app needed in ``wsgi.py``.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Models
======

The models mudule contains base classes need to use the SQLAlchemy ORM to encapsulate the PostgreSQL data base used in the backend.

The following modules are defined:

entities

.. autoclass:: MyFinance.models.entities.ExternalAccounts

Finance module
==============

.. autofunction:: MyFinance.finance.create_app

Liablility module
=================

.. autofunction:: MyFinance.liability.enter_liability

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`