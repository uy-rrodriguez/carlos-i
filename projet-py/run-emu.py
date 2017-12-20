#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, traceback
from emu import emu

if __name__ == '__main__':
    try:
        emu.run()
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
