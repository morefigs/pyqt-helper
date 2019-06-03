from sys import argv as argv_
from pathlib import Path
from typing import Optional, List, Type
from PyQt5.QtWidgets import QAbstractButton, QStackedWidget, QComboBox, QLineEdit, QTextEdit,\
    QPlainTextEdit, QSpinBox, QDoubleSpinBox, QLabel, QProgressBar, QAbstractSlider


class QWidgetCodeGenerator:
    """
    Holds various attribute names of a PyQt widget object and generates code using them.
    """
    _name_value_type: Optional[str] = None
    _name_get_value_func: Optional[str] = None
    _name_set_value_func: Optional[str] = None
    _name_get_enabled_func: str = 'isEnabled'
    _name_set_enabled_func: str = 'setEnabled'

    _template_get_value = (
        '    @property\n'
        '    def {object._property_name}(self) -> {object._name_value_type}:\n'
        '        return self.ui.{object._object_name}.{object._name_get_value_func}()\n'
    )

    _template_set_value = (
        '    @{object._property_name}.setter\n'
        '    def {object._property_name}(self, value: {object._name_value_type}) -> None:\n'
        '        self.ui.{object._object_name}.{object._name_set_value_func}(value)\n'
    )

    _template_get_enabled = (
        '    @property\n'
        '    def {object._property_name}_enabled(self) -> bool:\n'
        '        return self.ui.{object._object_name}.{object._name_get_enabled_func}()\n'
    )

    _template_set_enabled = (
        '    @{object._property_name}_enabled.setter\n'
        '    def {object._property_name}_enabled(self, enabled: bool) -> None:\n'
        '        self.ui.{object._object_name}.{object._name_set_enabled_func}(enabled)\n'
    )

    _all_templates = (
        _template_get_value,
        _template_set_value,
        _template_get_enabled,
        _template_set_enabled,
    )

    @classmethod
    def _template_generatable(cls, template: str) -> bool:
        """
        Returns whether the class has the required info to generate code for a specified code
        template string.
        """
        get_set_value_requires = (cls._name_value_type is not None and
                                  cls._name_get_value_func is not None and
                                  cls._name_set_value_func is not None)
        get_set_enable_requires = (cls._name_get_enabled_func is not None and
                                   cls._name_set_enabled_func)

        requirements = {
            cls._template_get_value: get_set_value_requires,
            cls._template_set_value: get_set_value_requires,
            cls._template_get_enabled: get_set_enable_requires,
            cls._template_set_enabled: get_set_enable_requires,
        }

        return requirements[template]

    def __init__(self, object_name: str, object_type: str, property_name: str):
        self._object_name = object_name
        self._object_type = object_type
        self._property_name = property_name

    def generate_code(self) -> str:
        """
        Generate code for the widget.
        """
        valid_templates = []

        for template in self._all_templates:
            if self._template_generatable(template):
                valid_templates.append(template)

        templates_str = '\n'.join(valid_templates)

        # substitute object tokens in code with actual object
        templates_str = templates_str.format(object=self)

        return templates_str


class QAbstractButtonCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = bool.__name__
    _name_get_value_func = QAbstractButton.isChecked.__name__
    _name_set_value_func = QAbstractButton.setChecked.__name__


class QStackedWidgetCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = int.__name__
    _name_get_value_func = QStackedWidget.currentIndex.__name__
    _name_set_value_func = QStackedWidget.setCurrentIndex.__name__


class QComboBoxCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = int.__name__
    _name_get_value_func = QComboBox.currentIndex.__name__
    _name_set_value_func = QComboBox.setCurrentIndex.__name__


class QLineEditCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = str.__name__
    _name_get_value_func = QLineEdit.text.__name__
    _name_set_value_func = QLineEdit.setText.__name__


class QTextEditCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = str.__name__
    _name_get_value_func = QTextEdit.toPlainText.__name__
    _name_set_value_func = QTextEdit.setText.__name__


class QPlainTextEditCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = str.__name__
    _name_get_value_func = QPlainTextEdit.toPlainText.__name__
    _name_set_value_func = QPlainTextEdit.setPlainText.__name__


class QSpinBoxCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = int.__name__
    _name_get_value_func = QSpinBox.value.__name__
    _name_set_value_func = QSpinBox.setValue.__name__


class QDoubleSpinBoxCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = float.__name__
    _name_get_value_func = QDoubleSpinBox.value.__name__
    _name_set_value_func = QDoubleSpinBox.setValue.__name__


class QLabelCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = str.__name__
    _name_get_value_func = QLabel.text.__name__
    _name_set_value_func = QLabel.setText.__name__


class QProgressBarCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = int.__name__
    _name_get_value_func = QProgressBar.value.__name__
    _name_set_value_func = QProgressBar.setValue.__name__


class QAbstractSliderCodeGenerator(QWidgetCodeGenerator):
    _name_value_type = int.__name__
    _name_get_value_func = QAbstractSlider.value.__name__
    _name_set_value_func = QAbstractSlider.setValue.__name__


def get_code_generator(object_name: str) -> 'QWidgetCodeGenerator':
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
    for object_name in object_names:
        if object_name and not object_name.startswith('#') and '_' in object_name:
            try:
                code_generator = get_code_generator(object_name)
            # ignore unknown object types
            except ValueError:
                print(f'Unknown widget type for {object_name}.')
            else:
                code = code_generator.generate_code()
                if code:
                    output.append(code)
                    worked += 1

    # class name is file name converted to CamelCase and with "Helper" appended
    class_name = ''.join(word.capitalize() for word in input_path.stem.split('_'))

    # save output file
    with output_path.open('w') as f:
        f.write('# This file was autogenerated using pyqt-helper - do not edit!\n\n\n')
        f.write(f'class {class_name}Helper:\n\n')
        f.write('\n'.join(output))

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
