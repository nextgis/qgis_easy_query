import os
from os import path

from qgis.PyQt.QtCore import QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import QgsApplication

from .easy_query_dialog import EasyQueryDialog

from . import about_dialog

_current_path = os.path.abspath(os.path.dirname(__file__))


class QGISEasyQuery:
    """QGIS Plugin Implementation."""

    keys_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "resources", "keys.json")
    )

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = "NextGIS Easy Query"

        self.pluginIsActive = False

        self._translator = None
        self.__init_translator()

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        _current_path = os.path.abspath(os.path.dirname(__file__))

        self.toolbar = self.iface.addToolBar("NextGIS EasyQuery")
        self.toolbar.setObjectName("NextGIS EasyQuery")

        easy_query_icon_path = os.path.abspath(
            os.path.join(_current_path, "icon.png")
        )
        easy_query_icon = QIcon(easy_query_icon_path)

        easy_query_action = QAction(
            easy_query_icon, "NextGIS EasyQuery", self.iface.mainWindow()
        )
        easy_query_action.triggered.connect(self.easy_query)
        easy_query_action.setEnabled(True)
        easy_query_action.setStatusTip("NextGIS EasyQuery")
        easy_query_action.setWhatsThis("NextGIS EasyQuery")
        self.toolbar.addAction(easy_query_action)
        self.iface.addPluginToVectorMenu(self.menu, easy_query_action)
        self.actions.append(easy_query_action)

        action_about = QAction(
            self.tr("About plugin…"), self.iface.mainWindow()
        )
        action_about.triggered.connect(self.about)
        self.iface.addPluginToVectorMenu(self.menu, action_about)
        self.actions.append(action_about)

    # --------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginVectorMenu("Easy Query", action)
            action.deleteLater()

        self.actions = []
        self.toolbar.hide()
        self.toolbar.deleteLater()
        self.toolbar = None

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

        add_translator(
            path.join(_current_path, "i18n", f"qgis_easy_query_{locale}.qm")
        )

    def about(self):
        dialog = about_dialog.AboutDialog(os.path.basename(self.plugin_dir))
        dialog.exec_()

    def tr(self, message):
        return QCoreApplication.translate(__class__.__name__, message)
