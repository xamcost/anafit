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
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def get_func(strfunc=None, typefunc=None):
    linlist = {'ax':(lambda x, a : a*x), 
                'ax+b':(lambda x, a, b : a*x+b), 
                'a(x-b)':(lambda x, a, b : a*(x-b))}
    powerlist = {'ax^n':(lambda x, a, n : a*(x**n)), 
                'c+ax^n':(lambda x, c, a, n : c+a*(x**n)), 
                'a(x-b)^n':(lambda x, a, b, n : a*((x-b)**n)), 
                'c+a(x-b)^n':(lambda x, c, a, b, n : c+a*((x-b)**n))}
    funclist = {**linlist, **powerlist}
    if strfunc is None:
        if typefunc is None:
            return funclist
        elif typefunc == 'linear':
            return linlist
        elif typefunc == 'power':
            return powerlist
    else:
        return funclist[strfunc]


class Figure:
    def __init__(self, fig=None):
        if fig is None:
            self._fig = plt.gcf()
        self._fig = fig
        self._ax = fig.get_axes()
        self._dictlin = {(lin.get_color() + lin.get_marker()):lin for axe in self._ax for lin in axe.get_lines()}
        self._currentLine = self._ax[0].get_lines()[0].get_color() + self._ax[0].get_lines()[0].get_marker()
        self._lastFit = {}
        
        toolbar = self._fig.canvas.toolbar
        self.button = QToolButton()
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.button.setIcon(QIcon(os.path.join(self.script_path, 'ana_icon.png')))
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
        self.testAction = QAction('Colorize', self.customFitMenu)
        self.testAction.triggered.connect(self.colorize)
        self.customFitMenu.addAction(self.testAction)
        
#        self.button.clicked.connect(self.colorize)
        
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
    
    @lastFit.setter
    def lastFit(self, lastFit):
        self._lastFit = lastFit

    def fit(self, strfunc):
        xydata = self._dictlin[self._currentLine].get_xydata()
        f = get_func(strfunc)
        popt, pcov = curve_fit(f, xydata[:, 0], xydata[:, 1], p0=tuple(np.zeros(f.__code__.co_argcount - 1)))
        self._lastFit.update({'curve':self._currentLine ,'xrange':xydata[:, 0], 'name':strfunc, 'coef':popt, 'cov':pcov})
        self._dictlin[self._currentLine].get_axes().plot(xydata[:, 0], list(map(lambda x : f(x, *popt), xydata[:, 0])), 'r-')
        self.fig.canvas.draw()
        

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
    