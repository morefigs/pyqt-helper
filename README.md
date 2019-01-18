# pyqt-ui-helper

Script for autogenerating getter and setter code for PyQt UI objects.

Usage
-----

`python pyqt_ui_helper.py widgets.txt`

where `widgets.txt` is a text file containing a PyQt widget object name on each line, and each object name starts with the object type, e.g. `spinBox_distance`.

Example
-------

Given a text file named `widgets.txt` containing the object name of `spinBox_distance`, the following code would be generated and saved to a Python file named `widgets_helper.py`:

```python
class WidgetsHelper:

    @property
    def distance(self) -> int:
        return self.ui.spinBox_distance.value()

    @distance.setter
    def distance(self, value: int) -> None:
        self.ui.spinBox_distance.setValue(value)

    @property
    def distance_enabled(self) -> bool:
        return self.ui.spinBox_distance.isEnabled()

    @distance_enabled.setter
    def distance_enabled(self, enabled: bool) -> None:
        self.ui.spinBox_distance.setEnabled(enabled)
```
