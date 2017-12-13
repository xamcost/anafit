#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 22:38:27 2017

@author: costalongam
"""

import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtWidgets


class Figure:
    def __init__(self, fig):
        self.fig = fig
        toolbar = fig.canvas.toolbar
        self.button = QtWidgets.QPushButton('Colorize !')
        toolbar.addWidget(self.button)
        self.button.clicked.connect(self.colorize)

    def colorize(self):
        colors = ["black", "blue", "red", "green"]
        plt.gca().get_lines()[0].set_color(np.random.choice(colors))
        self.fig.canvas.draw()
        
        
if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(0,100,1), np.random.rand(100))
    test = Figure(fig)
    