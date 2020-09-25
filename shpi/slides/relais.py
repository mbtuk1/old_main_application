#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import pi3d
import json
import logging

from .. import config  # TODO need this import?
from ..core import peripherals
from ..core import graphics
from ..core import mqttclient

try:
    import urllib.request as urlopen
except:
    from urllib2 import urlopen

try:
    unichr
except NameError:
    unichr = chr


def get_relay_status(relay):
    try:
        value = peripherals.read_one_byte(relay.read)
    except:
        logging.error('Error relay status')
        relay.status = 'error'
    else:
        if value == peripherals.VALS.get('OFF'):
            relay.status = 'OFF'
        else:
            relay.status = 'ON'


def press_switch(relay):
    if relay.status == 'ON':
        try:
            peripherals.write_32u4(relay.write, peripherals.VALS.get('OFF'),"switch relay off")
        except:
            logging.error('Error relay off')
        else:
            relay.status = 'OFF'
            relay.colouring.set_colour([1,1,1])
    else:
        try:
            peripherals.write_32u4(relay.write, peripherals.VALS.get('ON'),"switch relay on")
        except:
            logging.error('Error relay on')
        else:
            relay.status = 'ON'
            relay.colouring.set_colour([0,1,0])


##################################################################
# relay1
textR1 = pi3d.PointText(graphics.pointFont, graphics.CAMERA,
                      max_chars=35, point_size=128)
# also big font possible, higher resolution
text2R1 = pi3d.PointText(graphics.pointFontbig,
                       graphics.CAMERA, max_chars=35, point_size=256)

# look for graphics in core/graphics.py  0xE00F -> light,   0xE001 -> circle
relay1 = pi3d.TextBlock(-225, 0, 0.1, 0.0, 1, text_format=unichr(
    0xE00F), size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

#titleR1 = pi3d.TextBlock(-200, 60, 0.1, 0.0, 15, text_format=str(config.RELAY1_NAME),
#                size=0.79, spacing="C", space=0.05, colour=(1.0, 1.0, 1.0, 1.0))

circleR1 = pi3d.TextBlock(-230, 15, 0.1, 0.0, 1, text_format=unichr(0xE001),
                        size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

textR1.add_text_block(relay1)
#textR1.add_text_block(titleR1)
text2R1.add_text_block(circleR1)

##################################################################
# relay2

textR2 = pi3d.PointText(graphics.pointFont, graphics.CAMERA,
                      max_chars=35, point_size=128)
text2R2 = pi3d.PointText(graphics.pointFontbig,
                       graphics.CAMERA, max_chars=35, point_size=256)
relay2 = pi3d.TextBlock(0, 0, 0.1, 0.0, 1, text_format=unichr(
    0xE00F), size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

#titleR2 = pi3d.TextBlock(-200, 60, 0.1, 0.0, 15, text_format=config.RELAY2_NAME,
#                size=0.79, spacing="C", space=0.05, colour=(1.0, 1.0, 1.0, 1.0))

circleR2 = pi3d.TextBlock(-5, 15, 0.1, 0.0, 1, text_format=unichr(0xE001),
                        size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

textR2.add_text_block(relay2)
#textR2.add_text_block(titleR2)
text2R2.add_text_block(circleR2)

##################################################################
# relay3

textR3 = pi3d.PointText(graphics.pointFont, graphics.CAMERA,
                      max_chars=35, point_size=128)
text2R3 = pi3d.PointText(graphics.pointFontbig,
                       graphics.CAMERA, max_chars=35, point_size=256)
relay3 = pi3d.TextBlock(225, 0, 0.1, 0.0, 1, text_format=unichr(
    0xE00F), size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

#titleR3 = pi3d.TextBlock(-200, 60, 0.1, 0.0, 15, text_format=config.RELAY3_NAME,
#                size=0.79, spacing="C", space=0.05, colour=(1.0, 1.0, 1.0, 1.0))

circleR3 = pi3d.TextBlock(220, 15, 0.1, 0.0, 1, text_format=unichr(0xE001),
                        size=0.99, spacing="C", space=0.6, colour=(1, 1, 1, 1))

textR3.add_text_block(relay3)
#textR3.add_text_block(titleR3)
text2R3.add_text_block(circleR3)

##################################################################

# set read and write locations
relay1.read = peripherals.READ_RELAY1
relay1.write = peripherals.RELAY1
relay2.read = peripherals.READ_RELAY2
relay2.write = peripherals.RELAY2
relay3.read = peripherals.READ_RELAY3
relay3.write = peripherals.RELAY3

# set iniital status to unknown
relay1.status = 'unknown'
relay2.status = 'unknown'
relay3.status = 'unknown'

def inloop(textchange=False, activity=False, offset=0):

    if textchange:
        textR1.regen()
        text2R1.regen()

        textR2.regen()
        text2R2.regen()

        textR3.regen()
        text2R3.regen()
    
    if relay1.status == 'unknown':
        get_relay_status(relay1)
    if relay1.status == 'error':
        relay1.colouring.set_colour([0, 0, 1])

    if relay2.status == 'unknown':
        get_relay_status(relay2)
    if relay2.status == 'error':
        relay2.colouring.set_colour([0, 0, 1])

    if relay3.status == 'unknown':
        get_relay_status(relay3)
    if relay3.status == 'error':
        relay3.colouring.set_colour([0, 0, 1])

    if peripherals.check_touch_pressed():
        if peripherals.clicked(relay1.x, relay1.y):
            press_switch(relay1)
        elif peripherals.clicked(relay2.x, relay2.y):
            press_switch(relay2)
        elif peripherals.clicked(relay3.x, relay3.y):
            press_switch(relay3)
    
    if offset != 0:
        graphics.slider_change(text2R1.text, offset)
        offset = graphics.slider_change(textR1.text, offset)

        if offset == 0:
            textR1.regen()
            text2R1.regen()

        graphics.slider_change(text2R2.text, offset)
        offset = graphics.slider_change(textR2.text, offset)

        if offset == 0:
            textR2.regen()
            text2R2.regen()

        graphics.slider_change(text2R3.text, offset)
        offset = graphics.slider_change(textR3.text, offset)

        if offset == 0:
            textR3.regen()
            text2R3.regen()
    

    textR1.draw()
    text2R1.draw()

    textR2.draw()
    text2R2.draw()

    textR3.draw()
    text2R3.draw()    

    return activity, offset
