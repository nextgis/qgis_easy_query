# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
import json

import os, sys

from .easy_query_dialog import EasyQueryDialog

_current_path = os.path.abspath(os.path.dirname(__file__))


class QGISEasyQuery():
    """QGIS Plugin Implementation."""

    keys_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'keys.json'))

    def __init__(self, iface):

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = u'Easy Query'

        self.toolbar = self.iface.addToolBar(u'Easy Query')
        self.toolbar.setObjectName(u'Easy Query')

        self.pluginIsActive = False


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # Import EGRN
        _current_path = os.path.abspath(os.path.dirname(__file__))

        
        easy_query_icon_path = os.path.abspath(os.path.join(_current_path,'icon.png'))
        easy_query_icon = QIcon(easy_query_icon_path)

        easy_query_action = QAction(easy_query_icon, u'Простые выборки', self.iface.mainWindow())
        easy_query_action.triggered.connect(self.easy_query)
        easy_query_action.setEnabled(True)
        easy_query_action.setStatusTip(u'Простые выборки')
        easy_query_action.setWhatsThis(u'Простые выборки')
        self.toolbar.addAction(easy_query_action)
        self.iface.addPluginToVectorMenu(self.menu, easy_query_action)
        self.actions.append(easy_query_action)

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginVectorMenu(
                u'Easy Query',
                action)
            self.iface.removeToolBarIcon(action)

        del self.toolbar

    #--------------------------------------------------------------------------

    def easy_query(self):

        if not self.pluginIsActive:
            self.dlg = EasyQueryDialog()
            self.dlg.show()
            self.pluginIsActive = True
        else:
            self.dlg.show()