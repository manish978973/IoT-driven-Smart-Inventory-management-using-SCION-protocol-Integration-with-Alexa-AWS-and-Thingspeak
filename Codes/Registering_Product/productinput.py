#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
#import Adafruit_CharLCD as LCD

db = mysql.connector.connect(
  host="localhost",
  user="productadmin",
  passwd="raspberry",
  database="productinfo"
)

cursor = db.cursor()
reader = SimpleMFRC522()
#lcd = LCD.Adafruit_CharLCD(4, 24, 23, 17, 18, 22, 16, 2, 4);

try:
  while True:
    #lcd.clear()
    #lcd.message('Place Card to\nregister')
    print('Place Card to\nregister')
    id, text = reader.read()
    cursor.execute("SELECT id FROM products WHERE rfid_uid="+str(id))
    cursor.fetchone()

    if cursor.rowcount >= 1:
     # lcd.clear()
     # lcd.message("Overwrite\nexisting user?")
      print("Overwrite\nexisting user?")
      overwrite = input("Overwite (Y/N)? ")
      if overwrite[0] == 'Y' or overwrite[0] == 'y':
        #lcd.clear()
        #lcd.message("Overwriting user.")
        print("Overwriting products.")
        time.sleep(1)
        sql_insert = "UPDATE products SET name = %s,unitweight = %s WHERE rfid_uid=%s"
      else:
        continue;
    else:
      sql_insert = "INSERT INTO products (name,unitweight,rfid_uid) VALUES (%s, %s, %s)"
    #lcd.clear()
    #lcd.message('Enter new name')
    print("Enter new name.")
    new_name = input("Name: ")
    new_unitweight = input("UnitWeight: ")

    cursor.execute(sql_insert, (new_name,new_unitweight, id))

    db.commit()

    #lcd.clear()
    #lcd.message("User " + new_name + "\nSaved")
    print("Product " + new_name + " with " + new_unitweight + "\nSaved")
    time.sleep(2)
finally:
  GPIO.cleanup()
