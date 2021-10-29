#arrows change start/stop indexes of video
#create a new video from the base video each time for viewing
#read from opencv videocapture of the video file
#write each in-bound frame to another video file
import cv2
from functools import partial

def prepare_video(video_file):
    old_video = cv2.VideoCapture(video_file)
    new_video = cv2.VideoWriter('video2.mp4', fourcc=-1, fps=60,
                           frameSize=(int(old_video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                      int(old_video.get(cv2.CAP_PROP_FRAME_HEIGHT))), isColor=True)
    edit_video(old_video, new_video)
    old_video.release()

def edit_video(old_video, new_video):
    cv2.namedWindow('Editing', cv2.WINDOW_NORMAL)
    # get_old_video_frame = partial(display_frame, get_frames(old_video))
    # adjust_window(old_video)
    frames = get_frames(old_video)
    display_frame(frames,0)
    prep_update_bar_one = partial(update_bar_one, frames)
    prep_update_bar_two = partial(update_bar_two, frames)
    prep_play_video = partial(play_video, old_video, frames)
    frame_count = int(old_video.get(cv2.CAP_PROP_FRAME_COUNT))-1
    cv2.createTrackbar('Start', 'Editing', 0, frame_count, prep_update_bar_one)
    cv2.createTrackbar('End', 'Editing', frame_count, frame_count, prep_update_bar_two)
    cv2.createTrackbar('Play', 'Editing', 0, 1, prep_play_video)
    continue_editing = True
    while continue_editing:
        key = cv2.waitKey(0)
        if key == ord('q') or key == -1: #key pressed is q or the exit button
            cv2.destroyAllWindows()
            continue_editing = False
        elif key == 13: # ordinal value of enter key
            save_video(frames, new_video)
            cv2.destroyAllWindows()
            continue_editing = False

def adjust_window(video):
    if video.get(cv2.CAP_PROP_FRAME_WIDTH) < 200 or video.get(cv2.CAP_PROP_FRAME_HEIGHT) < 200:
        cv2.resizeWindow('Editing', 500,500)
        print('hit')

def get_frames(video):
    frames = []
    while True:
        ret, frame = video.read()
        if ret:
            frames.append(frame)
        else:
            break
    return frames

def display_frame(frames, index):
    # displays the corresponding index of the frame within the video
    # cv2.imshow('Editing',cv2.imread('melt.png'))
    cv2.imshow('Editing', frames[index])

def update_bar_one(frames, event):
    cv2.setTrackbarMin('End', 'Editing', event + 1)
    if event >= cv2.getTrackbarPos('End', 'Editing'):
        cv2.setTrackbarPos('End', 'Editing', event + 1)
    display_frame(frames, event)

def update_bar_two(frames, event):
    cv2.setTrackbarMax('Start', 'Editing', event - 1)
    if event <= cv2.getTrackbarPos('Start', 'Editing'):
        cv2.setTrackbarPos('Start', 'Editing', event - 1)
    display_frame(frames, event)

def play_video(video, frames, event):
    wait = int(1000 / video.get(cv2.CAP_PROP_FPS))
    if event == 1:
        for i in range(cv2.getTrackbarPos('Start', 'Editing'), cv2.getTrackbarPos('End', 'Editing')):
            if cv2.getTrackbarPos('Play', 'Editing') == 0:
                break
            display_frame(frames, i)
            key = cv2.waitKey(wait)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
    else:
        display_frame(frames, cv2.getTrackbarPos('Start', 'Editing'))

def save_video(frames, video_writer):
    for i in range(cv2.getTrackbarPos('Start', 'Editing'), cv2.getTrackbarPos('End', 'Editing')):
        video_writer.write(frames[i])
    video_writer.release()

def do_something(event):
    print('clicked')

if __name__ == '__main__':
    prepare_video('video1.mp4')
