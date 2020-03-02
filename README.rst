Spiking a refactoring of
`uw-dnmr <https://github.com/sametz/uw_dnmr>`_
as a PySides2 Qt app.

This also tests using a 'src' project structure,
and using `Briefcase`_ (part of `The BeeWare Project`_ suite of tools)
to build an app.

This prototype was successfully turned into an installable app for Mac OSX
(see Releases).
Note that app and installer currently borrow BeeWare's mascot, Brutus the Bee,
from the BeeWare tutorial.

Once this prototype is satisfactory,
it will be incorporated into the **uw-dnmr** project.
If you want to run the app from source or work with the code,
here is a brief description on how to get it up and running as a developer.

Setting up the development environment
======================================

Create a virtual environment (should work for python 3.6+):

.. code-block:: bash

   python -m venv venv

Activate the virtual environment:

.. code-block:: bash

   source venv/bin/activate (Mac)
   venv\Scripts\activate.bat (Windows)

Install in developer mode:

.. code-block:: bash

   pip install -e ".[dev]"

Run the tests:

.. code-block:: bash

   pytest

Run the application:

.. code-block:: bash

   python -m qt_nmr

.. _`Briefcase`: https://github.com/beeware/briefcase
.. _`The BeeWare Project`: https://beeware.org/