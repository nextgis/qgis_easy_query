import os
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *
import processing
import numpy as np

FORM_CLASS, _ = uic.loadUiType(os.path.abspath(os.path.join(os.path.dirname(__file__), 'qgis_easy_query.ui')))

class EasyQueryDialog(QWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    plugin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    def __init__(self, parent=None):
        # init dock
        super(EasyQueryDialog, self).__init__(parent)
        self.setupUi(self)
        self.clear_table()

        self.addConditionButton.clicked.connect(self.add_condition)
        self.deleteConditionButton.clicked.connect(self.delete_condition)
        self.runButton.clicked.connect(self.run)
        self.closeButton.clicked.connect(self.cancel)

        self.LayerCombobox.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.LayerCombobox.currentIndexChanged.connect(self.clear_table)

        header = self.conditionsQueryTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

    def create_operator_combobox(self):
        operator_combobox = QComboBox()
        operator_combobox.addItems(['=','!=','>','<','>=','<='])
        operator_combobox.setCurrentIndex(0)
        return operator_combobox

    def clear_table(self):
        self.conditionsQueryTable.setRowCount(0)

    def add_condition(self):
        if not self.LayerCombobox.currentText():
            QMessageBox.information(None, u'Внимание!',
                                    u'Сначала необходимо выбрать слой')
            return

        row_count = self.conditionsQueryTable.rowCount()
        self.conditionsQueryTable.setRowCount(row_count+1)
        new_row_id = row_count

        current_fields_comboBox = QgsFieldComboBox()
        current_fields_comboBox.setLayer(self.LayerCombobox.currentLayer())
        self.conditionsQueryTable.setCellWidget(new_row_id, 0, current_fields_comboBox)

        current_operator_combobox = self.create_operator_combobox()
        self.conditionsQueryTable.setCellWidget(new_row_id, 1, current_operator_combobox)

        current_values_combobox = QComboBox()
        current_values_combobox.setEditable(True)
        self.conditionsQueryTable.setCellWidget(new_row_id, 2, current_values_combobox)

        current_fields_comboBox.currentIndexChanged.connect(
            lambda: self.field_combobox_changed(current_fields_comboBox, current_values_combobox))

        pass

    def delete_condition(self):
        rows = sorted(set(index.row() for index in self.conditionsQueryTable.selectedIndexes()), reverse=True)
        for row in rows:
            self.conditionsQueryTable.removeRow(row)

    def field_combobox_changed(self, current_fields_comboBox, current_values_combobox):
        current_values_combobox.clear()
        try:
            fields = current_fields_comboBox.layer().fields()
        except:
            return
        for field in fields:
            if field.name() == current_fields_comboBox.currentField():
                current_type = field.typeName()

        idx = fields.indexFromName(current_fields_comboBox.currentField())

        if current_type.lower() in ['string', 'text', 'char', 'varchar', 'datetime']:
            text_mode = True
            numerical_mode = False
        elif current_type.lower() in ['integer', 'integer32', 'integer64', 'real', 'double', 'float']:
            text_mode = False
            numerical_mode = True
        else:
            text_mode = False
            numerical_mode = False

        if (text_mode == False) and (numerical_mode == False):
            current_values_combobox.clear()

        if text_mode == True:
            unique_values_raw = list(current_fields_comboBox.layer().uniqueValues(idx))
            unique_values = []
            for value in unique_values_raw:
                if not type(value) is str:
                    continue
                else:
                    unique_values.append(value)
            current_values_combobox.addItems(unique_values)

        if numerical_mode == True:
            all_values = []
            for feature in current_fields_comboBox.layer().getFeatures():
                all_values.append(feature[current_fields_comboBox.currentField()])

            try:
                val_min = str(np.nanmin(all_values))
                val_max = str(np.nanmax(all_values))
                val_25 = str(np.nanpercentile(all_values, 25))
                val_50 = str(np.nanpercentile(all_values, 50))
                val_75 = str(np.nanpercentile(all_values, 75))
                current_values_combobox.addItems([val_min, val_25, val_50, val_75, val_max])
            except:
                pass

    def run(self):
        if not self.LayerCombobox.currentText():
            QMessageBox.information(None, u'Внимание!',
                                    u'Необходимо выбрать слой')
            return

        row_count = self.conditionsQueryTable.rowCount()
        if row_count == 0:
            QMessageBox.information(None, u'Внимание!',
                                    u'Не задано ни одного условия')

        conditions = []
        for i in range(0,row_count):
            if not self.conditionsQueryTable.cellWidget(i,0).currentText():
                QMessageBox.information(None, u'Внимание!',
                                        u'У всех условий должно быть выбрано поле')
                return

            if not self.conditionsQueryTable.cellWidget(i,2).currentText():
                QMessageBox.information(None, u'Внимание!',
                                        u'У всех условий должно быть выбрано значение')
                return

            current_field = self.conditionsQueryTable.cellWidget(i,0).currentText()
            fields = self.conditionsQueryTable.cellWidget(i,0).layer().fields()
            for field in fields:
                if field.name() == self.conditionsQueryTable.cellWidget(i,0).currentField():
                    current_type = field.typeName()

            current_operator = self.conditionsQueryTable.cellWidget(i,1).currentText()
            current_value = self.conditionsQueryTable.cellWidget(i,2).currentText()
            if current_type.lower() in ['string', 'text', 'char', 'varchar']:
                current_value = '\'%s\'' % current_value

            current_condition = '(\"%s\" %s %s)' % (current_field, current_operator, current_value)
            conditions.append(current_condition)

        if self.conditionModeCombobox.currentIndex() == 0:
            # AND
            general_condition = ' AND '.join(conditions)
        else:
            # OR
            general_condition = ' OR '.join(conditions)

        if self.resultCombobox.currentIndex() == 0:
            # select
            self.LayerCombobox.currentLayer().selectByExpression(general_condition)
        elif self.resultCombobox.currentIndex() == 1:
            # new layer
            res = processing.runAndLoadResults("native:extractbyexpression",
                           {'INPUT': self.LayerCombobox.currentLayer(),
                            'EXPRESSION': general_condition,
                            'OUTPUT': 'TEMPORARY_OUTPUT'})

    def cancel(self):
        self.close()