import os

from qgis.PyQt.QtCore import QSettings, QUrl, QLocale
from qgis.PyQt.QtGui import QDesktopServices, QTextDocument, QPixmap
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.PyQt import uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'qgis_easy_query_about.ui'))

class AboutDialog(QDialog, FORM_CLASS):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.btnHelp = self.buttonBox.button(QDialogButtonBox.Help)

        doc = QTextDocument()
        doc.setHtml(self.getAboutText())
        self.textBrowser.setDocument(doc)
        self.textBrowser.setOpenExternalLinks(True)

        self.buttonBox.helpRequested.connect(self.openHelp)

    def reject(self):
        QDialog.reject(self)

    def openHelp(self):
        overrideLocale = QSettings().value('locale/overrideFlag', False, type=bool)
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value('locale/userLocale', '')

        localeShortName = localeFullName[0:2]
        if localeShortName in ['ru', 'uk']:
            QDesktopServices.openUrl(QUrl('https://nextgis.ru'))
        else:
            QDesktopServices.openUrl(QUrl('http://nextgis.com'))

    def getAboutText(self):
        return self.tr('<p>Easy to use queries.</p>'
            '<p>EasyQuery is an alternative for Select features using expression tool. The idea is to provide less comprehensive, but more intuitive way to run simple queries.</p>'
            '<p><strong>Developers</strong>: '
            '<a href="http://nextgis.org">NextGIS</a></p>'
            '<p><strong>Homepage</strong>: '
            '<a href="https://github.com/nextgis/qgis_easy_query">'
            'https://github.com/nextgis/qgis_easy_query</a></p>'
            '<p>Please report bugs at '
            '<a href="https://github.com/nextgis/qgis_easy_query/issues">'
            'bugtracker</a></p>'
            '<p>Other helpful services by NextGIS:</p>'
            '<ul><li><b>Convenient up-to-date data extracts for any place in the world: <a href="https://data.nextgis.com">https://data.nextgis.com</a></b></li>'
            '<li><b>Fully featured Web GIS service: <a href="https://nextgis.com/nextgis-com/plans">https://nextgis.com/nextgis-com/plans</a></b></li></ul>'
            )