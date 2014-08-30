# -*- coding: utf-8 -*-

"""
***************************************************************************
    WPS.py
    ---------------------
    Date                 : August 2014
    Copyright            : (C) 2014 by Alessandro Pasotti
    Email                : apasotti at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alessandro Pasotti'
__date__ = 'August 2014'
__copyright__ = '(C) 2014, Alessandro Pasotti'

import pickle
import os
import sys
import types

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from WPSDialog import WPSDialog


# PyWPS prints log messages on stderr..., save writers and restore
# defauls
_stderr = sys.stderr
_stdout = sys.stdout


sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'PyWPS'))
import pywps


from processing.core.Processing import Processing
from processing.tools.general import *

def QGISProcessFactory(alg_name):
    """This is the bridge between SEXTANTE and PyWPS:
    it creates PyWPS processes based on SEXTANTE alg name"""
    from pywps.Process import WPSProcess
    from new import classobj
    import types
    from processing.core.Processing import Processing
    # Sanitize name
    class_name = alg_name.replace(':', '_')
    alg = Processing.getAlgorithm(alg_name)

    def process_init(self):
        # Automatically init the process attributes
        WPSProcess.__init__(self,
            identifier=alg_name, # must be same, as filename
            title=alg_name,
            version = "0.1",
            storeSupported = "true",
            statusSupported = "true",
            abstract= '<![CDATA[' + str(alg) + ']]>',
            grassLocation=False)
        self.alg = alg
        # Add I/O
        i = 1
        for parm in alg.parameters:
            if getattr(parm, 'optional', False):
                minOccurs = 0
            else:
                minOccurs = 1
            # TODO: create "LiteralValue", "ComplexValue" or "BoundingBoxValue"
            # this can be done checking the class:
            # parm.__class__, one of
            # ['Parameter', 'ParameterBoolean', 'ParameterCrs', 'ParameterDataObject', 'ParameterExtent', 'ParameterFile', 'ParameterFixedTable', 'ParameterMultipleInput', 'ParameterNumber', 'ParameterRange', 'ParameterRaster', 'ParameterSelection', 'ParameterString', 'ParameterTable','ParameterTableField', 'ParameterVector']
            if parm.__class__.__name__ == 'ParameterBoolean':
                type = types.BooleanType
            else:
                type = types.StringType
            self._inputs['Input%s' % i] = self.addLiteralInput(parm.name, parm.description,
                                            minOccurs=minOccurs,
                                            type=type,
                                            default=getattr(parm, 'default', None))
            i += 1

        i = 1
        for parm in alg.outputs:
            self._outputs['Output%s' % i] = self.addLiteralOutput(identifier = parm.name,
                                            title = parm.description)
            i += 1

        for k in self._inputs:
             setattr(self, k, self._inputs[k])

        for k in self._outputs:
             setattr(self, k, self._outputs[k])



    def execute(self):
        # Run alg with params
        # TODO: get args
        args = {}
        for k in self._inputs:
            v = getattr(self, k)
            args[v.identifier] = v.getValue()
        # Adds None for output parameter(s)
        for k in self._outputs:
            v = getattr(self, k)
            args[v.identifier] = None

        #processing.runalg("grass:v.hull","/home/ale/Documenti/maps/regioni_semplificato_4326.shp",False,"6.6268611901,18.5188598654,35.4930324712,47.0862707258",-1,0.0001,0,None)
        from processing import runalg
        alg = Processing.runAlgorithm(self.alg, None, args)
        if alg is not None:
            result = alg.getOutputValuesAsDictionary()
            for k in self._outputs:
                v = getattr(self, k)
                args[v.identifier] = result.get(k, None)
        return


    new_class = classobj('%sProcess' % class_name, (WPSProcess, ), {
        '__init__' :  process_init,
        'execute' : execute,
        'params' : [],
        'alg' : alg,
        '_inputs' : {},
        '_outputs' : {},
    })
    return new_class



class WPS:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()

    def initGui(self):
        # Create action that will start plugin
        self.action = QAction(QIcon(":/plugins/"), "&WPS", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("activated()"), self.config)
        # Add toolbar button and menu item
        self.iface.addPluginToMenu("WPS", self.action)

    # change settings
    def config(self):
        """TO BE IMPLEMENTED"""
        QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('WPS', "WPS"), QCoreApplication.translate('WPS', "CONFIGURATION: TO BE IMPLEMENTED"))
        return


        # create and show the dialog
        dlg = WPSDialog()
        # Get settings
        settings = WPS.getSettings()
        dlg.mimeComboBox.setCurrentIndex(dlg.MIMES.index(settings['mime']))
        dlg.code.setPlainText(settings['code'])
        # show the dialog
        dlg.show()
        result = dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # save settings
            WPS.storeSettings({
                'mime': str(dlg.mimeComboBox.currentText()),
                'code': str(dlg.code.toPlainText()),
            })


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("WPS",self.action)


    @staticmethod
    def _getSettingsPath():
        dirname = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dirname, 'wps.pkl')

    @staticmethod
    def storeSettings(settings):
        # Stores configuration locally
        output = open(WPS._getSettingsPath(), 'wb')
        config = pickle.dump(settings, output)
        output.close()

    @staticmethod
    def getSettings():
        # Store configuration locally
        try:
            output = open(WPS._getSettingsPath(), 'rb')
            # Pickle dictionary using protocol 0.
            settings = pickle.load(output)
            output.close()
        except:
            settings = {
                'mime' : 'text/plain',
                'code' : ''
            }
        return settings


    ############################################################################
    #
    # Server processing
    #

    @staticmethod
    def _initServer(project_path, parameters):
        """Initalize server"""
        try:
            WPS.methods
        except:
            Processing.initialize()
            WPS.methods = Processing.algs
            WPS.processes = []
            for i in WPS.methods:
                for m in WPS.methods[i]:
                    WPS.processes.append(QGISProcessFactory(m))

        # TODO: handle POST, SOAP etc...
        WPS.wps = pywps.Pywps('GET')
        WPS.request = '&'.join(["%s=%s" % (k, parameters[k]) for k in parameters])
        pywps.config.setConfigValue("server","outputPath", '/tmp')


    @staticmethod
    def _pywps_proxy(project_path, parameters):
        WPS._initServer(project_path, parameters)
        WPS.wps.parseRequest(WPS.request)
        response = WPS.wps.performRequest(processes=WPS.processes)
        print response
        return 'application/xml'

    @staticmethod
    def GetCapabilities(project_path, parameters):
        return WPS._pywps_proxy(project_path, parameters)

    @staticmethod
    def DescribeProcess(project_path, parameters):
        return WPS._pywps_proxy(project_path, parameters)

    @staticmethod
    def Execute(project_path, parameters):
        return WPS._pywps_proxy(project_path, parameters)


if __name__ == "__main__":
    pass
