#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pal Transmit
# Generated: Sat Oct  6 22:11:47 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from long_sync_pulse import long_sync_pulse  # grc-generated hier_block
from math import sqrt
from optparse import OptionParser
from short_sync_pulse import short_sync_pulse  # grc-generated hier_block
import osmosdr
import pmt
from gnuradio import qtgui


class pal_transmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Pal Transmit")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pal Transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pal_transmit")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_visual = samp_visual = 702
        self.samp_rate = samp_rate = samp_visual/(52e-6)
        self.samp_line = samp_line = int((64e-6)*samp_rate)
        self.sub_freq = sub_freq = 4433618.75
        self.samp_visual_delay = samp_visual_delay = int(2.5/64*samp_line)
        self.samp_h_sync = samp_h_sync = int(4.7/64*samp_line)
        self.samp_burst_delay = samp_burst_delay = int(0.9/64*samp_line)
        self.samp_burst = samp_burst = int(2.25/64*samp_line)
        self.rf_gain = rf_gain = 14
        self.lines_visual = lines_visual = 576
        self.lines_half_frame = lines_half_frame = 305
        self.level_blank = level_blank = 0.285
        self.level_black = level_black = 0.339
        self.if_gain = if_gain = 40
        self.color_offset = color_offset = -0.25
        self.color_ampl = color_ampl = 0.5
        self.burst_ampl = burst_ampl = 0.15000
        self.bb_gain = bb_gain = 62

        ##################################################
        # Blocks
        ##################################################
        self._color_ampl_range = Range(0, 2, 0.01, 0.5, 200)
        self._color_ampl_win = RangeWidget(self._color_ampl_range, self.set_color_ampl, 'Color Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._color_ampl_win)
        self._burst_ampl_range = Range(0, 2, 0.01, 0.15000, 200)
        self._burst_ampl_win = RangeWidget(self._burst_ampl_range, self.set_burst_ampl, 'Color Burst Amplitude', "counter_slider", float)
        self.top_grid_layout.addWidget(self._burst_ampl_win)
        self.stdin = blocks.file_source(gr.sizeof_char*1, '/dev/stdin', False)
        self.stdin.set_begin_tag(pmt.PMT_NIL)
        self.short_sync_pulse_0_3_0_1 = short_sync_pulse(
            samp_half_line=samp_line/2,
        )
        self.short_sync_pulse_0_3_0_0_0 = short_sync_pulse(
            samp_half_line=samp_line/2,
        )
        self.short_sync_pulse_0_3_0_0 = short_sync_pulse(
            samp_half_line=samp_line/2,
        )
        self.short_sync_pulse_0_3_0 = short_sync_pulse(
            samp_half_line=samp_line/2,
        )
        self.osmosdr_sink_0_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf=0' )
        self.osmosdr_sink_0_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_0.set_center_freq(180e6, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(0, 0)

        self.long_sync_pulse_0_0 = long_sync_pulse(
            samp_half_line=432,
        )
        self.long_sync_pulse_0 = long_sync_pulse(
            samp_half_line=432,
        )
        self.blocks_vector_to_stream_2_1_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_vector_to_stream_2_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_vector_to_stream_2_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, lines_half_frame*samp_visual)
        self.blocks_vector_to_stream_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, lines_half_frame*samp_visual)
        self.blocks_vector_to_stream_1_1 = blocks.vector_to_stream(gr.sizeof_float*samp_visual, 3*lines_visual)
        self.blocks_vector_to_stream_1_0_1 = blocks.vector_to_stream(gr.sizeof_float*1, lines_half_frame*samp_visual)
        self.blocks_vector_to_stream_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, lines_half_frame*samp_visual)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_float*samp_visual, 3*lines_visual)
        self.blocks_vector_to_stream_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_line)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, samp_line/2)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_stream_to_vector_1_0_0_1_1 = blocks.stream_to_vector(gr.sizeof_float*1, samp_visual)
        self.blocks_stream_to_vector_1_0_0_1_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, samp_visual)
        self.blocks_stream_to_vector_1_0_0_1_0 = blocks.stream_to_vector(gr.sizeof_float*1, samp_visual)
        self.blocks_stream_to_vector_1_0_0_1 = blocks.stream_to_vector(gr.sizeof_float*1, samp_visual)
        self.blocks_stream_to_vector_1_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*samp_visual, lines_half_frame)
        self.blocks_stream_to_vector_1_0_0_0 = blocks.stream_to_vector(gr.sizeof_float*samp_visual, lines_half_frame)
        self.blocks_stream_to_vector_1_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, 3*samp_visual*lines_visual)
        self.blocks_stream_to_vector_0_1_1_2_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_1_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_1_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_1_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_burst)
        self.blocks_stream_to_vector_0_1_0_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_stream_to_vector_0_1_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_stream_to_vector_0_1_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_stream_to_vector_0_1_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_visual)
        self.blocks_stream_to_vector_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_line)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_line/2)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, samp_line/2)
        self.blocks_stream_to_streams_2 = blocks.stream_to_streams(gr.sizeof_gr_complex*samp_visual, 2)
        self.blocks_stream_to_streams_1 = blocks.stream_to_streams(gr.sizeof_float*samp_visual*lines_visual*3, 2)
        self.blocks_stream_to_streams_0_0_0_0 = blocks.stream_to_streams(gr.sizeof_float*samp_visual, 2)
        self.blocks_stream_to_streams_0_0_0 = blocks.stream_to_streams(gr.sizeof_float*samp_visual, 2)
        self.blocks_stream_to_streams_0_0 = blocks.stream_to_streams(gr.sizeof_float*lines_half_frame*samp_visual, 3)
        self.blocks_stream_to_streams_0 = blocks.stream_to_streams(gr.sizeof_float*lines_half_frame*samp_visual, 3)
        self.blocks_stream_mux_4 = blocks.stream_mux(gr.sizeof_gr_complex*samp_burst, (8, 305, 7, 305))
        self.blocks_stream_mux_3_0 = blocks.stream_mux(gr.sizeof_float*702, (9, lines_visual/2, 8))
        self.blocks_stream_mux_3 = blocks.stream_mux(gr.sizeof_float*702, (8, lines_visual/2, 9))
        self.blocks_stream_mux_2_1 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samp_h_sync+samp_burst_delay, samp_burst, samp_visual_delay, samp_visual, samp_line-(samp_h_sync+samp_burst_delay+samp_burst+samp_visual_delay+samp_visual)))
        self.blocks_stream_mux_2_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samp_h_sync,samp_burst_delay+samp_burst+samp_visual_delay, samp_visual, samp_line-(samp_h_sync+samp_burst_delay+samp_burst+samp_visual_delay+samp_visual)))
        self.blocks_stream_mux_2 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samp_h_sync,samp_burst_delay+samp_burst+samp_visual_delay, samp_visual, samp_line-(samp_h_sync+samp_burst_delay+samp_burst+samp_visual_delay+samp_visual)))
        self.blocks_stream_mux_1_1_0 = blocks.stream_mux(gr.sizeof_gr_complex*samp_visual, (8, 305, 7, 305))
        self.blocks_stream_mux_1_0_0_0_1 = blocks.stream_mux(gr.sizeof_gr_complex*samp_burst, (1,1))
        self.blocks_stream_mux_1 = blocks.stream_mux(gr.sizeof_gr_complex*samp_line/2, (6,5,5, 2*305, 5, 5, 4, 2*305))
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (samp_visual, samp_visual))
        self.blocks_null_source_0_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_1_0 = blocks.null_sink(gr.sizeof_float*samp_visual)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*samp_visual)
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(samp_burst)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.00390625/2, ))
        self.blocks_float_to_complex_1_0 = blocks.float_to_complex(lines_half_frame*samp_visual)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(lines_half_frame*samp_visual)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_1 = blocks.add_const_vcc(([-0.35*(1+1j)/sqrt(2)]*samp_visual))
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vcc((level_black, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((level_black, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 4433618.75, color_ampl, 0)
        self.analog_const_source_x_3_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.analog_const_source_x_3_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.analog_const_source_x_3_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_3 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_2 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_1_1_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_1_1_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_1_1_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_1_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_3_0_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, level_blank)
        self.analog_const_source_x_0_0_3_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, level_blank)
        self.analog_const_source_x_0_0_3_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, level_blank)
        self.analog_const_source_x_0_0_3_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, level_blank)
        self.analog_const_source_x_0_0_3 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_2_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, (-1+1j)/sqrt(2)*burst_ampl)
        self.analog_const_source_x_0_0_1_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, (-1-1j)/sqrt(2)*burst_ampl)
        self.analog_const_source_x_0_0_0_0_0_1_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_0_0_0_1_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_0_0_0_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0_0_0_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0.35*(1+1j)/sqrt(2))
        self.analog_const_source_x_0_0_0_0_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0.35*(1+1j)/sqrt(2))
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_const_source_x_0_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1_0_0_0_0, 0))
        self.connect((self.analog_const_source_x_0_0_0_0_0_0, 0), (self.blocks_stream_to_vector_0_1_0_0_0_0_0, 0))
        self.connect((self.analog_const_source_x_0_0_0_0_0_1, 0), (self.blocks_stream_mux_2_1, 0))
        self.connect((self.analog_const_source_x_0_0_0_0_0_1_0, 0), (self.blocks_stream_mux_2_1, 4))
        self.connect((self.analog_const_source_x_0_0_0_0_0_1_0_0, 0), (self.blocks_stream_mux_2_1, 2))
        self.connect((self.analog_const_source_x_0_0_1_0_0_0, 0), (self.blocks_stream_to_vector_0_1_1_2_0, 0))
        self.connect((self.analog_const_source_x_0_0_2_0_0_0, 0), (self.blocks_stream_to_vector_0_1_1_2, 0))
        self.connect((self.analog_const_source_x_0_0_3, 0), (self.blocks_stream_mux_2, 0))
        self.connect((self.analog_const_source_x_0_0_3_0, 0), (self.blocks_stream_mux_2, 1))
        self.connect((self.analog_const_source_x_0_0_3_0_0, 0), (self.blocks_stream_mux_2, 3))
        self.connect((self.analog_const_source_x_0_0_3_0_0_0, 0), (self.blocks_stream_mux_2_0, 3))
        self.connect((self.analog_const_source_x_0_0_3_0_1, 0), (self.blocks_stream_mux_2_0, 1))
        self.connect((self.analog_const_source_x_0_0_3_1_1, 0), (self.blocks_stream_to_vector_1_0_0_1, 0))
        self.connect((self.analog_const_source_x_0_0_3_1_1_0, 0), (self.blocks_stream_to_vector_1_0_0_1_0, 0))
        self.connect((self.analog_const_source_x_0_0_3_1_1_0_0, 0), (self.blocks_stream_to_vector_1_0_0_1_0_0, 0))
        self.connect((self.analog_const_source_x_0_0_3_1_1_1, 0), (self.blocks_stream_to_vector_1_0_0_1_1, 0))
        self.connect((self.analog_const_source_x_0_0_3_2, 0), (self.blocks_stream_mux_2_0, 0))
        self.connect((self.analog_const_source_x_3, 0), (self.blocks_stream_to_vector_0_1_1, 0))
        self.connect((self.analog_const_source_x_3_0, 0), (self.blocks_stream_to_vector_0_1_1_0, 0))
        self.connect((self.analog_const_source_x_3_0_0, 0), (self.blocks_stream_to_vector_0_1_1_1, 0))
        self.connect((self.analog_const_source_x_3_0_0_0, 0), (self.blocks_stream_to_vector_0_1_1_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_stream_mux_2, 2))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_stream_mux_2_0, 2))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_stream_to_streams_2, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_stream_to_vector_0_0_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_vector_to_stream_2, 0))
        self.connect((self.blocks_float_to_complex_1_0, 0), (self.blocks_vector_to_stream_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_stream_to_vector_1_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_vector_to_stream_0_1, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_null_source_0_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_stream_mux_2_1, 3))
        self.connect((self.blocks_stream_mux_1, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_stream_mux_1_0_0_0_1, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.blocks_stream_mux_1_1_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_stream_mux_2, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_mux_2_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_stream_mux_2_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_stream_mux_3, 0), (self.blocks_stream_to_vector_1_0_0_0, 0))
        self.connect((self.blocks_stream_mux_3_0, 0), (self.blocks_stream_to_vector_1_0_0_0_0, 0))
        self.connect((self.blocks_stream_mux_4, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.blocks_stream_to_streams_0, 1), (self.blocks_float_to_complex_1, 0))
        self.connect((self.blocks_stream_to_streams_0, 2), (self.blocks_float_to_complex_1, 1))
        self.connect((self.blocks_stream_to_streams_0, 0), (self.blocks_vector_to_stream_1_0, 0))
        self.connect((self.blocks_stream_to_streams_0_0, 1), (self.blocks_float_to_complex_1_0, 0))
        self.connect((self.blocks_stream_to_streams_0_0, 2), (self.blocks_float_to_complex_1_0, 1))
        self.connect((self.blocks_stream_to_streams_0_0, 0), (self.blocks_vector_to_stream_1_0_1, 0))
        self.connect((self.blocks_stream_to_streams_0_0_0, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_stream_to_streams_0_0_0, 0), (self.blocks_stream_mux_3, 1))
        self.connect((self.blocks_stream_to_streams_0_0_0_0, 0), (self.blocks_null_sink_1_0, 0))
        self.connect((self.blocks_stream_to_streams_0_0_0_0, 1), (self.blocks_stream_mux_3_0, 1))
        self.connect((self.blocks_stream_to_streams_1, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.blocks_stream_to_streams_1, 1), (self.blocks_vector_to_stream_1_1, 0))
        self.connect((self.blocks_stream_to_streams_2, 1), (self.blocks_vector_to_stream_2_1, 0))
        self.connect((self.blocks_stream_to_streams_2, 0), (self.blocks_vector_to_stream_2_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_stream_mux_1, 3))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_stream_mux_1, 7))
        self.connect((self.blocks_stream_to_vector_0_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0_0, 0), (self.blocks_stream_mux_1_1_0, 3))
        self.connect((self.blocks_stream_to_vector_0_1_0_0_0, 0), (self.blocks_stream_mux_1_1_0, 1))
        self.connect((self.blocks_stream_to_vector_0_1_0_0_0_0, 0), (self.blocks_stream_mux_1_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1_0_0_0_0_0, 0), (self.blocks_stream_mux_1_1_0, 2))
        self.connect((self.blocks_stream_to_vector_0_1_1, 0), (self.blocks_stream_mux_4, 0))
        self.connect((self.blocks_stream_to_vector_0_1_1_0, 0), (self.blocks_stream_mux_4, 2))
        self.connect((self.blocks_stream_to_vector_0_1_1_0_0, 0), (self.blocks_stream_mux_4, 3))
        self.connect((self.blocks_stream_to_vector_0_1_1_1, 0), (self.blocks_stream_mux_4, 1))
        self.connect((self.blocks_stream_to_vector_0_1_1_2, 0), (self.blocks_stream_mux_1_0_0_0_1, 0))
        self.connect((self.blocks_stream_to_vector_0_1_1_2_0, 0), (self.blocks_stream_mux_1_0_0_0_1, 1))
        self.connect((self.blocks_stream_to_vector_1_0_0, 0), (self.blocks_stream_to_streams_1, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_0, 0), (self.blocks_stream_to_streams_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_0_0, 0), (self.blocks_stream_to_streams_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_1, 0), (self.blocks_stream_mux_3, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_1_0, 0), (self.blocks_stream_mux_3, 2))
        self.connect((self.blocks_stream_to_vector_1_0_0_1_0_0, 0), (self.blocks_stream_mux_3_0, 2))
        self.connect((self.blocks_stream_to_vector_1_0_0_1_1, 0), (self.blocks_stream_mux_3_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1, 0), (self.blocks_stream_mux_2_1, 1))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_to_streams_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_vector_to_stream_1_0_1, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_vector_to_stream_1_1, 0), (self.blocks_stream_to_streams_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_2, 0), (self.blocks_stream_to_vector_0_1_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_2_0, 0), (self.blocks_stream_to_vector_0_1_0_0, 0))
        self.connect((self.blocks_vector_to_stream_2_1, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_vector_to_stream_2_1_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.long_sync_pulse_0, 0), (self.blocks_stream_mux_1, 1))
        self.connect((self.long_sync_pulse_0_0, 0), (self.blocks_stream_mux_1, 5))
        self.connect((self.short_sync_pulse_0_3_0, 0), (self.blocks_stream_mux_1, 0))
        self.connect((self.short_sync_pulse_0_3_0_0, 0), (self.blocks_stream_mux_1, 2))
        self.connect((self.short_sync_pulse_0_3_0_0_0, 0), (self.blocks_stream_mux_1, 6))
        self.connect((self.short_sync_pulse_0_3_0_1, 0), (self.blocks_stream_mux_1, 4))
        self.connect((self.stdin, 0), (self.blocks_uchar_to_float_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pal_transmit")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_visual(self):
        return self.samp_visual

    def set_samp_visual(self, samp_visual):
        self.samp_visual = samp_visual
        self.set_samp_rate(self.samp_visual/(52e-6))
        self.blocks_add_const_vxx_1.set_k(([-0.35*(1+1j)/sqrt(2)]*self.samp_visual))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_line(int((64e-6)*self.samp_rate))
        self.osmosdr_sink_0_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_samp_line(self):
        return self.samp_line

    def set_samp_line(self, samp_line):
        self.samp_line = samp_line
        self.set_samp_visual_delay(int(2.5/64*self.samp_line))
        self.set_samp_h_sync(int(4.7/64*self.samp_line))
        self.set_samp_burst_delay(int(0.9/64*self.samp_line))
        self.set_samp_burst(int(2.25/64*self.samp_line))
        self.short_sync_pulse_0_3_0_1.set_samp_half_line(self.samp_line/2)
        self.short_sync_pulse_0_3_0_0_0.set_samp_half_line(self.samp_line/2)
        self.short_sync_pulse_0_3_0_0.set_samp_half_line(self.samp_line/2)
        self.short_sync_pulse_0_3_0.set_samp_half_line(self.samp_line/2)

    def get_sub_freq(self):
        return self.sub_freq

    def set_sub_freq(self, sub_freq):
        self.sub_freq = sub_freq

    def get_samp_visual_delay(self):
        return self.samp_visual_delay

    def set_samp_visual_delay(self, samp_visual_delay):
        self.samp_visual_delay = samp_visual_delay

    def get_samp_h_sync(self):
        return self.samp_h_sync

    def set_samp_h_sync(self, samp_h_sync):
        self.samp_h_sync = samp_h_sync

    def get_samp_burst_delay(self):
        return self.samp_burst_delay

    def set_samp_burst_delay(self, samp_burst_delay):
        self.samp_burst_delay = samp_burst_delay

    def get_samp_burst(self):
        return self.samp_burst

    def set_samp_burst(self, samp_burst):
        self.samp_burst = samp_burst

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0_0.set_gain(self.rf_gain, 0)

    def get_lines_visual(self):
        return self.lines_visual

    def set_lines_visual(self, lines_visual):
        self.lines_visual = lines_visual

    def get_lines_half_frame(self):
        return self.lines_half_frame

    def set_lines_half_frame(self, lines_half_frame):
        self.lines_half_frame = lines_half_frame

    def get_level_blank(self):
        return self.level_blank

    def set_level_blank(self, level_blank):
        self.level_blank = level_blank
        self.analog_const_source_x_0_0_3_0_1.set_offset(self.level_blank)
        self.analog_const_source_x_0_0_3_0_0_0.set_offset(self.level_blank)
        self.analog_const_source_x_0_0_3_0_0.set_offset(self.level_blank)
        self.analog_const_source_x_0_0_3_0.set_offset(self.level_blank)

    def get_level_black(self):
        return self.level_black

    def set_level_black(self, level_black):
        self.level_black = level_black
        self.blocks_add_const_vxx_0_0.set_k((self.level_black, ))
        self.blocks_add_const_vxx_0.set_k((self.level_black, ))

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0_0.set_if_gain(self.if_gain, 0)

    def get_color_offset(self):
        return self.color_offset

    def set_color_offset(self, color_offset):
        self.color_offset = color_offset

    def get_color_ampl(self):
        return self.color_ampl

    def set_color_ampl(self, color_ampl):
        self.color_ampl = color_ampl
        self.analog_sig_source_x_0.set_amplitude(self.color_ampl)

    def get_burst_ampl(self):
        return self.burst_ampl

    def set_burst_ampl(self, burst_ampl):
        self.burst_ampl = burst_ampl
        self.analog_const_source_x_0_0_2_0_0_0.set_offset((-1+1j)/sqrt(2)*self.burst_ampl)
        self.analog_const_source_x_0_0_1_0_0_0.set_offset((-1-1j)/sqrt(2)*self.burst_ampl)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_sink_0_0.set_bb_gain(self.bb_gain, 0)


def main(top_block_cls=pal_transmit, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
