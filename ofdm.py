#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: YASH
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import ofdm_epy_block_0_2 as epy_block_0_2  # embedded python block
import sip



class ofdm(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.noisestd = noisestd = 0
        self.my_const = my_const = digital.constellation_8psk().base()
        self.h = h = [1.0, 0.2 + 0.3j, 0.1 - 0.05j]
        self.delay_actual_signal = delay_actual_signal = 0
        self.FFT_SIZE = FFT_SIZE = 8

        ##################################################
        # Blocks
        ##################################################

        self._noisestd_range = Range(0, 5, 0.01, 0, 200)
        self._noisestd_win = RangeWidget(self._noisestd_range, self.set_noisestd, "'noisestd'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noisestd_win)
        self._delay_actual_signal_range = Range(0, 100, 1, 0, 200)
        self._delay_actual_signal_win = RangeWidget(self._delay_actual_signal_range, self.set_delay_actual_signal, "'delay_actual_signal'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_actual_signal_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Predicted output', 'Actual output', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_histogram_sink_x_0_1 = qtgui.histogram_sink_f(
            10000,
            100,
            (-0.5),
            1.5,
            "",
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0_1.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0_1.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_1.enable_accumulate(False)
        self.qtgui_histogram_sink_x_0_1.enable_grid(True)
        self.qtgui_histogram_sink_x_0_1.enable_axis_labels(True)


        labels = ['Bit error rate', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_1_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_histogram_sink_x_0_1_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            8, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(8):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(1, h)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fft_vxx_1 = fft.fft_vcc(FFT_SIZE, True, [1]*FFT_SIZE, False, 1)
        self.fft_vxx_0 = fft.fft_vcc(FFT_SIZE, False, [1]*FFT_SIZE, False, 1)
        self.epy_block_0_2 = epy_block_0_2.blk(interp_rate=3)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(my_const)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(my_const)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, FFT_SIZE)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, FFT_SIZE)
        self.blocks_uchar_to_float_0_2 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0_0 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_SIZE)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, FFT_SIZE)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, [1]*(FFT_SIZE + 3))
        self.blocks_stream_demux_1 = blocks.stream_demux(gr.sizeof_gr_complex*1, [1]*FFT_SIZE)
        self.blocks_stream_demux_0 = blocks.stream_demux(gr.sizeof_gr_complex*1, [1]*FFT_SIZE)
        self.blocks_keep_m_in_n_0 = blocks.keep_m_in_n(gr.sizeof_gr_complex, FFT_SIZE, (FFT_SIZE + 3), 3)
        self.blocks_delay_1_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, delay_actual_signal)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 8, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noisestd, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_uchar_to_float_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.epy_block_0_2, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_keep_m_in_n_0, 0))
        self.connect((self.blocks_delay_1_0_0_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_keep_m_in_n_0, 0), (self.blocks_delay_1_0_0_0, 0))
        self.connect((self.blocks_stream_demux_0, 1), (self.blocks_stream_mux_0, 4))
        self.connect((self.blocks_stream_demux_0, 5), (self.blocks_stream_mux_0, 8))
        self.connect((self.blocks_stream_demux_0, 0), (self.blocks_stream_mux_0, 3))
        self.connect((self.blocks_stream_demux_0, 2), (self.blocks_stream_mux_0, 5))
        self.connect((self.blocks_stream_demux_0, 6), (self.blocks_stream_mux_0, 9))
        self.connect((self.blocks_stream_demux_0, 7), (self.blocks_stream_mux_0, 10))
        self.connect((self.blocks_stream_demux_0, 7), (self.blocks_stream_mux_0, 2))
        self.connect((self.blocks_stream_demux_0, 5), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_stream_demux_0, 6), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_stream_demux_0, 4), (self.blocks_stream_mux_0, 7))
        self.connect((self.blocks_stream_demux_0, 3), (self.blocks_stream_mux_0, 6))
        self.connect((self.blocks_stream_demux_1, 6), (self.qtgui_const_sink_x_0, 6))
        self.connect((self.blocks_stream_demux_1, 2), (self.qtgui_const_sink_x_0, 2))
        self.connect((self.blocks_stream_demux_1, 5), (self.qtgui_const_sink_x_0, 5))
        self.connect((self.blocks_stream_demux_1, 4), (self.qtgui_const_sink_x_0, 4))
        self.connect((self.blocks_stream_demux_1, 3), (self.qtgui_const_sink_x_0, 3))
        self.connect((self.blocks_stream_demux_1, 1), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.blocks_stream_demux_1, 7), (self.qtgui_const_sink_x_0, 7))
        self.connect((self.blocks_stream_demux_1, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.fft_vxx_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_uchar_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_uchar_to_float_0_2, 0), (self.qtgui_histogram_sink_x_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_stream_demux_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_demux_1, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.epy_block_0_2, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.epy_block_0_2, 0), (self.blocks_uchar_to_float_0_2, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_add_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_noisestd(self):
        return self.noisestd

    def set_noisestd(self, noisestd):
        self.noisestd = noisestd
        self.analog_noise_source_x_0.set_amplitude(self.noisestd)

    def get_my_const(self):
        return self.my_const

    def set_my_const(self, my_const):
        self.my_const = my_const
        self.digital_constellation_decoder_cb_0.set_constellation(self.my_const)
        self.digital_constellation_encoder_bc_0.set_constellation(self.my_const)

    def get_h(self):
        return self.h

    def set_h(self, h):
        self.h = h
        self.interp_fir_filter_xxx_0.set_taps(self.h)

    def get_delay_actual_signal(self):
        return self.delay_actual_signal

    def set_delay_actual_signal(self, delay_actual_signal):
        self.delay_actual_signal = delay_actual_signal
        self.blocks_delay_1_0_0_0.set_dly(int(self.delay_actual_signal))

    def get_FFT_SIZE(self):
        return self.FFT_SIZE

    def set_FFT_SIZE(self, FFT_SIZE):
        self.FFT_SIZE = FFT_SIZE
        self.blocks_keep_m_in_n_0.set_m(self.FFT_SIZE)
        self.blocks_keep_m_in_n_0.set_n((self.FFT_SIZE + 3))




def main(top_block_cls=ofdm, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
