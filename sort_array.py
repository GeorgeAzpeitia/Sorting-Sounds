import math
import random
import time

class Canvas_Array(object):
  """docstring for Array"""
  #size of the gap between bars, should be kept between 0 and 0.25
  spacer_ratio = 0.05 
  #animation delay in ms
  delay = 0.5
  def __init__(self, master, canvas, size, rand):
    self.master = master
    self.canvas = canvas
    self.size = size
    self.width = int(self.canvas['width'])
    self.height = int(self.canvas['height'])

    #Temporary solution until I figure out how to display an array with more elements
    #than the width of the window
    if self.size > self.width: 
      self.size = self.width
    
    self.bar_width = float(self.width) / float(self.size)
   
    if (self.bar_width * Canvas_Array.spacer_ratio) < 0.25:
      self.bar_spacer_width = 0
    else:
      self.bar_spacer_width = math.ceil(self.bar_width * Canvas_Array.spacer_ratio)

    self.bar_width = (float(self.width) - (self.size - 1) * self.bar_spacer_width) / self.size 
    self.bar_slope = float(self.height) / float(self.width)
    vals = range(self.size)
    if rand:
        random.shuffle(vals)
    self.bar_array = []
   #bar_width should never be < 1
    if self.bar_width <= 1:
      x0 = 0
      x1 = 0
      y1 = self.height - 1
      
      for val in vals:
        y0 = self.height - (val * self.bar_slope)
        self.bar_array.append((val, self.canvas.create_line(x0, y0, x1, y1, fill='white')))
        x0 += 1
        x1 += 1

    else:
      x0 = 0
      x1 = self.bar_width + 1
      y1 = self.height + 1
      for val in vals:

        fill = 'white'
        # if (val + 1) % 5 == 0:
        #   fill = 'blue'
        #   # print "i % 5 = " + str(val + 1)
        # if (val + 1) % 10 == 0: 
        #   fill = 'red'
        #   # print "i % 9 = " + str(val + 1)
        
        y0 = self.height - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))
        self.bar_array.append((val, self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=0)))
        x0 = x1 + self.bar_spacer_width
        x1 = x0 + self.bar_width

  def swap(self, i, j):
    """Swaps the bars at positions i and j"""
    i_x0, i_y0, i_x1, i_y1 = self.canvas.coords(self.bar_array[i][1])
    j_x0, j_y0, j_x1, j_y1 = self.canvas.coords(self.bar_array[j][1])
    print str(j_x0) +" " +  str(i_x0)
    self.canvas.move(self.bar_array[i][1], j_x0 - i_x0, 0)
    self.canvas.move(self.bar_array[j][1], i_x0 - j_x0, 0)
    tmp = self.bar_array[i]
    self.bar_array[i] = self.bar_array[j]
    self.bar_array[j] = tmp
    # time.sleep(self.delay)

  def chg_color(self, addr, color):
    """Changes the color of the bar at position i"""
    self.canvas.itemconfig(addr, fill=color)

  def val(self, i):
    """returns the val of the bar at index i """
    return self.bar_array[i][0]

  def compared(self, i, j):
    """colors two bars red to show they're being compared for 20 * delay ms"""
    # print "comparing : " + str(i) + " " + str(j)
    # i_color = self.canvas.itemcget(self.bar_array[i][1], 'fill')
    j_color = self.canvas.itemcget(self.bar_array[j][1], 'fill')
    # print i_color + " " + j_color
    # self.chg_color(i, 'red')
    addr = self.bar_array[j][1]
    self.chg_color(addr, 'red')
    # self.master.after(300, self.chg_color, i, 'white')
    self.master.after(50, self.chg_color, addr, 'white')
    # time.sleep(self.delay)


