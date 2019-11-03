from sys import argv as argv_
from pathlib import Path
from typing import Optional, List, Type
from PyQt5.QtWidgets import QAbstractButton, QStackedWidget, QComboBox, QLineEdit, QTextEdit, \
    QPlainTextEdit, QSpinBox, QDoubleSpinBox, QLabel, QProgressBar, QAbstractSlider


class QWidgetCodeGenerator:
    """
    Holds various attribute names of a PyQt widget object and generates code using them.
    """
    _widget_value_type_name: Optional[str] = None
    _widget_get_value_func_name: Optional[str] = None
    _widget_set_value_func_name: Optional[str] = None
    _widget_get_enabled_func_name: str = 'isEnabled'
    _widget_set_enabled_func_name: str = 'setEnabled'
    _widget_primary_signal_name: Optional[str] = 'valueChanged'

    _template_get_set_widget_value = (
        '    @property\n'
        '    def {object._property_name}(self) -> {object._widget_value_type_name}:\n'
        '        return self.ui.{object._object_name}.{object._widget_get_value_func_name}()\n'
        '\n'
        '    @{object._property_name}.setter\n'
        '    def {object._property_name}(self, value: {object._widget_value_type_name}) -> None:\n'
        '        self.ui.{object._object_name}.{object._widget_set_value_func_name}(value)\n'
    )

    _template_get_set_widget_enabled = (
        '    @property\n'
        '    def {object._property_name}_enabled(self) -> bool:\n'
        '        return self.ui.{object._object_name}.{object._widget_get_enabled_func_name}()\n'
        '\n'
        '    @{object._property_name}_enabled.setter\n'
        '    def {object._property_name}_enabled(self, enabled: bool) -> None:\n'
        '        self.ui.{object._object_name}.{object._widget_set_enabled_func_name}(enabled)\n'
    )

    _template_primary_signal_slot = (
        '    def on_{object._property_name}_{object._widget_primary_signal_name}('
        'self, *args) -> None:\n'
        '        print(\'"on_{object._property_name}_{object._widget_primary_signal_name}" called '
        'with args:\', args)\n'
    )

    _property_templates = (
        _template_get_set_widget_value,
        _template_get_set_widget_enabled,
        _template_primary_signal_slot,
    )

    _template_connect_primary_signal = (
        '        self.ui.{object._object_name}.{object._widget_primary_signal_name}.connect('
        'self.on_{object._property_name}_{object._widget_primary_signal_name})\n'
    )

    _connection_templates = (_template_connect_primary_signal, )




    @classmethod
    def _template_is_generatable(cls, template: str) -> bool:
        """
        Checks that we have all of the info required to generate code.
        """
        template_requirements = {
            cls._template_get_set_widget_value: (
                    cls._widget_value_type_name is not None and
                    cls._widget_get_value_func_name is not None and
                    cls._widget_set_value_func_name is not None
            ),
            cls._template_get_set_widget_enabled: (
                    cls._widget_get_enabled_func_name is not None and
                    cls._widget_set_enabled_func_name
            ),
            cls._template_connect_primary_signal: cls._widget_primary_signal_name is not None,
            cls._template_primary_signal_slot: True,
        }

        return template_requirements[template]

    def __init__(self, object_name: str, object_type: str, property_name: str):
        self._object_name = object_name
        self._object_type = object_type
        self._property_name = property_name

    def generate_code(self, code_type: str) -> str:
        """
        Generate code for the widget.
        """
        code_types = {
            'properties': self._property_templates,
            'connections': self._connection_templates
        }

        valid_templates = []

        for template in code_types[code_type]:
            if self._template_is_generatable(template):
                valid_templates.append(template)

        templates_str = '\n'.join(valid_templates)

        # substitute object tokens in code with actual object
        templates_str = templates_str.format(object=self)

        return templates_str


class QAbstractButtonCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = bool.__name__
    _widget_get_value_func_name = QAbstractButton.isChecked.__name__
    _widget_set_value_func_name = QAbstractButton.setChecked.__name__


class QStackedWidgetCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = int.__name__
    _widget_get_value_func_name = QStackedWidget.currentIndex.__name__
    _widget_set_value_func_name = QStackedWidget.setCurrentIndex.__name__


class QComboBoxCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = int.__name__
    _widget_get_value_func_name = QComboBox.currentIndex.__name__
    _widget_set_value_func_name = QComboBox.setCurrentIndex.__name__


class QLineEditCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = str.__name__
    _widget_get_value_func_name = QLineEdit.text.__name__
    _widget_set_value_func_name = QLineEdit.setText.__name__


class QTextEditCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = str.__name__
    _widget_get_value_func_name = QTextEdit.toPlainText.__name__
    _widget_set_value_func_name = QTextEdit.setText.__name__


class QPlainTextEditCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = str.__name__
    _widget_get_value_func_name = QPlainTextEdit.toPlainText.__name__
    _widget_set_value_func_name = QPlainTextEdit.setPlainText.__name__


class QSpinBoxCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = int.__name__
    _widget_get_value_func_name = QSpinBox.value.__name__
    _widget_set_value_func_name = QSpinBox.setValue.__name__


class QDoubleSpinBoxCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = float.__name__
    _widget_get_value_func_name = QDoubleSpinBox.value.__name__
    _widget_set_value_func_name = QDoubleSpinBox.setValue.__name__


class QLabelCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = str.__name__
    _widget_get_value_func_name = QLabel.text.__name__
    _widget_set_value_func_name = QLabel.setText.__name__


class QProgressBarCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = int.__name__
    _widget_get_value_func_name = QProgressBar.value.__name__
    _widget_set_value_func_name = QProgressBar.setValue.__name__


class QAbstractSliderCodeGenerator(QWidgetCodeGenerator):
    _widget_value_type_name = int.__name__
    _widget_get_value_func_name = QAbstractSlider.value.__name__
    _widget_set_value_func_name = QAbstractSlider.setValue.__name__


def _get_code_generator(object_name: str) -> 'QWidgetCodeGenerator':
    """
    Get the correct code generation using the widget's objectName.
    """
    generator_types = {
        'widget': QWidgetCodeGenerator,
        'groupBox': QAbstractButtonCodeGenerator,
        'action': QAbstractButtonCodeGenerator,
        'pushButton': QAbstractButtonCodeGenerator,
        'toolButton': QAbstractButtonCodeGenerator,
        'radioButton': QAbstractButtonCodeGenerator,
        'checkBox': QAbstractButtonCodeGenerator,
        'stackedWidget': QStackedWidgetCodeGenerator,
        'comboBox': QComboBoxCodeGenerator,
        'lineEdit': QLineEditCodeGenerator,
        'textEdit': QTextEditCodeGenerator,
        'plainTextEdit': QPlainTextEditCodeGenerator,
        'spinBox': QSpinBoxCodeGenerator,
        'doubleSpinBox': QDoubleSpinBoxCodeGenerator,
        'label': QLabelCodeGenerator,
        'progressBar': QProgressBarCodeGenerator,
        'verticalSlider': QAbstractSliderCodeGenerator,
        'horizontalSlider': QAbstractSliderCodeGenerator,
    }

    object_type, property_name = object_name.split('_', maxsplit=1)
    try:
        code_generator = generator_types[object_type]
    except IndexError:
        raise ValueError('Unknown object type')
    return code_generator(object_name, object_type, property_name)


def process_file(input_file: str, output_file: Optional[str] = None) -> str:
    """
    Take a text file (e.g. main_ui.txt) that contains names of PyQt objects (e.g. spinBox_distance)
    and generates an output file (e.g. main_ui_helper.py) in the same directory that defines a class
    with helper properties for the PyQt object.
    """

    input_path = Path(input_file)

    if output_file is None:
        # converts "some_filename.ext" to "some_filename_helper.py"
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

    for code_type in ('properties', 'connections'):

        for object_name in object_names:
            if object_name and not object_name.startswith('#') and '_' in object_name:
                try:
                    code_generator = _get_code_generator(object_name)
                # ignore unknown object types
                except ValueError:
                    print(f'Unknown widget type for {object_name}.')
                else:
                    code = code_generator.generate_code(code_type)
                    if code:
                        output.append(code)
                        worked += 1





    # class name is file name converted to CamelCase and with "Helper" appended
    class_name = ''.join(word.capitalize() for word in input_path.stem.split('_'))

    # save output file
    with output_path.open('w') as f:
        f.write('# This file was autogenerated using pyqt-helper - do not edit!\n\n\n')
        f.write(f'class {class_name}Helper:\n\n')
        f.write(''.join(output))

    print(f'Successfully generated code for {worked} objects.')
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
    main(argv_)
