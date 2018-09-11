#!/usr/bin/env python3
import subprocess

VISIB_LINES = 576
PIXEL_PER_LINE = 702
VIDEO_SCALE = '{}:{}'.format(PIXEL_PER_LINE, VISIB_LINES)

ffmpeg = subprocess.Popen(['/usr/bin/ffmpeg',
    '-i', '/home/marble/lib/Videos/bigbuckbunny.mp4',
    '-c:v', 'rawvideo',
    '-vf', 'scale=' + VIDEO_SCALE + ':force_original_aspect_ratio=decrease,pad=' + VIDEO_SCALE + ':(ow-iw)/2:(oh-ih)/2',
    '-c:v', 'rawvideo',
    '-f', 'rawvideo',
    '-pix_fmt', 'yuv444p',
    '-r', '50',
    #    '-y',
    '-'],
    stdout = subprocess.PIPE)

while True:
    #y = list(ffmpeg.stdout.read(702*576))
    #u = list(ffmpeg.stdout.read(702*576))
    v = list(ffmpeg.stdout.read(702*576*3))
    if len(v) < 702*576:
        break;
    #data = [y, u, v]

ffmpeg.kill()
