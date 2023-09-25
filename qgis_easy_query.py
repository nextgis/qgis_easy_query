# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.core import QgsApplication
from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QAction
import json

import os, sys

from .easy_query_dialog import EasyQueryDialog

_current_path = os.path.abspath(os.path.dirname(__file__))
from os import path
from . import about_dialog


class QGISEasyQuery():
    """QGIS Plugin Implementation."""

    keys_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', 'keys.json'))

    def __init__(self, iface):
        self.plugin_dir = path.dirname(__file__)
        self._translator = None
        self.__init_translator()
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = u'NextGIS Easy Query'

        self.toolbar = self.iface.addToolBar(u'NextGIS EasyQuery')
        self.toolbar.setObjectName(u'NextGIS EasyQuery')

        self.pluginIsActive = False

        _current_path = os.path.abspath(os.path.dirname(__file__))

        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        localeFullName = QSettings().value('locale/userLocale', '')
        translationPath = os.path.join(_current_path, 'i18n', 'qgis_easy_query_' + localeFullName + '.qm')

        self.localePath = translationPath
        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        _current_path = os.path.abspath(os.path.dirname(__file__))

        easy_query_icon_path = os.path.abspath(os.path.join(_current_path, 'icon.png'))
        easy_query_icon = QIcon(easy_query_icon_path)

        easy_query_action = QAction(easy_query_icon, u'NextGIS EasyQuery', self.iface.mainWindow())
        easy_query_action.triggered.connect(self.easy_query)
        easy_query_action.setEnabled(True)
        easy_query_action.setStatusTip(u'NextGIS EasyQuery')
        easy_query_action.setWhatsThis(u'NextGIS EasyQuery')

        action_about = QAction(self.tr('About'), self.iface.mainWindow())
        action_about.triggered.connect(self.about)
        self.toolbar.addAction(easy_query_action)
        self.iface.addPluginToVectorMenu(self.menu, easy_query_action)
        self.iface.addPluginToVectorMenu(self.menu, action_about)
        self.actions.append(easy_query_action)
        self.actions.append(action_about)

    # --------------------------------------------------------------------------

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
            action.deleteLater()

        del self.toolbar

    # --------------------------------------------------------------------------

    def easy_query(self):

        if not self.pluginIsActive:
            self.dlg = EasyQueryDialog()
            self.dlg.show()
            self.pluginIsActive = True
        else:
            self.dlg.show()

    def __init_translator(self):
        # initialize locale
        locale = QgsApplication.instance().locale()

        def add_translator(locale_path):
            if not path.exists(locale_path):
                return
            translator = QTranslator()
            translator.load(locale_path)
            QCoreApplication.installTranslator(translator)
            self._translator = translator  # Should be kept in memory

        add_translator(path.join(
            self.plugin_dir, 'i18n',
            'qgis_easy_query_{}.qm'.format(locale)
        ))

    def about(self):
        dialog = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec_()

    def tr(self, message):
        return QCoreApplication.translate(__class__.__name__, message)
