#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pal Transmit Block
# Generated: Sat Oct  6 22:37:51 2018
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

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import pmt
import sip
import sys
from gnuradio import qtgui


class pal_transmit_block(gr.top_block, Qt.QWidget):

    def __init__(self, path_fifo_u='', path_fifo_v='', path_fifo_y=''):
        gr.top_block.__init__(self, "Pal Transmit Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Pal Transmit Block")
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

        self.settings = Qt.QSettings("GNU Radio", "pal_transmit_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.path_fifo_u = path_fifo_u
        self.path_fifo_v = path_fifo_v
        self.path_fifo_y = path_fifo_y

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 13.5e6
        self.rf_gain = rf_gain = 14
        self.if_gain = if_gain = 48

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	864*625, #size
        	samp_rate, #samp_rate
        	"Y", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.1, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
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
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1/1.7, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1, ))
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_short*1, path_fifo_v, False)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_short*1, path_fifo_y, True)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, path_fifo_u, False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_short_to_float_0_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_short_to_float_0_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.osmosdr_sink_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_short_to_float_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_short_to_float_0_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pal_transmit_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

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
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.osmosdr_sink_0_0.set_sample_rate(self.samp_rate)

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

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(path_fifo_u=options.path_fifo_u, path_fifo_v=options.path_fifo_v, path_fifo_y=options.path_fifo_y)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
