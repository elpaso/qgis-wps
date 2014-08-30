# -*- coding: utf-8 -*-
"""
***************************************************************************
Name			 	 : WPS
Description          : WPS
Date                 : 11/Aug/2014
copyright            : (C) 2014 by ItOpen
email                : info@itopen.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtCore, QtGui
from Ui_WPS import Ui_WPS
# create the dialog

class WPSDialog(QtGui.QDialog, Ui_WPS ):

    MIMES = ['text/plain', 'text/html', 'application/xml']

    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.mimeComboBox.addItems(self.MIMES)

    @QtCore.pyqtSlot()
    def on_clearButton_clicked(self):
        self.code.setPlainText('')

