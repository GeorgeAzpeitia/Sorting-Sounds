
import array
import algos
import sound
import Tkinter as tk
import math
master = Tk()
width = 1200
height = math.floor(0.75 * width)

def chg_height(x):
	return math.floor(0.75 * x)


w = Canvas(master, bg = "black", width=width, height=height)
L = w.create_text((0,0), anchor="nw", fill="white", text="Width: " + str(width) + " Height: " + str(height))
array = []

for i in range(100):
	x = 12 * i
	y = chg_height(x + 12)
 	array.append((x + 1, 900, x + 11, 900-y, i))
for bar in array:
	w.create_rectangle(bar[0], bar[1], bar[2], bar[3], fill="white")
w.pack()


mainloop()