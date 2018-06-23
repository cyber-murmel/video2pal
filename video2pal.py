#!/usr/bin/env python3
import subprocess
from PIL import Image

VIDEO_SCALE = '702:576'
ffmpeg = subprocess.Popen(['/usr/bin/ffmpeg',
    '-i', '/home/marble/lib/Videos/bigbuckbunny.mp4',
    '-c:v', 'rawvideo',
    '-vf', 'scale=' + VIDEO_SCALE + ':force_original_aspect_ratio=decrease,pad=' + VIDEO_SCALE + ':(ow-iw)/2:(oh-ih)/2',
    '-c:v', 'rawvideo',
    '-f', 'rawvideo',
    '-pix_fmt', 'yuv444p',
    '-r', '50',
    '-y',
    '-'],
    stdout = subprocess.PIPE)

ffmpeg.stdout.read(702*576*3*100)

img = Image.new('YCbCr', (702, 576))

y = list(ffmpeg.stdout.read(702*576))
u = list(ffmpeg.stdout.read(702*576))
v = list(ffmpeg.stdout.read(702*576))
data = [_ for _ in zip(y, u, v)]

def yuv_frame2pal_frame(yuv_frame):
    pass

img.putdata(data)
img.show()

ffmpeg.kill()
