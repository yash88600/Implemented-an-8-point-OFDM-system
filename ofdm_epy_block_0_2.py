"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.interp_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, interp_rate = 2):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.interp_block.__init__(
            self,
            name='BER Counter',   # will show up in GRC
            in_sig=[np.int8, np.int8],
            out_sig=[np.int8],
            interp = interp_rate
        )
        self.interp_rate = interp_rate
        self.set_relative_rate(interp_rate)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        error = np.bitwise_xor(input_items[0], input_items[1])
        error = np.unpackbits(error.astype('uint8'))
        pattern_list = []
        for i in range(self.interp_rate):
            pattern_list.append(error[(7-i)::8])
        output_items[0][:] = np.concatenate(pattern_list)
        return len(output_items[0])
