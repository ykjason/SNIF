from mss import mss
import show_window

class Window():
    def __init__(self):
        self._window = mss()
        self._main_monitor = self._window.monitors[1]


    def grab_main_monitor(self):
        return self._window.grab(self._main_monitor)



    def return_window(self):
        return self._window


    def return_main_monitor(self):
        return self._main_monitor


if __name__ == '__main__':
    temp = Window()
    print(temp.return_window().monitors)
    #[{'left': 0, 'top': 0, 'width': 4240, 'height': 1537}, combination of both monitors
    # {'left': 0, 'top': 0, 'width': 2560, 'height': 1440}, primary monitor
    # {'left': 2560, 'top': 487, 'width': 1680, 'height': 1050}] secondary monitor
    print(temp.return_main_monitor())
    show_window.run(temp.grab_main_monitor())

