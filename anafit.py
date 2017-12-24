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
import sys
import json
from scipy.optimize import curve_fit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from customFitDialog import Ui_customFitDialog


# global variable
script_path = os.path.dirname(os.path.abspath(__file__))

def save_customlist(customlist):
    with open(os.path.join(script_path, 'customFit.txt'), 'w') as fid:
        json.dump(customlist, fid, indent=2, sort_keys=True)

def get_func(strfunc=None, typefunc=None):
        linlist = {'ax':'lambda x, a : a*x ; (1)', 
                    'ax+b':'lambda x, a, b : a*x+b ; (1, 1)', 
                    'a(x-b)':'lambda x, a, b : a*(x-b) ; (1, 1)'}
        powerlist = {'ax^n':'lambda x, a, n : a*(x**n) ; (1, 1)', 
                    'a+bx^n':'lambda x, a, c, n : a+b*(x**n) ; (1, 1, 1)', 
                    'a(x-b)^n':'lambda x, a, b, n : a*((x-b)**n) ; (1, 1, 1)', 
                    'a+b(x-c)^n':'lambda x, a, b, c, n : a+b*((x-c)**n) ; (1, 1, 1, 1)'}
        if os.path.exists(os.path.join(script_path, 'customFit.txt')):
            with open(os.path.join(script_path, 'customFit.txt'), 'r') as fid:
                customlist = json.load(fid)
        else:
            customlist = {}
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

def from_fdef(fdef):
    fstr, pstr = fdef.split(';')
    return eval(fstr), eval(pstr)

class CustomFitDialog(Ui_customFitDialog):
    def __init__(self, dialog, fname=None):
        super().__init__()
        self.setupUi(dialog)
#        self.customFitButtonBox.rejected.connect(self.cancelbutton)
        self.customFitButtonBox.accepted.connect(self.ok)
        if fname is not None:
            dialog.setWindowTitle('Edit Fit')
            fdef = get_func(strfunc=fname)
            self.customFitName.setText(fname)
            self.customFitDef.setText(fdef)
        
    def ok(self):
        self.fname = self.customFitName.text()
        self.fdef = self.customFitDef.text()

#    def cancelbutton(self):
#        self.close()
        
class Fit(object):
    def __init__(self, xydata, fname, p=None):
        self._xydata = xydata
        self._fname = fname
        if ';'  not in fname:
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
        xrange = 'Xrange : [{0}, {1}]'.format(np.min(self._xydata[:,0]), np.max(self._xydata[:,0]))
        fit = 'Fitting function : ' + self._fname
        init = 'Initialising parameters : {0}'.format(self._p)
        coef = 'Coeff. : {0}'.format(self._popt)
        return xrange + '\n' + fit +'\n' + init +'\n' + coef    

