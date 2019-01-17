from typing import Optional
from PyQt5.QtWidgets import QAbstractButton, QStackedWidget, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, \
    QSpinBox, QDoubleSpinBox, QLabel, QProgressBar


class ObjectStrings:
    """ Holds various attribute names of a widget object, and generates getter and setter code. """
    _data_type = None
    _func_get = None
    _func_set = None

    _get_value_code = (
        '    @property\n'
        '    def {x._property_name}(self) -> {x._data_type}:\n'
        '        return self.ui.{x._object_name}.{x._func_get}()\n')

    _set_value_code = (
        '    @{x._property_name}.setter\n'
        '    def {x._property_name}(self, value: {x._data_type}) -> None:\n'
        '        self.ui.{x._object_name}.{x._func_set}(value)\n')

    _get_enabled_code = (
        '    @property\n'
        '    def {x._property_name}_enabled(self) -> bool:\n'
        '        return self.ui.{x._object_name}.isEnabled()\n')

    _set_enabled_code = (
        '    @{x._property_name}_enabled.setter\n'
        '    def {x._property_name}_enabled(self, enabled: bool) -> None:\n'
        '        self.ui.{x._object_name}.setEnabled(enabled)\n')

    @staticmethod
    def from_object_name(object_name: str) -> 'ObjectStrings':

        types = {
            'pushButton': QAbstractButtonStrings,
            'toolButton': QAbstractButtonStrings,
            'radioButton': QAbstractButtonStrings,
            'checkBox': QAbstractButtonStrings,
            'stackedWidget': QStackedWidgetStrings,
            'comboBox': QComboBoxStrings,
            'lineEdit': QLineEditStrings,
            'textEdit': QTextEditStrings,
            'plainTextEdit': QPlainTextEditStrings,
            'spinBox': QSpinBoxStrings,
            'doubleSpinBox': QDoubleSpinBoxStrings,
            'label': QLabelStrings,
            'progressBar': QProgressBarStrings,
        }

        object_type, property_name = object_name.split('_', maxsplit=1)
        object_type_strings = types[object_type]
        return object_type_strings(object_name, object_type, property_name)

    def __init__(self, object_name: str, object_type: str, property_name: str):
        self._object_name = object_name
        self._object_type = object_type
        self._property_name = property_name

    def generate_code(self,
                      get_value_code: Optional[bool] = True,
                      set_value_code: Optional[bool] = True,
                      get_enabled_code: Optional[bool] = True,
                      set_enabled_code: Optional[bool] = True,
                      ) -> str:

        codes = []
        if get_value_code:
            codes.append(self._get_value_code)
        if set_value_code:
            codes.append(self._set_value_code)
        if get_enabled_code:
            codes.append(self._get_enabled_code)
        if set_enabled_code:
            codes.append(self._set_enabled_code)

        all_codes = '\n'.join(codes)

        return all_codes.format(x=self)


class QAbstractButtonStrings(ObjectStrings):
    _data_type = bool.__name__
    _func_get = QAbstractButton.isChecked.__name__
    _func_set = QAbstractButton.setChecked.__name__


class QStackedWidgetStrings(ObjectStrings):
    _data_type = int.__name__
    _func_get = QStackedWidget.currentIndex.__name__
    _func_set = QStackedWidget.setCurrentIndex.__name__


class QComboBoxStrings(ObjectStrings):
    _data_type = int.__name__
    _func_get = QComboBox.currentIndex.__name__
    _func_set = QComboBox.setCurrentIndex.__name__


class QLineEditStrings(ObjectStrings):
    _data_type = str.__name__
    _func_get = QLineEdit.text.__name__
    _func_set = QLineEdit.setText.__name__


class QTextEditStrings(ObjectStrings):
    _data_type = str.__name__
    _func_get = QTextEdit.toPlainText.__name__
    _func_set = QTextEdit.setText.__name__


class QPlainTextEditStrings(ObjectStrings):
    _data_type = str.__name__
    _func_get = QPlainTextEdit.toPlainText.__name__
    _func_set = QPlainTextEdit.setPlainText.__name__


class QSpinBoxStrings(ObjectStrings):
    _data_type = int.__name__
    _func_get = QSpinBox.value.__name__
    _func_set = QSpinBox.setValue.__name__


class QDoubleSpinBoxStrings(ObjectStrings):
    _data_type = float.__name__
    _func_get = QDoubleSpinBox.value.__name__
    _func_set = QDoubleSpinBox.setValue.__name__


class QLabelStrings(ObjectStrings):
    _data_type = str.__name__
    _func_get = QLabel.text.__name__
    _func_set = QLabel.setText.__name__


class QProgressBarStrings(ObjectStrings):
    _data_type = int.__name__
    _func_get = QProgressBar.value.__name__
    _func_set = QProgressBar.setValue.__name__


if __name__ == '__main__':

    tests = (
        'pushButton_connected',
        'pushButton_running',
        'spinBox_distance_mm',
    )

    for t in tests:
        x = ObjectStrings.from_object_name(t)
        print(x.generate_code())
