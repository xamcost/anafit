#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:38:27 2017

@author: costalongam
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import functools
import dill as pickle # mandatory to import pickle like this to pickle lambdas
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from customFitDialog import Ui_customFitDialog

# global variable
script_path = os.path.dirname(os.path.abspath(__file__))

def get_func(strfunc=None, typefunc=None):
        linlist = {'ax':(lambda x, a : a*x, (1)), 
                    'ax+b':(lambda x, a, b : a*x+b, (1, 1)), 
                    'a(x-b)':(lambda x, a, b : a*(x-b), (1, 1))}
        powerlist = {'ax^n':(lambda x, a, n : a*(x**n), (1, 1)), 
                    'a+bx^n':(lambda x, a, c, n : a+b*(x**n), (1, 1, 1)), 
                    'a(x-b)^n':(lambda x, a, b, n : a*((x-b)**n), (1, 1, 1)), 
                    'a+b(x-c)^n':(lambda x, a, b, c, n : a+b*((x-c)**n), (1, 1, 1, 1))}
        fid = open(os.path.join(script_path, 'customFit.pkl'), 'rb')
        customlist = pickle.load(fid)
        fid.close()
        funclist = {**linlist, **powerlist, **customlist}
        if strfunc is None:
            if typefunc is None:
                return funclist
            elif typefunc == 'linear':
                return linlist
            elif typefunc == 'power':
                return powerlist
            elif typefunc == 'custom':
                return customlist
        else:
            return funclist[strfunc]


class CustomFitDialog(Ui_customFitDialog):
    def __init__(self, dialog):
        Ui_customFitDialog.__init__(self)
        self.setupUi(dialog)
        self.customFitButtonBox.rejected.connect(self.cancelbutton)

    def cancelbutton(self):
        exit()
        
class Fit(object):
    def __init__(self, xydata, fname, p=None):
        self._xydata = xydata
        self._fname = fname
        if p is None:
            self._f, self._p = get_func(self._fname)
        else: 
            self._f, _ = get_func(self._fname)
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
        self.__init__(self._xydata, self._fname, p)
        
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
        xrange = 'Xrange : [{0}, {1}]'.format(np.min(self._xydata[:,0]), np.max(self._xydata[:,0]))
        fit = 'Fitting function : ' + self._fname
        init = 'Initialising parameters : {0}'.format(self._p)
        coef = 'Coeff. : {0}'.format(self._popt)
        return xrange + '\n' + fit +'\n' + init +'\n' + coef    

class Figure:
    def __init__(self, fig=None):
        if fig is None:
            self._fig = plt.gcf()
        self._fig = fig
        self._ax = fig.get_axes()
        self._dictlin = {(lin.get_color() + lin.get_marker()):lin for axe in self._ax for lin in axe.get_lines()}
        self._currentLine = self._ax[0].get_lines()[0].get_color() + self._ax[0].get_lines()[0].get_marker()
        self._lastFit = {}
        self.cfDialog = QDialog()
        _ = CustomFitDialog(self.cfDialog)
        
        toolbar = self._fig.canvas.toolbar
        self.button = QToolButton()
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.button.setIcon(QIcon(os.path.join(script_path, 'ana_icon.png')))
        self.button.setPopupMode(2)
        self.menu = QMenu()
        self.button.setMenu(self.menu)
        toolbar.addWidget(self.button)
        
        self.datasetMenu = QMenu('Datasets')
        self.menu.addMenu(self.datasetMenu)
        self.dataAction = {}
        for lin in self._dictlin.keys():
            self.dataAction[lin] = QAction(lin, self.datasetMenu)
            self.dataAction[lin].triggered.connect(functools.partial(self.set_currentLine, lin))
            self.datasetMenu.addAction(self.dataAction[lin])
            self.dataAction[lin].setEnabled(True)
        self.dataAction[self._currentLine].setEnabled(False)
        
        self.basicFitMenu = QMenu('Basic fit')
        self.menu.addMenu(self.basicFitMenu)
        
        self.linearFitMenu = QMenu('Linear')
        self.basicFitMenu.addMenu(self.linearFitMenu)
        for fname in get_func(typefunc='linear').keys():
            self.linearFitMenu.addAction(fname, functools.partial(self.fit, fname))
        self.powerFitMenu = QMenu('Power')
        self.basicFitMenu.addMenu(self.powerFitMenu)
        for fname in get_func(typefunc='power').keys():
            self.powerFitMenu.addAction(fname, functools.partial(self.fit, fname))
        
        self.customFitMenu = QMenu('Custom fit')
        self.menu.addMenu(self.customFitMenu)
        for fname in get_func(typefunc='custom').keys():
            self.customFitMenu.addAction(fname, functools.partial(self.fit, fname))
        self.customFitMenu.addSeparator()
        self.customFitMenu.addAction('New Fit', self.new_customFit)
        
    @property
    def fig(self):
        return self._fig
    
    @fig.setter
    def fig(self, fig):
        self._fig = fig 
        
    @property
    def currentLine(self):
        return self._currentLine
    
    @currentLine.setter
    def currentLine(self, lin):
        for key in self._dictlin.keys():
            self.dataAction[key].setEnabled(True)
        self.dataAction[lin].setEnabled(False)
        self._currentLine = lin
        
    def set_currentLine(self, lin):
        self.currentLine = lin
        
    @property
    def lastFit(self):
        return self._lastFit
        
    def fit(self, strfunc):
        lin = self._dictlin[self._currentLine]
        self._lastFit = Fit(lin.get_xydata(), strfunc)
        lin.get_axes().plot(self._lastFit.xydata[:, 0], list(map(lambda x : self._lastFit.f(x, *self._lastFit.popt), self._lastFit.xydata[:, 0])), 'r-')
        self.fig.canvas.draw()
    
    def new_customFit(self):
        # TODO: create a QDialog that ask for the function
        self.cfDialog.show()
#        fid = open(os.path.join(self.script_path, 'customFit.pkl'),'wb')
#        pickle.dump(self._customFit, fid)
#        fid.close()

    def colorize(self):
        colors = ["black", "blue", "red", "green"]
        plt.gca().get_lines()[0].set_color(np.random.choice(colors))
        self.fig.canvas.draw()
        

        
if __name__ == "__main__":
#    import sys
#    app = QApplication(sys.argv)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(0,100,1), np.arange(50,250,2) + 10*(np.random.rand(100) - 1/2), 'b+')
    ax.plot(np.arange(0,100,1), np.arange(0,300,3) + 30*(np.random.rand(100) - 1/2), 'rx')
    ax.plot(np.arange(0,100,1), np.square(np.arange(0,10,0.1)) + 5*(np.random.rand(100) - 1/2), 'k.')
    test = Figure(fig)
#    app.exec_()
    