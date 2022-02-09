# from oscpy.server import OSCThreadServer
from time import sleep
# from oscpy.client import OSCClient
from datetime import datetime, date
# Visulisation
import sys
from PyQt5.QtWidgets import *
from visual import DiskPanel

# Initialisation
# osc = OSCThreadServer()
# sock = osc.listen(address='127.0.0.1', port=9002, default=True)
x_pos, x_move = [0.0, 0.0]
t1 = datetime.now()

# Panel
app = QApplication(sys.argv)
disk = DiskPanel()
disk.show()

def callback(OVTK_GDF_Right):
  OVTK_GDF_Left = 1-OVTK_GDF_Right
  print("Left prediction : ", round(OVTK_GDF_Left, 2),
          "Right prediction : ", round(OVTK_GDF_Right, 2))
  global x_move, x_pos, t1
  if OVTK_GDF_Left-OVTK_GDF_Right >= 0.3:
    x_move -= 0.2*100
    t1 = datetime.now()
  elif OVTK_GDF_Right-OVTK_GDF_Left >= 0.3:
    x_move += 0.2*100
    t1 = datetime.now()
  # Timestamp
  else:
    t2 = datetime.now()
    if (t2-t1).microseconds > 200000:  # unit:0.2 second
      if x_pos > 0.0:
        x_move -= 0.1*100
      elif x_pos == 0.0:
        x_move = 0.0
      else:
        x_move += 0.1*100
    print("No thinking time:", float((t2-t1).microseconds), "microseconds")

  # Output result
  x_pos += x_move
  x_move = 0.0
  disk.sld.setValue(x_pos)
  QApplication.processEvents()
  print("Current x_pos value is:", x_pos)

  # Send cmd to Arduino
  if x_pos >= 6*100:     # at least thinking for 1.2s to change the pointer
    x_pos = 0
    print("Right targets")

  elif x_pos <= -6*100:
    x_pos = 0
    print("Left targets")
    # put your Arduino command here: 


sys.exit(app.exec_())
sleep(10)
