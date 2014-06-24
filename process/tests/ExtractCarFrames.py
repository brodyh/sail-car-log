from VideoReader import * 
from ArgParser import *
import sys, cv2, pickle

FRAME_STEP = 5
HISTORY_WINDOW = 30 
FUTURE_WINDOW = 20

def export_frames(fnums, fname):
    f = open(fname, 'w')
    pickle.dump(fnums, f)


def drawBorder(I, color, thickness): 
    cv2.rectangle(I, (0,0), (I.shape[1], I.shape[0]), color, thickness)

if __name__ == '__main__':
    args = parse_args(sys.argv[1], sys.argv[2])
    reader = VideoReader(args['video'])

    framenums = set()
    last_record = 0 
    while True:
        for p in range(FRAME_STEP):
            (success, I) = reader.getNextFrame()
        if not success:
            break

        if reader.framenum in framenums:
            drawBorder(I, (0,255,0), 10)
        cv2.imshow('video', I)
        key = chr(cv2.waitKey(50) & 255)
        if key == 'c':
            print reader.framenum
            for p in range(HISTORY_WINDOW):
                framenums.add(reader.framenum - p)
            for p in range(FUTURE_WINDOW):
                framenums.add(reader.framenum + p)

    export_frames(framenums, sys.argv[3])
