import pytest
from pyqt_helper.pyqt_helper import main, process_file


def test_main():
    # test number of args
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
