from sys import argv
from pathlib import Path
from typing import Optional, List
from PyQt5.QtWidgets import QAbstractButton, QStackedWidget, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, \
    QSpinBox, QDoubleSpinBox, QLabel, QProgressBar, QGroupBox, QAbstractSlider


class ObjectCodeGen:
    """
    Holds various attribute names of a PyQt widget object, and generates getter and setter code.
    """
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
    def from_object_name(object_name: str) -> 'ObjectCodeGen':

        types = {
            'groupBox': QWidgetCodeGen,
            'action': QWidgetCodeGen,
            'pushButton': QWidgetCodeGen,
            'toolButton': QWidgetCodeGen,
            'radioButton': QWidgetCodeGen,
            'checkBox': QWidgetCodeGen,
            'stackedWidget': QStackedWidgetCodeGen,
            'comboBox': QComboBoxCodeGen,
            'lineEdit': QLineEditCodeGen,
            'textEdit': QTextEditCodeGen,
            'plainTextEdit': QPlainTextEditCodeGen,
            'spinBox': QSpinBoxCodeGen,
            'doubleSpinBox': QDoubleSpinBoxCodeGen,
            'label': QLabelCodeGen,
            'progressBar': QProgressBarCodeGen,
            'verticalSlider': QAbstractSliderCodeGen,
            'horizontalSlider': QAbstractSliderCodeGen,
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


class QWidgetCodeGen(ObjectCodeGen):
    _data_type = bool.__name__
    _func_get = QAbstractButton.isChecked.__name__
    _func_set = QAbstractButton.setChecked.__name__


class QStackedWidgetCodeGen(ObjectCodeGen):
    _data_type = int.__name__
    _func_get = QStackedWidget.currentIndex.__name__
    _func_set = QStackedWidget.setCurrentIndex.__name__


class QComboBoxCodeGen(ObjectCodeGen):
    _data_type = int.__name__
    _func_get = QComboBox.currentIndex.__name__
    _func_set = QComboBox.setCurrentIndex.__name__


class QLineEditCodeGen(ObjectCodeGen):
    _data_type = str.__name__
    _func_get = QLineEdit.text.__name__
    _func_set = QLineEdit.setText.__name__


class QTextEditCodeGen(ObjectCodeGen):
    _data_type = str.__name__
    _func_get = QTextEdit.toPlainText.__name__
    _func_set = QTextEdit.setText.__name__


class QPlainTextEditCodeGen(ObjectCodeGen):
    _data_type = str.__name__
    _func_get = QPlainTextEdit.toPlainText.__name__
    _func_set = QPlainTextEdit.setPlainText.__name__


class QSpinBoxCodeGen(ObjectCodeGen):
    _data_type = int.__name__
    _func_get = QSpinBox.value.__name__
    _func_set = QSpinBox.setValue.__name__


class QDoubleSpinBoxCodeGen(ObjectCodeGen):
    _data_type = float.__name__
    _func_get = QDoubleSpinBox.value.__name__
    _func_set = QDoubleSpinBox.setValue.__name__


class QLabelCodeGen(ObjectCodeGen):
    _data_type = str.__name__
    _func_get = QLabel.text.__name__
    _func_set = QLabel.setText.__name__


class QProgressBarCodeGen(ObjectCodeGen):
    _data_type = int.__name__
    _func_get = QProgressBar.value.__name__
    _func_set = QProgressBar.setValue.__name__


class QAbstractSliderCodeGen(ObjectCodeGen):
    _data_type = int.__name__
    _func_get = QAbstractSlider.value.__name__
    _func_set = QAbstractSlider.setValue.__name__


def process_file(input_file: str, output_file: Optional[str] = None) -> str:
    """
    Take a text file (e.g. main_ui.txt) that contains names of PyQt objects (e.g. spinBox_distance)
    and generates an output file (e.g. main_ui_helper.py) in the same directory that defines a class
    with helper properties for the PyQt object.
    """

    input_path = Path(input_file)

    if output_file is None:
        # replaces ".txt" with "_helper.py"
        output_path = Path(input_path.with_name(f'{input_path.stem}_helper')).with_suffix('.py')
    else:
        output_path = Path(output_file)

    # get lines from file
    object_names = []
    try:
        with input_path.open('r') as f:
            for line in f:
                object_names.append(line.strip())
    except FileNotFoundError:
        print(f'File "{input_path}" not found.')
        exit(1)

    # process line if valid
    worked = 0
    output = []
    for object_name in object_names:
        if object_name and not object_name.startswith('#') and '_' in object_name:
            try:
                output.append(ObjectCodeGen.from_object_name(object_name).generate_code())
                worked += 1
            except KeyError:
                # ignore invalid lines
                print(f'Unknown widget type for {object_name}.')

    # class name is file name converted to CamelCase and with "Helper" appended
    class_name = ''.join(word.capitalize() for word in input_path.stem.split('_'))

    # save output file
    with output_path.open('w') as f:
        f.write('# This file was autogenerated using pyqt_helper.py, do NOT edit!\n\n\n')
        f.write(f'class {class_name}Helper:\n\n')
        f.write('\n'.join(output))

    print(f'Successfully processed {worked} object names.')
    return str(output_path)


def main(argv: List[str]) -> None:

    # validate inputs
    args = argv[1:]
    if len(args) not in (1, 2):
        args_str = ", ".join([f'"{x}"' for x in args])
        raise TypeError(f'Expected 1 or 2 arguments but got {len(args)} ({args_str}).')

    # get/generate input and output files
    input_file = argv[1]
    try:
        output_file = argv[2]
    except IndexError:
        output_file = None

    process_file(input_file, output_file)


if __name__ == '__main__':
    main(argv)
