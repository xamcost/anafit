Anafit
=================================

Anafit is a package providing fitting tools for matplotlib figures. It is largely inspired from the Ezyfit toolbox for Matlab.

Source code repository and issue tracker:
   git@gitlab.com:xamcosta/Anafit.git

Python Package Index:
   to be filled

Requirements
------------

Python:
   Anafit has been coded using Python 3.5 from Anaconda_ distribution.

pip/setuptools:
   Those are the most convenient way to install Anafit and its dependencies. 
   Most likely they are already installed in your system, but if not, please 
   refer to `pip`_ doc webpage.

Matplotlib and PyQt5:
   When called, Anafit will appear as a new button in the `matplotlib`_ figure 
   toolbar. However, this requires `PyQt5`_ as matplotlib’s backend. If it is not
   the backend you’re using, change it using, in the Python console:
   .. code:: python
   
      matplotlib.use(‘Qt5Agg’)

Other packages:
   To fit, Anafit uses scipy.optimize.curve_fit function from `scipy`_ module.
   It also uses `numpy`_ , os , sys , functools and finally json (for 
   custom fit function saving in a text file).

.. _Anaconda: http://docs.continuum.io/anaconda/
.. _PyPy: http://pypy.org/
.. _pip: https://pip.pypa.io/en/stable/installing/
.. _matplotlib: https://matplotlib.org/
.. _PyQt5: https://pypi.python.org/pypi/PyQt5/5.9.2
.. _scipy: https://www.scipy.org/
.. _NumPy: http://www.numpy.org/

Installation
------------

Once you have installed the above-mentioned dependencies, you can use pip
to download and install the latest release with a single command::

   python3 -m pip install anafit

To un-install, use::

   python3 -m pip uninstall anafit

Note that you can also just download and add the anafit repository to your PYTHONPATH.

Usage
-----

First, import anafit and matplotlib, and set the backend to Qt5:

.. code:: python

   import anafit
   import matplotlib.pyplot as plt
   matplotlib.use(‘Qt5Agg’)

Adding anafit button to a matplotlib figure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is done simply by calling anafit.Figure() class:

.. code:: python

   fig = plt.figure() 
   ana = anafit.Figure(fig)

If no argument is passed to anafit.Figure(), the anafit button will be added to the
current active figure.

Selecting data to fit
^^^^^^^^^^^^^^^^^^^^^





