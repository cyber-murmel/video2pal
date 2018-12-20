#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pal Transmit Block
# Generated: Mon Oct 22 23:56:13 2018
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import pmt


class pal_transmit_block(gr.top_block):

    def __init__(self, path_fifo_u='', path_fifo_v='', path_fifo_y=''):
        gr.top_block.__init__(self, "Pal Transmit Block")

        ##################################################
        # Parameters
        ##################################################
        self.path_fifo_u = path_fifo_u
        self.path_fifo_v = path_fifo_v
        self.path_fifo_y = path_fifo_y

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = int(13.5e6)
        self.rf_gain = rf_gain = 14
        self.if_gain = if_gain = 48

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf=0' )
        self.osmosdr_sink_0_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0_0.set_center_freq(180e6, 0)
        self.osmosdr_sink_0_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0_0.set_bb_gain(24, 0)
        self.osmosdr_sink_0_0.set_antenna('', 0)
        self.osmosdr_sink_0_0.set_bandwidth(0, 0)

        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_short_to_float_0_0_0 = blocks.short_to_float(1, 2**8)
        self.blocks_short_to_float_0_0 = blocks.short_to_float(1, 2**8)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 2**8)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 2)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1/(1+0.339), ))
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_short*1, path_fifo_v, False)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_short*1, path_fifo_y, True)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, path_fifo_u, False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_vff((-0.5, ))
        self.blocks_add_const_vxx_1 = blocks.add_const_vff((-0.5, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((0.339, ))
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 4433618.75, 0.5, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(864, analog.GR_SQR_WAVE, 1, 2, -1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_short_to_float_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_short_to_float_0_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_short_to_float_0_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_short_to_float_0_0_0, 0), (self.blocks_add_const_vxx_1_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.osmosdr_sink_0_0, 0))

    def get_path_fifo_u(self):
        return self.path_fifo_u

    def set_path_fifo_u(self, path_fifo_u):
        self.path_fifo_u = path_fifo_u
        self.blocks_file_source_0.open(self.path_fifo_u, False)

    def get_path_fifo_v(self):
        return self.path_fifo_v

    def set_path_fifo_v(self, path_fifo_v):
        self.path_fifo_v = path_fifo_v
        self.blocks_file_source_0_1.open(self.path_fifo_v, False)

    def get_path_fifo_y(self):
        return self.path_fifo_y

    def set_path_fifo_y(self, path_fifo_y):
        self.path_fifo_y = path_fifo_y
        self.blocks_file_source_0_0.open(self.path_fifo_y, True)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0_0.set_gain(self.rf_gain, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0_0.set_if_gain(self.if_gain, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--path-fifo-u", dest="path_fifo_u", type="string", default='',
        help="Set path_fifo_u [default=%default]")
    parser.add_option(
        "", "--path-fifo-v", dest="path_fifo_v", type="string", default='',
        help="Set path_fifo_v [default=%default]")
    parser.add_option(
        "", "--path-fifo-y", dest="path_fifo_y", type="string", default='',
        help="Set path_fifo_y [default=%default]")
    return parser


def main(top_block_cls=pal_transmit_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(path_fifo_u=options.path_fifo_u, path_fifo_v=options.path_fifo_v, path_fifo_y=options.path_fifo_y)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
