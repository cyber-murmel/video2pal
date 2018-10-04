#!/usr/bin/env python2.7

import os
from tempfile import mkdtemp
from threading import Thread
from time import sleep
from multiprocessing import Process
from multiprocessing.pool import ThreadPool

import pal_transmit_block

def main():
    pool = ThreadPool(processes=3)
    try:
        # create two fifos in temporary directory
        tmpdir = mkdtemp()
        path_fifo_Y = os.path.join(tmpdir, "Y")
        path_fifo_U = os.path.join(tmpdir, "U")
        path_fifo_V = os.path.join(tmpdir, "V")
        os.mkfifo(path_fifo_Y)
        os.mkfifo(path_fifo_U)
        os.mkfifo(path_fifo_V)
        class options:
            path_fifo_y = path_fifo_Y
            path_fifo_u = path_fifo_U
            path_fifo_v = path_fifo_V
        pal_transmit_block_process = Process(target=pal_transmit_block.main, kwargs={"options": options})
        pal_transmit_block_process.start()

        try:
            # concurrently open writing access to all fifos, because we don't
            # know in what order the gnuradio generated script will open them
            fifo_Y_result = pool.apply_async(open, (path_fifo_Y, 'wb')) # tuple of args for foo
            fifo_U_result = pool.apply_async(open, (path_fifo_U, 'wb')) # tuple of args for foo
            fifo_V_result = pool.apply_async(open, (path_fifo_V, 'wb')) # tuple of args for foo
            fifo_Y = fifo_Y_result.get()
            fifo_U = fifo_U_result.get()
            fifo_V = fifo_V_result.get()
            
            # TODO make magichappen here
            for i in range(5000):
                fifo_Y.write(b'\x00\x00\x00\x70'*2700)
                fifo_U.write(b'\x00\x00\x00\x70'*2700)
                fifo_V.write(b'\x00\x00\x00\x70'*2700)
        finally:
            fifo_Y.close()
            fifo_U.close()
            fifo_V.close()

        pal_transmit_block_process.join()
    finally:
        os.remove(path_fifo_Y)
        os.remove(path_fifo_U)
        os.remove(path_fifo_V)
        os.rmdir(tmpdir)

if __name__ == '__main__':
    main()
