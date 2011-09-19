============
Installation
============

Dependencies
============
These are the versions that I tested the code with, but the code will most
likely work with older versions.

Required
--------
- `Python 2.7.1 <http://www.python.org/>`_
- `Scipy 0.9.0 <http://www.scipy.org/>`_
- `Numpy 1.5.1 <http://numpy.scipy.org/>`_
- `PyTables <http://www.pytables.org>`_
- `Matplotlib 0.99.3 <http://matplotlib.sourceforge.net/>`_

Optional
--------
These are required to bulid the documentation:

- `Sphinx <http://sphinx.pocoo.org/>`_
- `Numpydoc <http://pypi.python.org/pypi/numpydoc>`_

Installation
============

There are currently two options for getting the source code:

1. Clone the source code with Git: ``git clone
   git://github.com/moorepants/BicycleParameters.git``
2. `Download the source from Github`__.

.. __: https://github.com/moorepants/BicycleParameters

Once you have the source code navigate to the directory and run::

  >>> python setup.py install

This will install the software into your system and you should be able to
import it with::

  >>> import DataProcessor
