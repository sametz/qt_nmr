Spiking a refactoring of
`uw-dnmr <hhttps://github.com/sametz/uw_dnmr>`_
as a PySides2 Qt app.

Setting up the development environment
======================================

Create a virtual environment (should work for python 3.6+):

.. code-block:: bash

   python -m venv venv

Activate the virtual environment:

.. code-block:: bash

   source env/bin/activate (Mac)
   env\Scripts\activate.bat (Windows)

Install in developer mode:

.. code-block:: bash

   pip install -e ".[dev]"

Run the tests:

.. code-block:: bash

   pytest
