#!/usr/bin/env python3
import subprocess
from PIL import Image
from math import tau, sqrt, sin, cos
from struct import pack
from io import BytesIO

even_frame = True
phase = 0

# lines and pixels
NUMB_LINES      = 625
VISIB_LINES     = 576
PIXEL_PER_LINE  = 702
VIDEO_SCALE     = '{}:{}'.format(PIXEL_PER_LINE, VISIB_LINES)

### timing values in micro seconds
## video line
# | h sync | burst delay | burst | visual delay | visual | front porch |
# |--------|-------------|-------|--------------|--------|-------------|
# |  4.7us |       0.9us | 2.25us|        2.5us |   52us |      1.65us |
SUBC_FREQ           = 4433618.75                        # subcarrier frquency
TIME_LINE           = 64e-6                             # time per line = 64us
TIME_VISUAL         = 52e-6                             # video time
TIME_PIXEL          = TIME_VISUAL/PIXEL_PER_LINE        # time per pixel
SAMP_PIXEL          = 1                                 # number of samples per pixel
SAMP_RATE           = SAMP_PIXEL/TIME_PIXEL             # resulting sample rate
SAMP_LINE           = SAMP_RATE*TIME_LINE               # sample per line
NUMB_SAMP           = SAMP_LINE*NUMB_LINES              # number of samples per double frame
BYTES_SAMP          = 1                                 # bytes per sample
BUFF_SIZE           = int(NUMB_SAMP*BYTES_SAMP)         # frame buffer size
print(SAMP_RATE)
### number of samples
SAMP_H_SYNC         = round(SAMP_RATE*4.7e-6)
SAMP_BURST_DELAY    = round(SAMP_RATE*0.9e-6)
SAMP_BURST          = round(SAMP_RATE*2.25e-6)
SAMP_VISUAL_DELAY   = round(SAMP_RATE*2.5e-6)
SAMP_VISUAL         = round(SAMP_RATE*TIME_VISUAL)
SAMP_FRONT_PORCH    = round(SAMP_RATE*1.6e-6)
SAMP_LINE           = SAMP_H_SYNC+ SAMP_BURST_DELAY + SAMP_BURST + SAMP_VISUAL_DELAY + SAMP_VISUAL + SAMP_FRONT_PORCH
#print(SAMP_LINE)
#print(round(SAMP_LINE/SAMP_RATE*1e6, 3))
SAMP_S_SYNC         = round(SAMP_RATE*2.35e-6)          # short sync low pulse
SAMP_L_SYNC         = round(SAMP_RATE*4.7e-6)           # long sync hight pulse
### phase stuff
PHASE_DIFF_SAMP = tau*SUBC_FREQ/SAMP_RATE
PHASE_DIFF_LINE = tau*SUBC_FREQ*SAMP_LINE/SAMP_RATE
BURST_PHASE_ODD = -tau/8
BURST_PHASE_EVEN = tau/8
while PHASE_DIFF_LINE>tau: PHASE_DIFF_LINE -= tau
#print(PHASE_DIFF_LINE)
#print((SAMP_LINE+SAMP_H_SYNC)/SAMP_RATE*(NUMBER_LINES)*50/2) # this should be close to 1
#print(SAMP_RATE)

SUBC_FREQ = 4433618.75          # subcarrier frquency
SAMP_WITDH = 1/SAMP_RATE
TIME_PS = 1/SAMP_RATE           # time per sample
FPS_I = 50

### signal levels
LEVEL_SYNC  = int(255*0.0)
LEVEL_BLANK = int(255*0.285)
LEVEL_BLACK = int(255*0.339)
LEVEL_WHITE = int(255*1.0)

# snippets
LONG_SYNC   = [[LEVEL_SYNC, 0]] * (SAMP_LINE//2 - SAMP_L_SYNC) + [[LEVEL_BLANK, 0]] * SAMP_L_SYNC
SHORT_SYNC  = [[LEVEL_SYNC, 0]] * SAMP_S_SYNC + [[LEVEL_BLANK, 0]] * (SAMP_LINE//2 - SAMP_S_SYNC)
#BLANK_LINE  =

def yuv_frame2pal_frame(yuv_frame):
    global even_frame, phase
    result = []
    # add 5 long syncs
    result += 5*LONG_SYNC + 5*SHORT_SYNC    # +5 = 5 lines
    if even_frame:
        result += [[LEVEL_BLACK, 0]] * (SAMP_LINE//2)

    for i in range(17):                     # +17 = 22 lines
        result += [[LEVEL_BLANK, 0]] * SAMP_BURST_DELAY
        result += [
            [sqrt(1/2)*LEVEL_BLANK * (1 + cos((BURST_PHASE_EVEN if even_frame else BURST_PHASE_ODD)+phase+i*PHASE_DIFF_SAMP)/2),
             sqrt(1/2)*LEVEL_BLANK * (1 + sin((BURST_PHASE_EVEN if even_frame else BURST_PHASE_ODD)+phase+i*PHASE_DIFF_SAMP)/2)]
             for i in range(0, SAMP_BURST)
        ]
    even_frame = not even_frame
    return result

def main():
    ffmpeg = subprocess.Popen(['/usr/bin/ffmpeg',
        '-i', '/home/marble/lib/Videos/bigbuckbunny.mp4',
        '-c:v', 'rawvideo',
        '-vf', 'scale=' + VIDEO_SCALE + ':force_original_aspect_ratio=decrease,pad=' + VIDEO_SCALE + ':(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'rawvideo',
        '-f', 'rawvideo',
        '-pix_fmt', 'yuv444p',
        '-r', '50',
        '-loglevel', 'quiet',
        #    '-y',
        '-'],
        stdout = subprocess.PIPE)
    # read 100 frames
    ffmpeg.stdout.read(702*576*3*100)
    Y_BUFF, U_BUFF, V_BUFF = [BytesIO(b'\x00'*5) for _ in range(3)]
    # write synchronisation pulses into Y buffer
    Y_BUFF.write(
        (
            bytes([LEVEL_SYNC]*(SAMP_LINE-SAMP_L_SYNC)) +
            bytes([LEVEL_BLANK]*SAMP_L_SYNC)
        )*5 +
        (
            bytes([LEVEL_SYNC]*SAMP_S_SYNC) +
            bytes([LEVEL_BLANK]*(SAMP_LINE-SAMP_L_SYNC))
        )*5
    )

    with open('/dev/stdout', 'wb') as out:
        while ffmpeg.poll() == None:
            y = ffmpeg.stdout.read(VISIB_LINES*PIXEL_PER_LINE)
            u = ffmpeg.stdout.read(VISIB_LINES*PIXEL_PER_LINE)
            v = ffmpeg.stdout.read(VISIB_LINES*PIXEL_PER_LINE)
            Y_BUFF.seek(0)
            # out.write(Y_BUFF.read())


    # # img = Image.new('YCbCr', (702, 576))
    #
    # # read and zip 1 frame
    # y = list(ffmpeg.stdout.read(702*576))
    # u = list(ffmpeg.stdout.read(702*576))
    # v = list(ffmpeg.stdout.read(702*576))
    # data = [_ for _ in zip(y, u, v)]
    #
    # #img.putdata(data)
    # #img.show()
    # qi = yuv_frame2pal_frame(data)
    # flat = [item for sublist in qi for item in sublist]
    # buf = pack('%sf' % len(flat), *flat)
    # with open('/dev/stdout', 'wb') as out:
    #     out.write(buf)
    # #print(len(out))

    ffmpeg.kill()
    Y_BUFF.close()
    U_BUFF.close()
    V_BUFF.close()

if __name__ == "__main__":
    main()
