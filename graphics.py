#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:38:27 2017

@author: costalongam
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.optimize import curve_fit
from PyQt5 import QtWidgets, QtGui


class Figure:
    def __init__(self, fig):
        self.fig = fig
        toolbar = fig.canvas.toolbar
        
#        self.button = QtWidgets.QPushButton('Colorize !')
        self.button = QtWidgets.QToolButton()
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.button.setIcon(QtGui.QIcon(os.path.join(self.script_path, 'ana_icon.png')))
        self.button.setPopupMode(2)
        
        self.menu = QtWidgets.QMenu()
        self.button.setMenu(self.menu)
        
        self.basicFitMenu = QtWidgets.QMenu('Basic fit')
        self.menu.addMenu(self.basicFitMenu)
        self.affineFitAction = QtWidgets.QAction('Affine', self.basicFitMenu)
        self.affineFitAction.triggered.connect(self.fitAffine)
        self.basicFitMenu.addAction(self.affineFitAction)
        
        self.customFitMenu = QtWidgets.QMenu('Custom fit')
        self.menu.addMenu(self.customFitMenu)
        self.testAction = QtWidgets.QAction('Colorize', self.customFitMenu)
        self.testAction.triggered.connect(self.colorize)
        self.customFitMenu.addAction(self.testAction)
        
        toolbar.addWidget(self.button)
        
#        self.button.clicked.connect(self.colorize)

    def fitAffine(self):
        xydata = plt.gca().get_lines()[0].get_xydata()
        f = lambda x, *p : p[0] * x + p[1]
        popt, pcov = curve_fit(f, xydata[:, 0], xydata[:, 1], p0=(0, 0))
        print('Param: {0}x + {1}'.format(popt[0], popt[1]))
        ax.plot(xydata[:, 0], popt[0] * xydata[:, 0] + popt[1], 'r-')
        self.fig.canvas.draw()

    def colorize(self):
        colors = ["black", "blue", "red", "green"]
        plt.gca().get_lines()[0].set_color(np.random.choice(colors))
        self.fig.canvas.draw()
        

     
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(0,100,1), np.arange(50,250,2) + 10*(np.random.rand(100) - 1/2), 'b+')
    test = Figure(fig)
    