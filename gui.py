
import sort_array
import algos
import sound
import Tkinter as tk
import sys

master = tk.Tk()
width = 1000
height = 1000

w = tk.Canvas(master, bg = "black", width=width, height=height)
w.pack()

L = w.create_text((0,0), anchor="nw", fill="white", text="Width: " + str(width) + " Height: " + str(height))

test = sort_array.Canvas_Array(w, int(sys.argv[1]))
for k, v in test.__dict__.items():
  print (k, v)
# array = []

# for i in range(100):
# 	x = 12 * i
# 	y = chg_height(x + 12)
#  	array.append((x + 1, 900-y, x + 13, 901 , i))
#  	if i == 100:
#  		print str(x+12)

# for bar in array:
# 	w.create_rectangle(bar[0], bar[1], bar[2], bar[3], fill="white")
# master.after

tk.mainloop()