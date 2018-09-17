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

with open('/dev/stdout', 'wb') as out:
    while ffmpeg.poll() == None:
        v = ffmpeg.stdout.read(702*576*3)
        out.write(v)

ffmpeg.kill()
