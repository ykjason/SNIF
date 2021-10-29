import cv2
import numpy
import show_window_tk
from mss import mss

def ss_to_array(image: 'Screenshot'):
    return numpy.array(image)

def setup_selection():
    selection = show_window_tk.Window(False, True)
    selection.run()
    return format_region(selection.region_dimensions())

def setup_videowriter(dimensions):
    # cv2.namedWindow('Screen',cv2.WINDOW_NORMAL)
    # frame_size = (dimensions['width'], dimensions['height'])
    # fourcc = cv2.VideoWriter_fourcc(*'h264')
    return cv2.VideoWriter('video1.mp4', fourcc=-1, fps=60,
                           frameSize=(dimensions['width'], dimensions['height']), isColor=True)



def run(area, video_writer):
    # window = mss()
    # cv2.namedWindow('Screen', cv2.WINDOW_NORMAL)
    # x = {'left': 600, 'top': 300, 'width': 560, 'height': 450}
    print(area)
    with mss() as window:
        cv2.namedWindow('Screen')
        while True:
            frame = ss_to_array(window.grab(area))
            cv2.imshow('Screen', frame)
            video_writer.write(frame)
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break

def format_region(rectangle):
    # The offsets are specific to my setup
    offset_x, offset_y = 9, 31
    return {'left': min(rectangle[0], rectangle[2]) + offset_x,
            'top': min(rectangle[1], rectangle[3]) + offset_y,
            'width': abs(rectangle[2]-rectangle[0]),
            'height': abs(rectangle[3] - rectangle[1])}

if __name__ == '__main__':
    region_dimensions = setup_selection()
    video_writer = setup_videowriter(region_dimensions)
    run(region_dimensions, video_writer)
    video_writer.release()
