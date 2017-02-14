#!/usr/bin/env python
import LCD1602

LCD1602.init(0x27,1)

def write(data):
  row, column, value = data
  LCD1602.write(row, column, "                ")
  LCD1602.write(row, column, value)
