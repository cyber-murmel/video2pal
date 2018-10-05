#!/usr/bin/env python2.7

import os
from tempfile import mkdtemp
from threading import Thread
from time import sleep
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from io import BytesIO
from struct import pack

import pal_transmit_block



# lines and pixels
NUMB_LINES      = 625
VISIB_LINES     = 576
PIXEL_PER_LINE  = 702
VIDEO_SCALE     = '{}:{}'.format(PIXEL_PER_LINE, VISIB_LINES)

# timing values in micro seconds
## video line anatomy
# | h sync | burst delay | burst | visual delay | visual | front porch |
# |--------|-------------|-------|--------------|--------|-------------|
# |  4.7us |       0.9us | 2.25us|        2.5us |   52us |      1.65us |
TIME_LINE           = 64e-6                             # time per line = 64us
TIME_VISUAL         = 52e-6                             # video time
TIME_PIXEL          = TIME_VISUAL/PIXEL_PER_LINE        # time per pixel
SAMP_PIXEL          = 1                                 # number of samples per pixel
SAMP_RATE           = SAMP_PIXEL/TIME_PIXEL             # resulting sample rate
SAMP_LINE           = SAMP_RATE*TIME_LINE               # sample per line
NUMB_SAMP           = SAMP_LINE*NUMB_LINES              # number of samples per double frame
BYTES_SAMP          = 2                                 # one short per sample
BUFF_SIZE           = int(NUMB_SAMP*BYTES_SAMP)         # frame buffer size

# number of samples per part
SAMP_H_SYNC         = int(SAMP_RATE*4.7e-6)
SAMP_BURST_DELAY    = int(SAMP_RATE*0.9e-6)
SAMP_BURST          = int(SAMP_RATE*2.25e-6)
SAMP_VISUAL_DELAY   = int(SAMP_RATE*2.5e-6)
SAMP_VISUAL         = int(SAMP_RATE*TIME_VISUAL)
SAMP_FRONT_PORCH    = SAMP_LINE-SAMP_H_SYNC-SAMP_BURST_DELAY-SAMP_BURST-SAMP_VISUAL_DELAY-SAMP_VISUAL
SAMP_S_SYNC         = int(SAMP_RATE*2.35e-6)          # short sync low pulse
SAMP_L_SYNC         = int(SAMP_RATE*27.3e-6)          # long sync hight pulse

# signal levels
LEVEL_SYNC  = int((2**15-1)*0.0)
LEVEL_BLANK = int((2**15-1)*0.285)
LEVEL_BLACK = int((2**15-1)*0.339)
LEVEL_WHITE = int((2**15-1)*1.0)

def prefill_buffers():
    buff_Y, buff_U, buff_V = [BytesIO(b'\x00'*BUFF_SIZE) for _ in range(3)]
    # first V sync
    for _ in range(6):
        buff_Y.seek(2*SAMP_S_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_S_SYNC))
    for _ in range(5):
        buff_Y.seek(2*SAMP_L_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_L_SYNC))
    for _ in range(5):
        buff_Y.seek(2*SAMP_S_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_S_SYNC))
    # first half frame
    for _ in range(305):
        buff_Y.seek(2*SAMP_H_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_BURST_DELAY+SAMP_BURST+SAMP_VISUAL_DELAY))
        buff_Y.seek(2*SAMP_VISUAL, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_FRONT_PORCH))
    # second V sync
    for _ in range(5):
        buff_Y.seek(2*SAMP_S_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_S_SYNC))
    for _ in range(5):
        buff_Y.seek(2*SAMP_L_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_L_SYNC))
    for _ in range(4):
        buff_Y.seek(2*SAMP_S_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_LINE/2-SAMP_S_SYNC))
    # second half frame
    for _ in range(305):
        buff_Y.seek(2*SAMP_H_SYNC, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_BURST_DELAY+SAMP_BURST+SAMP_VISUAL_DELAY))
        buff_Y.seek(2*SAMP_VISUAL, 1)
        buff_Y.write(pack("h", LEVEL_BLANK)*int(SAMP_FRONT_PORCH))
    return buff_Y, buff_U, buff_V

def ffmpeg_producer(path_fifo_Y, path_fifo_U, path_fifo_V):
    try:
        buff_Y, buff_U, buff_V = prefill_buffers()
        # concurrently open writing access to all fifos, because we don't
        # know in what order the gnuradio generated script will open them
        pool = ThreadPool(processes=3)
        fifo_Y_result = pool.apply_async(open, (path_fifo_Y, 'wb'))
        fifo_U_result = pool.apply_async(open, (path_fifo_U, 'wb'))
        fifo_V_result = pool.apply_async(open, (path_fifo_V, 'wb'))
        fifo_Y = fifo_Y_result.get()
        fifo_U = fifo_U_result.get()
        fifo_V = fifo_V_result.get()

        # TODO make magichappen here
        for i in range(50000):
            # set buffer pointer to beginning of it
            buff_Y.seek(0)
            buff_U.seek(0)
            buff_V.seek(0)
            for j in range(100):
                fifo_Y.write(buff_Y.read(BUFF_SIZE/100))
                fifo_U.write(buff_U.read(BUFF_SIZE/100))
                fifo_V.write(buff_V.read(BUFF_SIZE/100))
            fifo_Y.write(buff_Y.read())
            fifo_U.write(buff_U.read())
            fifo_V.write(buff_V.read())
            print(i/25.0)
    finally:
        fifo_Y.close()
        fifo_U.close()
        fifo_V.close()


def main():
    try:
        # create two fifos in temporary directory
        tmpdir = mkdtemp()
        path_fifo_Y = os.path.join(tmpdir, "Y")
        path_fifo_U = os.path.join(tmpdir, "U")
        path_fifo_V = os.path.join(tmpdir, "V")
        os.mkfifo(path_fifo_Y)
        os.mkfifo(path_fifo_U)
        os.mkfifo(path_fifo_V)
        # start put paths into options class to pass to gnuradio generated script
        # and start it
        class options:
            path_fifo_y = path_fifo_Y
            path_fifo_u = path_fifo_U
            path_fifo_v = path_fifo_V
        pal_transmit_block_process = Process(target=pal_transmit_block.main, kwargs={"options": options})
        pal_transmit_block_process.start()
        # start ffmpeg producer and when finished wait for the gnuradio thing to
        # finish too
        ffmpeg_producer(path_fifo_Y, path_fifo_U, path_fifo_V)
    finally:
        pal_transmit_block_process.terminate()
        pal_transmit_block_process.join()
        # cleanup
        os.remove(path_fifo_Y)
        os.remove(path_fifo_U)
        os.remove(path_fifo_V)
        os.rmdir(tmpdir)

if __name__ == '__main__':
    main()
