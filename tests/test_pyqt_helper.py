import pytest
import pkg_resources
from pyqt_helper.pyqt_helper import main, process_file


def test_version():
    version = pkg_resources.require('pyqt-helper')[0].version
    assert version == '0.0.2'


def test_main():
    with pytest.raises(TypeError):
        main()

    for argv in (
        [],
        ['a'],
        ['a', 'b', 'c', 'd'],
    ):
        with pytest.raises(TypeError):
            main(argv)


def test_process_file():
    for args in (
        ['data/dummy_ui.txt'],
        ['data/dummy_ui.txt', 'data/dummy_ui_helper_2.py'],
    ):
        output_path = process_file(*args)

        # compare with expected output
        with open('data/dummy_ui_correct.py') as output_correct:
            with open(output_path) as output_generated:
                assert output_correct.readlines() == output_generated.readlines()