Anafit
=================================

Anafit is a package providing fitting tools for matplotlib figures. It is largely inspired from the Ezyfit toolbox for Matlab.

Source code repository and issue tracker:
   https://gitlab.com/xamcosta/Anafit

Python Package Index:
   https://pypi.python.org/pypi/anafit/0.1.5

Requirements
------------

Python:
   Anafit has been coded using Python 3.5 from Anaconda_ distribution.

pip/setuptools:
   Those are the most convenient way to install Anafit and its dependencies. 
   Most likely they are already installed in your system, but if not, please 
   refer to `pip`_ doc webpage.

Matplotlib and PyQt5:
   When called, Anafit menu, based on `PyQt5`_, will appear as a new button in the 
   `matplotlib`_ figure toolbar. However, this requires Qt5Agg as matplotlib’s 
   backend. 
   WARNING : When imported, anafit will switch your actual backend to Qt5Agg, 
   destroying all figures already constructed during your session. 

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

First, import anafit:

.. code:: python

   import anafit

Note that importing anafit will switch matplotlib’s backend to ‘Qt5Agg’, destroying your current figures ! To prevent this, the best is to import anafit BEFORE importing matplotlib.pyplot or pylab.

Adding anafit button to a matplotlib figure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is done simply by calling anafit.Figure() class:

.. code:: python

   fig = plt.figure() 
   ana = anafit.Figure(fig)

If no argument is passed to anafit.Figure(), the anafit button will be added to the
current active figure.

Fitting a curve
^^^^^^^^^^^^^^^

In case several curves are plotted, you can select the one you wanna fit in the “Dataset” menu. The dataset are represented by a icon filled with the color of the curve, followed by their marker. 

Then, in the “Show Fit” menu, you can select predefined fitting functions, sorted by types (linear, power, etc…), or your own saved fitting functions, or any function you want to define on the way, using “Other Fit…”.

The fitting curve will appear as an orange line on your figure, and its parameters will appear in the Python console. You can access them anytime through the attribute ana.lastFit . More generally, an history of fits is stored in ana.fits . These anafit.Fit object contains not only the fit informations, but also the handles of the fit line, allowing to easily change the style of the fit curve. For instance, you can change the color of the last fit by simply running:

.. code:: python
 
   ana.fits[-1].linfit.set_color(‘r’)


Defining a region of interest (ROI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can restrict the range on which you wanna fit your datas in the “Define Range” menu. This menu displays the current range, and offers the possibility to set the range manually in a dialog (‘Define…’) or by selecting two points on the figure (‘Define ROI’). You can restore the full range by selecting ‘Reset’.

Creating custom fit functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create your own fitting functions in the ‘Edit User Fit’ menu. They will then appear in the ’Show Fit’ menu. Those fitting functions are stored in a text file in the anafit repository, that you can edit by hand. Clicking ‘Reset’ deletes all custom fitting functions, but let one as an example.

Getting slopes from drawn lines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can draw a line on the figure by selecting ‘Draw Line’, and remove it using ‘Undo Line’. Use ‘Get Slope’ to access the parameters of this line: in log-log scale, this returns the prefactor and the exponent of a power law.

You can draw a line corresponding to a given slope (a given exponent in log-log scale) using ‘Show Slope’.

Displaying fit infos
^^^^^^^^^^^^^^^^^^^^

You can display the range of confidence of the fit curve by selecting ’Show Confidence’. The interval of confidence is evaluated using the square root of the diagonal of the covariance matrix. 


