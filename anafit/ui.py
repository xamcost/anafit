from PyQt5 import QtGui
from PyQt5 import QtWidgets
import os
import matplotlib.pyplot as plt
import functools
from .customFitDialog import Ui_customFitDialog
from .utilities import *


class Ui_Fit:

    def __init__(self):
        """
        Class constructing the anafit UI

        """

        self.button = QtWidgets.QToolButton()
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.button.setIcon(QtGui.QIcon(os.path.join(script_path, 'ana_icon.png')))
        self.button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.menu = QtWidgets.QMenu()
        self.button.setMenu(self.menu)

        self.menu.addAction('Undo Fit', self.undo_fit, QtGui.QKeySequence.Undo)
        self.menu.addAction('Remove all fit', self.remove_all_fit, QtGui.QKeySequence('Shift+Ctrl+Z'))
        self.menu.addSeparator()

        self.datasetMenu = QtWidgets.QMenu('Dataset')
        self.menu.addMenu(self.datasetMenu)
        self.dataAction = {}
        self.dataActionIcon = {}
        self.datasetSep = self.datasetMenu.addSeparator()
        self.datasetMenu.addAction('Refresh', self.refresh_dataset)
        self.defineRangeMenu = QtWidgets.QMenu('Define Range')
        self.menu.addMenu(self.defineRangeMenu)
        self.rangeAction = QtWidgets.QAction('Current: full', self.defineRangeMenu)
        self.defineRangeMenu.addAction(self.rangeAction)
        self.rangeAction.setEnabled(False)
        self.defineRangeMenu.addSeparator()
        self.defineRangeMenu.addAction('Define ...', self.define_range, QtGui.QKeySequence('Shift+Ctrl+X'))
        self.defineRangeMenu.addAction('Define ROI', self.define_roi, QtGui.QKeySequence('Ctrl+X'))
        self.defineRangeMenu.addAction('Reset', self.reset_range)

        self.showFitMenu = QtWidgets.QMenu('Show Fit')
        self.menu.addMenu(self.showFitMenu)
        self.linearFitMenu = QtWidgets.QMenu('Linear')
        self.showFitMenu.addMenu(self.linearFitMenu)
        self.powerFitMenu = QtWidgets.QMenu('Power')
        self.showFitMenu.addMenu(self.powerFitMenu)
        self.expFitMenu = QtWidgets.QMenu('Exponential')
        self.showFitMenu.addMenu(self.expFitMenu)
        self.showFitMenu.addSeparator()
        self.showCustomFitActionGroup = QtWidgets.QActionGroup(self.showFitMenu)
        self.showCustomFitActions = {}
        self.showFitSep = self.showFitMenu.addSeparator()
        self.showFitMenu.addAction('Other Fit...', self.other_fit, QtGui.QKeySequence('Ctrl+O'))
        
        self.editFitMenu = QtWidgets.QMenu('Edit User Fit')
        self.menu.addMenu(self.editFitMenu)
        self.editFitActionGroup = QtWidgets.QActionGroup(self.showFitMenu)
        self.editFitActions = {}
        self.editFitSep = self.editFitMenu.addSeparator()
        self.editFitMenu.addAction('New Fit', self.new_fit, QtGui.QKeySequence.New)
        self.editFitMenu.addSeparator()
        self.editFitMenu.addAction('Reset', self.reset_fit)
        
        self.displayMenu = QtWidgets.QMenu('Display Options')
        self.menu.addMenu(self.displayMenu)
        self.showFitInfoAction = QtWidgets.QAction('Show Fit Info', self.displayMenu)
        self.showFitInfoAction.setCheckable(True)
        self.showFitInfoAction.setShortcut(QtGui.QKeySequence('Ctrl+I'))
        self.showFitInfoAction.triggered.connect(self.show_fitInfo)
        self.displayMenu.addAction(self.showFitInfoAction)
        self.showConfidenceAction = QtWidgets.QAction('Show Confidence', self.displayMenu)
        self.showConfidenceAction.setCheckable(True)
        self.showConfidenceAction.triggered.connect(self.show_confidence)
        self.displayMenu.addAction(self.showConfidenceAction)

        self.menu.addSeparator()
        self.menu.addAction('Draw Line', self.draw_line, QtGui.QKeySequence('Ctrl+L'))
        self.menu.addAction('Undo Line', self.undo_line, QtGui.QKeySequence('Shift+Ctrl+L'))
        self.menu.addAction('Get Slope', self.get_slope, QtGui.QKeySequence('Ctrl+G'))
        self.menu.addAction('Show Slope', self.show_slope, QtGui.QKeySequence('Shift+Ctrl+G'))

    @property
    def fig(self):
        pass

    @fig.setter
    def fig(self, fig):
        pass

    @property
    def current_line(self):
        pass

    @current_line.setter
    def current_line(self, lin):
        pass

    def set_current_line(self, lin):
        pass

    @property
    def last_fit(self):
        pass

    @property
    def fits(self):
        pass

    def undo_fit(self):
        pass

    def remove_all_fit(self):
        pass

    def refresh_dataset(self):
        pass

    def define_range(self):
        pass

    def define_roi(self):
        pass

    def reset_range(self):
        pass

    def add_fit_in_menu(self, fname):
        """
        Creates new actions in Show Fit menu and Edit User Fit menu when a new
        custom fitting function of name fname is defined

        Parameters
        ----------

        fname: str
            function name (a key from fitting functions dict)

        """
        self.showCustomFitActions[fname] = QtWidgets.QAction(fname, self.showCustomFitActionGroup)
        self.showCustomFitActions[fname].triggered.connect(functools.partial(self.fit, fname))
        self.showFitMenu.insertAction(self.showFitSep, self.showCustomFitActions[fname])

        self.editFitActions[fname] = QtWidgets.QAction(fname, self.editFitActionGroup)
        self.editFitActions[fname].triggered.connect(functools.partial(self.edit_fit, fname))
        self.editFitMenu.insertAction(self.editFitSep, self.editFitActions[fname])

    def other_fit(self):
        pass

    def edit_fit(self, fname):
        pass

    def new_fit(self):
        pass

    def reset_fit(self):
        pass

    def draw_line(self):
        pass

    def undo_line(self):
        pass

    def remove_all_lines(self):
        pass

    def get_slope(self):
        pass

    def show_slope(self):
        pass
    
    def show_fitInfo(self):
        pass
    
    def show_confidence(self):
        pass


class CustomFitDialog(Ui_customFitDialog):
    def __init__(self, dialog, fname=None):
        """
        Class constructing a dialog to ask the user for a function name and its
        corresponding definition

        Parameters
        ----------

        dialog : QDialog
            base dialog
        fname : str, optional
            function name (a key from fitting functions dict). If
            provided, the dialog will be used to edit an existing function from
            the custom fitting function database
            Default: None

        """
        super().__init__()
        self.fname = None
        self.fdef = None
        self._popt, self._pcov = None, None
        self.setupUi(dialog)
        #        self.customFitButtonBox.rejected.connect(self.cancelbutton)
        self.customFitButtonBox.accepted.connect(self.ok)
        if fname is not None:
            dialog.setWindowTitle('Edit Fit')
            fdef = get_func(strfunc=fname)
            self.customFitName.setText(fname)
            self.customFitDef.setText(fdef)

    def ok(self):
        """
        Reads the line edit asked to the user, if ok button has been pressed

        """
        self.fname = self.customFitName.text()
        self.fdef = self.customFitDef.text()

