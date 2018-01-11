#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:38:27 2017

@author: costalongam
"""
import functools
import json
import os
import sys
import matplotlib
if 'matplotlib.pyplot' in sys.modules:
    matplotlib.pyplot.switch_backend('Qt5Agg')
elif 'matplotlib.pylab' in sys.modules:
    matplotlib.pylab.switch_backend('Qt5Agg')
elif not matplotlib.get_backend() == 'Qt5Agg':
        matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from scipy.optimize import curve_fit
from .ui import Ui_Fit, CustomFitDialog
from .utilities import *


class Fit(object):
    def __init__(self, xydata, fname, p=None):
        """
        Class containing all information corresponding to a fitted set of data:
        the xy sets of data, the fitting function, its parameters and their 
        initialising values as well as the covariant matrix from the fit. Uses 
        scipy.optimize.curve_fit
    
        Parameters
        ----------
    
        xydata: numpy.ndarray
            2 columns array containing x and y data to be fitted
        fname: str
            fitting function name (a key from fitting functions dict)
        p: tuple, optional
            if provided, the initialising parameters contained in the string 
            definition of the fitting function are ignored and set to p
            Default: None
    
        """
        self._popt, self._pcov = None, None
        self._xydata = xydata
        self._fname = fname
        if ';' not in fname:
            if p is None:
                fdef = get_func(self._fname)
                self._f, self._p = from_fdef(fdef)
            else:
                fdef = get_func(self._fname)
                self._f, _ = from_fdef(fdef)
                self._p = p
        else:
            self._f, self._p = from_fdef(fname)
        self.fit()

    @property
    def xydata(self):
        return self._xydata

    @xydata.setter
    def xydata(self, xydata):
        self.__init__(xydata, self._fname)

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, fname):
        self.__init__(self._xydata, fname)

    @property
    def f(self):
        return self._f

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, p):
        self._p = p
        self.fit()

    @property
    def popt(self):
        return self._popt

    @property
    def pcov(self):
        return self._pcov

    def fit(self):
        self._popt, self._pcov = curve_fit(self._f, self._xydata[:, 0], self._xydata[:, 1],
                                           p0=self._p)

    def __repr__(self):
        xrange = 'Xrange : [{0:.1f}, {0:.1f}]'.format(np.min(self._xydata[:, 0]), np.max(self._xydata[:, 0]))
        fit = 'Fitting function : ' + self._fname
        init = 'Initialising parameters : {0}'.format(self._p)
        coef = 'Coeff. : {0}'.format(self._popt)
        return xrange + '\n' + fit + '\n' + init + '\n' + coef


class DrawLine(object):
    def __init__(self, fig, show_slope=None):
        """
        Class allowing to draw dynamically a line on a matplotlib plot
    
        Parameters
        ----------
    
        fig: matplotlib.pyplot.figure object
            the figure window to draw the line in
        show_slope: float, optional
            If provided, the line to be drawn will have a slope given by 
            show_slope. If the scale is log-log, this corresponds to the 
            exponent of a power law
            Default: None
    
        """
        self.b = None
        self.fig = fig
        self.ax = fig.gca()
        self.slope = show_slope
        self.pt1 = np.array(plt.ginput(1)[0])
        self.pt2 = None
        self.lx, = self.ax.plot(*self.pt1, 'k--')
        self.cmove = self.fig.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        self.cclicked = self.fig.canvas.mpl_connect('button_press_event', self.mouse_clicked)

    def mouse_move(self, event):
        """
        Draws a line following the mouse cursor or a given slope when the mouse
        is moved in the figure window
    
        Parameters
        ----------
    
        event: matplotlib mouse motion_notify_event
    
        """
        if not event.inaxes:
            return
        x = event.xdata
        if self.slope is None:
            y = event.ydata
        else:
            if self.ax.get_xscale() == 'log' and self.ax.get_yscale() == 'log':
                y = np.exp(np.log(self.pt1[1]) - self.slope * np.log(self.pt1[0])) * x ** self.slope
            else:
                y = self.slope * (x - self.pt1[0]) + self.pt1[1]
        self.lx.set_ydata([self.pt1[1], y])
        self.lx.set_xdata([self.pt1[0], x])
        self.fig.canvas.draw()

    def mouse_clicked(self, event):
        """
        Terminates the line drawing to a clicked point in the figure window
    
        Parameters
        ----------
    
        event: matplotlib mouse button_press_event
    
        """
        if not event.inaxes:
            return
        if self.slope is None:
            self.pt2 = [event.xdata, event.ydata]
        else:
            self.pt2 = [event.xdata,
                        np.exp(np.log(self.pt1[1]) - self.slope * np.log(self.pt1[0])) * event.xdata ** self.slope]
        self.get_slope()
        self.lx.set_xdata([self.pt1[0], self.pt2[0]])
        self.lx.set_ydata([self.pt1[1], self.pt2[1]])
        self.fig.canvas.draw()
        self.fig.canvas.mpl_disconnect(self.cmove)
        self.fig.canvas.mpl_disconnect(self.cclicked)

    def get_slope(self):
        """
        Returns parameters corresponding to a drawn line on the figure window.
        If scale is lin-lin, returns a and b from y = ax+b line definition.
        If scale is log-log, returns n and a from y = ax^n line definition.
        
        Returns
        ----------
        slope: float
            slope or power law exponent
        b: float
            origin value or power law prefactor
    
        """
        if self.slope is None:
            if self.ax.get_xscale() == 'log' and self.ax.get_yscale() == 'log':
                self.slope = (np.log(self.pt2[1]) - np.log(self.pt1[1])) / (np.log(self.pt2[0]) - np.log(self.pt1[0]))
            else:
                self.slope = (self.pt2[1] - self.pt1[1]) / (self.pt2[0] - self.pt1[0])
        if self.ax.get_xscale() == 'log' and self.ax.get_yscale() == 'log':
            self.b = np.exp(np.log(self.pt2[1]) - self.slope * np.log(self.pt2[0]))
        else:
            self.b = self.pt2[1] - self.slope * self.pt2[0]
        return self.slope, self.b

    def __repr__(self):
        if self.ax.get_xscale() == 'log' and self.ax.get_yscale() == 'log':
            lstr = 'Line a*x^n : a = {0:.1f} , n = {1:.1f} \n'.format(self.b, self.slope)
        else:
            lstr = 'Line a*x+b : a = {0:.1f} , b = {1:.1f} \n'.format(self.slope, self.b)
        return lstr


class Figure(Ui_Fit):
    def __init__(self, fig=None):
        """
        Class constructing the anafit menu and includes it in the toolbar of a
        matplotlib.pyplot.figure
    
        Parameters
        ----------
    
        fig: matplotlib.pyplot.figure object
            the figure window where to include anafit. If not provided, the 
            current figure is used (plt.gcf())
            Default: None
    
        """
        if fig is None:
            fig = plt.gcf()
        self._fig = fig
        if not fig.axes:
            raise ValueError('Needs an axis before fitting')
        if not fig.axes[0].lines:
            raise ValueError('Needs some points before fitting')
        super().__init__()
        self._ax = fig.axes
        self._dictlin = {(lin.get_color() + lin.get_marker()): lin for axe in self._ax for lin in axe.get_lines()}
        self._currentLine = self._ax[0].lines[0].get_color() + self._ax[0].lines[0].get_marker()
        self._fits = {}
        self._lastFit = []
        self._linFit = []
        self._xrange = ()
        self._lines = []

        toolbar = self._fig.canvas.toolbar
        toolbar.addWidget(self.button)

        # Populating the datasets
        for lin in self._dictlin.keys():
            self.dataAction[lin] = QtWidgets.QAction(lin, self.datasetMenu)
            self.dataAction[lin].triggered.connect(functools.partial(self.set_current_line, lin))
            self.datasetMenu.insertAction(self.datasetSep, self.dataAction[lin])
            self.dataAction[lin].setEnabled(True)
        self.dataAction[self._currentLine].setEnabled(False)

        # Populating linear fits
        for fname in get_func(typefunc='linear').keys():
            self.linearFitMenu.addAction(fname, functools.partial(self.fit, fname))

        # Populating power fits
        for fname in get_func(typefunc='power').keys():
            self.powerFitMenu.addAction(fname, functools.partial(self.fit, fname))

        # Populating custom fits
        for fname in get_func(typefunc='custom').keys():
            self.showCustomFitActions[fname] = QtWidgets.QAction(fname, self.showCustomFitActionGroup)
            self.showCustomFitActions[fname].triggered.connect(functools.partial(self.fit, fname))
            self.showCustomFitActionGroup.addAction(self.showCustomFitActions[fname])
        self.showFitMenu.insertActions(self.showFitSep, self.showCustomFitActionGroup.actions())

        for fname in get_func(typefunc='custom').keys():
            self.editFitActions[fname] = QtWidgets.QAction(fname, self.editFitActionGroup)
            self.editFitActions[fname].triggered.connect(functools.partial(self.edit_fit, fname))
            self.editFitActionGroup.addAction(self.editFitActions[fname])
        self.editFitMenu.insertActions(self.editFitSep, self.editFitActionGroup.actions())

    @property
    def fig(self):
        return self._fig

    @fig.setter
    def fig(self, fig):
        self._fig = fig

    @property
    def current_line(self):
        return self._currentLine

    @current_line.setter
    def current_line(self, lin):
        for key in self._dictlin.keys():
            self.dataAction[key].setEnabled(True)
        self.dataAction[lin].setEnabled(False)
        self._currentLine = lin

    def set_current_line(self, lin):
        """
        Another setter for the current dataset. Used as a slot for the dataset
        selection menu's actions
    
        Parameters
        ----------
    
        lin: matplotlib.pyplot.line object
            the dataset line object
    
        """
        self.current_line = lin

    @property
    def last_fit(self):
        return self._lastFit

    @property
    def fits(self):
        return self._fits

    def undo_fit(self):
        """
        Slot to undo the last fit. 
        Note that it does not affect the fit history !
    
        """
        self._linFit[-1][0].remove()
        del self._linFit[-1]
        self.fig.canvas.draw()

    def remove_all_fit(self):
        """
        Slot to remove all fit. Also deletes the fit history !
    
        """
        for lin in self._linFit:
            lin[0].remove()
        self._linFit = []
        self._fits = {}
        self._lastFit = []
        self.fig.canvas.draw()

    def refresh_dataset(self):
        """
        Slot to refresh dataset menu, for instance if a new plot has been added
        after anafit.Figure() called
        
        """
        newlin = {(lin.get_color() + lin.get_marker()): lin for axe in self._ax for lin in axe.get_lines()}
        for lin in set(newlin.keys()).difference(self._dictlin.keys()):
            self.dataAction[lin] = QtWidgets.QAction(lin, self.datasetMenu)
            self.dataAction[lin].triggered.connect(functools.partial(self.set_current_line, lin))
            self.datasetMenu.insertAction(self.datasetSep, self.dataAction[lin])
            self.dataAction[lin].setEnabled(True)
        for lin in set(self._dictlin.keys()).difference(newlin.keys()):
            self.datasetMenu.removeAction(self.dataAction[lin])
            del self.dataAction[lin]
        self._dictlin = newlin
        self._currentLine = self._ax[0].get_lines()[0].get_color() + self._ax[0].get_lines()[0].get_marker()
        self.dataAction[self._currentLine].setEnabled(False)

    def define_range(self):
        """
        Slot to display a dialog asking the user for a tuple corresponding to 
        the xrange to consider for fitting
    
        """
        xrange, ok = QtWidgets.QInputDialog.getText(self.showFitMenu,
                                                    'Enter the x-range where to fit',
                                                    'ex: (10, 100) :')
        if ok:
            self._xrange = eval(xrange)
            self.rangeAction.setText('Current : ({0:.1f}, {1:.1f})'.format(*self._xrange))
        else:
            pass

    def define_roi(self):
        """
        Slot to define the x-fitting range graphically, by selecting two points
    
        """
        pts = plt.ginput(2, show_clicks=True)
        if pts[0][0] < pts[0][1]:
            self._xrange = (pts[0][0], pts[1][0])
        else:
            self._xrange = (pts[1][0], pts[0][0])
        self.rangeAction.setText('Current : ({0:.1f}, {1:.1f})'.format(*self._xrange))

    def reset_range(self):
        """
        Slot to reset the xr-fitting range, therefore using the full range
    
        """
        self._xrange = ()
        self.rangeAction.setText('Current : full')

    def fit(self, strfunc):
        """
        Fit the selected dataset by the function of name strfunc. Uses 
        scipy.optimize.curve_fit. Print fitting infos in command line.
        
        Parameters
        ----------
    
        strfunc: str
            function name (a key from fitting functions dict)
    
        """
        lin = self._dictlin[self._currentLine]
        if self._xrange is ():
            xydata = lin.get_xydata()
        else:
            xydata = np.array([xy for xy in lin.get_xydata() if self._xrange[0] < xy[0] < self._xrange[1]])
        fitted = Fit(xydata, strfunc)
        if self._currentLine in self._fits.keys():
            self._fits[self._currentLine].append(fitted)
        else:
            self._fits[self._currentLine] = [fitted]
        self._lastFit = fitted
        linfit = lin.axes.plot(self._lastFit.xydata[:, 0], list(
            map(lambda x: self._lastFit.f(x, *self._lastFit.popt), self._lastFit.xydata[:, 0])), 'r-')
        self._linFit.append(linfit)
        print(self._lastFit)
        self.fig.canvas.draw()

    def other_fit(self):
        """
        Slot to fit the current selected dataset by a function asked to the 
        user through a dialog
    
        """
        fdef, ok = QtWidgets.QInputDialog.getText(self.showFitMenu,
                                                  'Enter your fitting function',
                                                  'ex: lambda x, a, b : a*x+b ; (1, 0.1) :')
        if ok:
            self.fit(fdef)
        else:
            pass

    def edit_fit(self, fname):
        """
        Slot to edit an already defined custom fitting function
        
        Parameters
        ----------
    
        fname: str
            function name (a key from fitting functions dict)
    
        """
        efDialog = QtWidgets.QDialog()
        editFitDialog = CustomFitDialog(efDialog, fname)
        efDialog.show()
        if efDialog.exec_() == QtWidgets.QDialog.Accepted:
            customlist = get_func(typefunc='custom')
            del customlist[fname]
            self.showFitMenu.removeAction(self.showCustomFitActions[fname])
            self.editFitMenu.removeAction(self.editFitActions[fname])
            customlist[editFitDialog.fname] = editFitDialog.fdef
            save_customlist(customlist)
            self.add_fit_in_menu(editFitDialog.fname)
        else:
            pass

    def new_fit(self):
        """
        Slot to define a new custom fitting function that will be saved in 
        customFit.txt
    
        """
        cfDialog = QtWidgets.QDialog()
        customFitDialog = CustomFitDialog(cfDialog)
        cfDialog.show()
        if cfDialog.exec_() == QtWidgets.QDialog.Accepted:
            customlist = get_func(typefunc='custom')
            customlist[customFitDialog.fname] = customFitDialog.fdef
            save_customlist(customlist)
            self.add_fit_in_menu(customFitDialog.fname)
        else:
            pass

    def reset_fit(self):
        """
        Slot to delete all custom fitting functions and refresh the Show Fit 
        menu and Edit User Fit menu
    
        """
        for k in set(self.showCustomFitActions.keys()).difference(['a(x-b)^2']):
            self.showFitMenu.removeAction(self.showCustomFitActions[k])
        for k in set(self.editFitActions.keys()).difference(['a(x-b)^2']):
            self.editFitMenu.removeAction(self.editFitActions[k])
        self.add_fit_in_menu('a(x-b)^2')
        customlist = {'a(x-b)^2': 'lambda x, a, b : a*(x-b)**2 ; (1, 1)'}
        save_customlist(customlist)

    def draw_line(self):
        """
        Slot to dynamically draw a line on the figure window
    
        """
        self._lines.append(DrawLine(self._fig))

    def undo_line(self):
        """
        Slot to remove the last drawn line
    
        """
        if self._lines:
            self._lines[-1].lx.remove()
            del self._lines[-1]
            self.fig.canvas.draw()

    def remove_all_lines(self):
        """
        Slot to remove all drawn lines. 
        CURRENTLY NOT USED
    
        """
        for lin in self._lines:
            lin.lx.remove()
        self._lines = []
        self.fig.canvas.draw()

    def get_slope(self):
        """
        Slot to get the slope of the last drawn line.
        If scale is lin-lin, print a and b from y = ax+b line definition.
        If scale is log-log, print n and a from y = ax^n line definition.
    
        """
        if len(self._lines) > 0:
            print(self._lines[-1])
        else:
            pass

    def show_slope(self):
        """
        Slot to draw a line corresponding to a given slope if scale is lin-lin,
        or to a given exponent if scale is log-log.
    
        """
        slope, ok = QtWidgets.QInputDialog.getText(self.menu,
                                                   'Enter the slope to show',
                                                   'ex: -1')
        if ok:
            self._lines.append(DrawLine(self._fig, show_slope=eval(slope)))
        else:
            pass


if __name__ == "__main__":
    plt.ion()
    my_fig = plt.figure()
    ax = my_fig.add_subplot(111)
    my_line, = ax.plot(np.arange(0, 100, 1), np.arange(50, 250, 2) + 10 * (np.random.rand(100) - 1 / 2), 'b+')
    ax.plot(np.arange(0, 100, 1), np.arange(0, 300, 3) + 30 * (np.random.rand(100) - 1 / 2), 'rx')
    ax.plot(np.arange(0, 100, 1), np.square(np.arange(0, 10, 0.1)) + 5 * (np.random.rand(100) - 1 / 2), 'k.')
    test = Figure(my_fig)
