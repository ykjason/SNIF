import tkinter as tk
#notes: edit bindings remain after creating the first window (does not have to press edit button again)
# make region control be able to cross over each other
def announce(event):
    print(f'clicked at {event.x} {event.y}')

def released(event):
    print(f'released at {event.x} {event.y}')

def nothing(event):
    print('hello')

class Window:
    def __init__(self, *args):
        self._window = tk.Tk()
        # self._set_geometry(self._window_dimensions())
        self._window_options(*args)
        self._create_canvas()
        self._set_window_bindings()
        self._active_buttons = False
        self._region_selected = True


    def _window_dimensions(self):
        # stores the width and height of the screen as an attribute
        # my window is 2560x1440
        self._width = self._window.winfo_screenwidth()
        self._height = self._window.winfo_screenheight()

    def _set_window_bindings(self):
        # binds select events for the main window
        self.canvas.bind('<Button-1>', self._first_point)
        self.canvas.bind('<B1-Motion>', self._second_point)
        self.canvas.bind('<ButtonRelease-1>', self._selected_area_options)

    def _window_options(self, fullscreen: bool, transparent: bool):
        # Applies additional options/settings to the window
        self._window.title('Area Selection')
        self._window_dimensions()
        if fullscreen:
            self._window.attributes('-fullscreen', 1)
        if transparent:
            self._window.attributes('-alpha', 0.5)

    def _set_geometry(self, dimensions: tuple):
        # sets the dimensions of the tkinter window using the screen dimensions
        self._window.geometry(f'{dimensions[0]}x{dimensions[1]}')

    def _create_canvas(self):
        self.canvas = tk.Canvas(self._window, width=self._width,
                                height=self._height)
        self.canvas_window = self.canvas.create_window(0, 0)
        self.canvas.pack()

    def _first_point(self, event):
        # Records the coordinates of the first point/corner of the recording area
        # Additionally stores this initial click as the final click in the event of no mouse movement
        if self._active_buttons == True:
            self._remove_selected_region()
        self._rectangle = Rectangle(event.x, event.y)
        self._rectangle.second_point(event.x, event.y)
        print(f'clicked at {event.x} {event.y}')

    def _second_point(self, event):
        # Records the coordinates of the next/final points
        self._rectangle.second_point(event.x, event.y)
        self._draw_canvas()

    def _draw_canvas(self):
        # Draws a new rectangle and deletes the previous one if any
        self.canvas.create_rectangle(self._rectangle.points(), fill='#F2034F', tags='selectedAreaRectangle')
        self._delete_oldest_object()

    def _delete_oldest_object(self):
        # Deletes the oldest object created on the canvas
        # print(self.canvas.find_all())
        # for i in self.canvas.find_all():
        #     print(self.canvas.type(i),i)
        #     print(self.canvas.gettags(i))
        if len(self.canvas.find_all()) > 2 and \
                self.canvas.gettags(self.canvas.find_all()[1])[0] == 'selectedAreaRectangle':
            self.canvas.delete(self.canvas.find_all()[1])

    def _remove_selected_region(self):
        print(self.canvas.find_all())
        for i in self.canvas.find_all():
            print(self.canvas.type(i))
        self.canvas.delete('selectedAreaRectangle')
        # self.canvas.delete('optionPrompt')
        self._button_frame.destroy()
        self._active_buttons = False
        print(self.canvas.find_all())

    def _selected_area_options(self, event):
        print(event.x, event.y)
        self._option_window_size = (133, 25)
        self._appropriate_button_location(self._button_spacing())
        self._create_buttons(text='Confirm', command=self._confirm_window, column=0)
        self._create_buttons(text='Edit', command=self._edit_window_commands, column=1)
        self._create_buttons(text='Cancel', command=self._remove_selected_region, column=2)

    def _confirm_window(self):
        print(self._rectangle.points())
        self._window.destroy()
        self._region_selected = True

    def region_dimensions(self):
        if self._region_selected:
            return self._rectangle.points()

    def _edit_window_commands(self):
        self.canvas.bind('<Key>', self._edit_window)
        # self.canvas.bind('<Key-Up>', self._edit_window)
        # self.canvas.bind('<Key-Left>', self._edit_window)
        # self.canvas.bind('<Key-Right>', self._edit_window)
        # self.canvas.bind('<Key-w>', self._edit_window)
        # self.canvas.bind('<Key-a>', self._edit_window)
        # self.canvas.bind('<Key-s>', self._edit_window)
        # self.canvas.bind('<Key-d>', self._edit_window)
        self.canvas.focus_set()

    def _edit_window(self, event):
        # Edits the selected region by creating a new rectangle with a larger/smaller dimension
        old_point = self._rectangle.right_x(), self._rectangle.bottom_y()
        if event.keysym == 'Down':
            self._rectangle = Rectangle(self._rectangle.left_x(),self._rectangle.top_y())
            self._rectangle.second_point(old_point[0], old_point[1] + 1)
        elif event.keysym == 'Up':
            self._rectangle = Rectangle(self._rectangle.left_x(), self._rectangle.top_y()-1)
            self._rectangle.second_point(*old_point)
        elif event.keysym == 'Left':
            self._rectangle = Rectangle(self._rectangle.left_x()-1, self._rectangle.top_y())
            self._rectangle.second_point(*old_point)
        elif event.keysym == 'Right':
            self._rectangle = Rectangle(self._rectangle.left_x(), self._rectangle.top_y())
            self._rectangle.second_point(old_point[0] + 1, old_point[1])
        elif event.keysym.upper() == 'W':
            self._rectangle = Rectangle(self._rectangle.left_x(), self._rectangle.top_y())
            self._rectangle.second_point(old_point[0], old_point[1] - 1)
        elif event.keysym.upper() == 'A':
            self._rectangle = Rectangle(self._rectangle.left_x(), self._rectangle.top_y())
            self._rectangle.second_point(old_point[0] - 1, old_point[1])
        elif event.keysym.upper() == 'S':
            self._rectangle = Rectangle(self._rectangle.left_x(), self._rectangle.top_y() + 1)
            self._rectangle.second_point(old_point[0], old_point[1])
        elif event.keysym.upper() == 'D':
            self._rectangle = Rectangle(self._rectangle.left_x() + 1, self._rectangle.top_y())
            self._rectangle.second_point(old_point[0], old_point[1])
        self._draw_canvas()
        self._button_frame.destroy()
        self._selected_area_options(event)


    def _button_spacing(self):
        if self._check_space(self._rectangle.bottom_y(), self._option_window_size[1], self._height):
            return (self._rectangle.middle_x() - self._option_window_size[0] // 2, self._rectangle.bottom_y())
        elif self._check_space(self._rectangle.top_y(), -self._option_window_size[1], self._height):
            return (self._rectangle.middle_x() - self._option_window_size[0] // 2, self._rectangle.top_y())
        elif self._check_space(self._rectangle.right_x(), self._option_window_size[0], self._width):
            return (self._rectangle.right_x(), self._rectangle.middle_y() + self._option_window_size[1] // 2)
        elif self._check_space(self._rectangle.left_x(), -self._option_window_size[0], self._width):
            return (self._rectangle.left_x()-self._option_window_size[0], self._rectangle.middle_y() + self._option_window_size[1] // 2)
        else:
            return self._rectangle.center()

    def _check_space(self, coordinate, options, window):
        # Returns whether or not the options menu can fit within the window at the given coordinate
        additional_spacing = 100
        return additional_spacing <= coordinate + options <= window - additional_spacing

    def _appropriate_button_location(self, coordinates):
        # pass
        self._button_frame = tk.Frame(self.canvas, width=self._option_window_size[0],
                                      height=self._option_window_size[1])
        self._button_frame.grid_propagate(False)
        self.canvas.itemconfigure(self.canvas_window, window=self._button_frame, tags='optionPrompt')
        self._button_frame.place(x=coordinates[0],y=coordinates[1])
        self._active_buttons = True
        # print(self._button_frame)

    def _create_buttons(self, text, command, column):
        # self._button_frame = tk.Frame(self.canvas, bg='#FF0000', width=100, height=100)
        # print(self._button_frame)
        button = tk.Button(self._button_frame, text=text, command=command)
        button.grid(row=0,column=column)

    def get_main_window(self):
        # returns main tkinter window
        return self._window

    def run(self):
        # executes mainloop for tkinter window
        self._window.mainloop()


class Rectangle:
    def __init__(self, x, y):
        self.x1, self.y1 = x, y

    def second_point(self, x, y):
        self.x2, self.y2 = x, y

    def points(self):
        return self.x1, self.y1, self.x2, self.y2

    def left_x(self):
        return min(self.x1, self.x2)

    def bottom_y(self):
        return max(self.y1, self.y2)

    def right_x(self):
        return max(self.x1, self.x2)

    def top_y(self):
        return min(self.y1, self.y2)

    def middle_x(self):
        return (self.x1 + self.x2) // 2

    def middle_y(self):
        return (self.y1 + self.y2) // 2

    def center(self):
        return (self.middle_x(), self.middle_y())

if __name__ == '__main__':
    w1 = Window(False, True)
    w1.run()
