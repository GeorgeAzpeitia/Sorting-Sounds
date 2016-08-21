
import sort_array
import algos
import sound
import Tkinter as tk
import sys
import time

class App(object):
  def __init__(self, master):
    self.master = master
    self.canvas = tk.Canvas(self.master, width=1200, height=900, bg='black')
    self.canvas.pack()
    self.arr = sort_array.Canvas_Array(self.master, self.canvas, int(sys.argv[1]), int(sys.argv[2]))
    self.canvas.pack()
    for k, v in self.arr.__dict__.items():
      print (k, v)
    self.master.after(3000, self.test)
    print "after"
    
  def test(self):
    self.bubs = Bubble_Sort(self.master, self.arr)

root = tk.Tk()
app = App(root)
root.mainloop()



















