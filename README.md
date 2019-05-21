# pyqt-helper

PyQt Helper is a script for auto-generating boiler plate code for interacting with PyQt widgets, such as value getters and setters, widget connections, and slot functions.

Usage
-----

`python pyqt_helper.py widgets.txt`

where `widgets.txt` is a text file containing a PyQt widget object name on each line e.g. `spinBox_distance`.

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

A PyQt UI class can then simply inherit `WidgetsHelper` to gain the provided functionality:

```python
class MyWindow(QMainWindow, WidgetsHelper):

    def method(self):
        # enable the distance spin box and set its value to 100
        self.distance_enabled = True
        self.distance = 100
        
```