class Figure:
    def __init__(self, fig=None):
        if fig is None:
            fig = plt.gcf()
        self._fig = fig
        self._ax = fig.get_axes()
        self._dictlin = {(lin.get_color() + lin.get_marker()):lin for axe in self._ax for lin in axe.get_lines()}
        self._currentLine = self._ax[0].get_lines()[0].get_color() + self._ax[0].get_lines()[0].get_marker()
        self._lastFit = {}
        self._linFit = []
        self._xrange = ()
        
        toolbar = self._fig.canvas.toolbar
        self.button = QToolButton()
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.button.setIcon(QIcon(os.path.join(script_path, 'ana_icon.png')))
        self.button.setPopupMode(2)
        self.menu = QMenu()
        self.button.setMenu(self.menu)
        toolbar.addWidget(self.button)
        
        self.menu.addAction('Undo Fit', self.undo_fit, QKeySequence.Undo)
        self.menu.addAction('Remove all fit', self.remove_all_fit, QKeySequence('Shift+Ctrl+Z'))
        self.menu.addSeparator()
        
        self.datasetMenu = QMenu('Dataset')
        self.menu.addMenu(self.datasetMenu)
        self.dataAction = {}
        for lin in self._dictlin.keys():
            self.dataAction[lin] = QAction(lin, self.datasetMenu)
            self.dataAction[lin].triggered.connect(functools.partial(self.set_currentLine, lin))
            self.datasetMenu.addAction(self.dataAction[lin])
            self.dataAction[lin].setEnabled(True)
        self.dataAction[self._currentLine].setEnabled(False)
        
        self.defineRangeMenu = QMenu('Define Range')
        self.menu.addMenu(self.defineRangeMenu)
        self.rangeAction = QAction('Current: full', self.defineRangeMenu)
        self.defineRangeMenu.addAction(self.rangeAction)
        self.rangeAction.setEnabled(False)
        self.defineRangeMenu.addSeparator()
        self.defineRangeMenu.addAction('Define ...', self.define_range, QKeySequence('Shift+Ctrl+X'))
        self.defineRangeMenu.addAction('Define ROI', self.define_roi, QKeySequence('Ctrl+X'))
        self.defineRangeMenu.addAction('Reset', self.reset_range)
        
        self.showFitMenu = QMenu('Show Fit')
        self.menu.addMenu(self.showFitMenu)
        self.editFitMenu = QMenu('Edit User Fit')
        self.menu.addMenu(self.editFitMenu)
        
        self.linearFitMenu = QMenu('Linear')
        self.showFitMenu.addMenu(self.linearFitMenu)
        for fname in get_func(typefunc='linear').keys():
            self.linearFitMenu.addAction(fname, functools.partial(self.fit, fname))
        self.powerFitMenu = QMenu('Power')
        self.showFitMenu.addMenu(self.powerFitMenu)
        for fname in get_func(typefunc='power').keys():
            self.powerFitMenu.addAction(fname, functools.partial(self.fit, fname))
        self.showFitMenu.addSeparator()
        
        self.showCustomFitActionGroup = QActionGroup(self.showFitMenu)
        self.showCustomFitActions = {}
        for fname in get_func(typefunc='custom').keys():
            self.showCustomFitActions[fname] = QAction(fname, self.showCustomFitActionGroup)
            self.showCustomFitActions[fname].triggered.connect(functools.partial(self.fit, fname))
            self.showCustomFitActionGroup.addAction(self.showCustomFitActions[fname])
        self.showFitMenu.addActions(self.showCustomFitActionGroup.actions())
        self.showFitSep = self.showFitMenu.addSeparator()
        self.showFitMenu.addAction('Other Fit...', self.other_fit, QKeySequence('Ctrl+O'))
        
        self.editFitActionGroup = QActionGroup(self.showFitMenu)
        self.editFitActions = {}
        for fname in get_func(typefunc='custom').keys():
            self.editFitActions[fname] = QAction(fname, self.editFitActionGroup)
            self.editFitActions[fname].triggered.connect(functools.partial(self.edit_fit, fname))
            self.editFitActionGroup.addAction(self.editFitActions[fname])
        self.editFitMenu.addActions(self.editFitActionGroup.actions())
        self.editFitSep = self.editFitMenu.addSeparator()
        self.editFitMenu.addAction('New Fit', self.new_fit, QKeySequence.New)
        self.editFitMenu.addSeparator()
        self.editFitMenu.addAction('Reset', self.reset_fit)
        
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
    
    def undo_fit(self):
        self._linFit[-1][0].remove()
        del self._linFit[-1]
        self.fig.canvas.draw()
        
    def remove_all_fit(self):
        for lin in self._linFit:
            lin[0].remove()
        self._linFit = []
        self.fig.canvas.draw()
        
    def define_range(self):
        xrange, ok = QInputDialog.getText(self.showFitMenu, 
                                        'Enter the x-range where to fit', 
                                        'ex: (10, 100) :')
        if ok:
            self._xrange = eval(xrange)
            self.rangeAction.setText('Current : ({0}, {1})'.format(*self._xrange))
        else:
            pass
        
    def define_roi(self):
        pts = plt.ginput(2, show_clicks=True)
        if pts[0][0] < pts[0][1]:
            self._xrange = (pts[0][0], pts[1][0])
        else:
            self._xrange = (pts[1][0], pts[0][0])
        self.rangeAction.setText('Current : ({0:.1f}, {1:.1f})'.format(*self._xrange))
        
    def reset_range(self):
        self._xrange = ()
        self.rangeAction.setText('Current : full')
    
    def add_fit_in_menu(self, fname):
        self.showCustomFitActions[fname] = QAction(fname, self.showCustomFitActionGroup)
        self.showCustomFitActions[fname].triggered.connect(functools.partial(self.fit, fname))
        self.showFitMenu.insertAction(self.showFitSep, self.showCustomFitActions[fname])
        
        self.editFitActions[fname] = QAction(fname, self.editFitActionGroup)
        self.editFitActions[fname].triggered.connect(functools.partial(self.edit_fit, fname))
        self.editFitMenu.insertAction(self.editFitSep, self.editFitActions[fname])
        
    def fit(self, strfunc):
        lin = self._dictlin[self._currentLine]
        if self._xrange is ():
            xydata = lin.get_xydata()
        else:
            xydata = np.array([xy for xy in lin.get_xydata() if xy[0] > self._xrange[0] and xy[0] < self._xrange[1]])
        self._lastFit = Fit(xydata, strfunc)
        linfit = lin.get_axes().plot(self._lastFit.xydata[:, 0], list(map(lambda x : self._lastFit.f(x, *self._lastFit.popt), self._lastFit.xydata[:, 0])), 'r-')
        self._linFit.append(linfit)
        print(self._lastFit)
        self.fig.canvas.draw()
        
    def other_fit(self):
        fdef, ok = QInputDialog.getText(self.showFitMenu, 
                                        'Enter your fitting function', 
                                        'ex: lambda x, a, b : a*x+b ; (1, 0.1) :')
        if ok:
            self.fit(fdef)
        else:
            pass
    
    def edit_fit(self, fname):
        efDialog = QDialog()
        editFitDialog = CustomFitDialog(efDialog, fname)
        efDialog.show()
        if efDialog.exec_() == QDialog.Accepted:
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
        cfDialog = QDialog()
        customFitDialog = CustomFitDialog(cfDialog)
        cfDialog.show()
        if cfDialog.exec_() == QDialog.Accepted:
            customlist = get_func(typefunc='custom')
            customlist[customFitDialog.fname] = customFitDialog.fdef
            save_customlist(customlist)
            self.add_fit_in_menu(customFitDialog.fname)
        else:
            pass
        
    def reset_fit(self):
        for k in set(self.showCustomFitActions.keys()).difference(['a(x-b)^2']):
            self.showFitMenu.removeAction(self.showCustomFitActions[k])
        for k in set(self.editFitActions.keys()).difference(['a(x-b)^2']):
            self.editFitMenu.removeAction(self.editFitActions[k])
        self.add_fit_in_menu('a(x-b)^2')
        customlist = {'a(x-b)^2':'lambda x, a, b : a*(x-b)**2 ; (1, 1)'}
        save_customlist(customlist)
        
        
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
    