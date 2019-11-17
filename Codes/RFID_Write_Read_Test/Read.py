#!/usr/bin/env python

import RPi.GPIO as GPIO

from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
  while True:
         id, text = reader.read()
         print(id)
         print(text)


finally:
        GPIO.cleanup()



