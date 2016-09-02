import random
import math
class Canvas_Array(object):
  """docstring for Array"""
  #size of the gap between bars, should be kept between 0 and 0.25
  spacer_ratio = 0.05 
  
  def __init__(self, master, canvas, config):
    self.master = master
    self.canvas = canvas
    self.config = config

    self.size = self.config.arr_size.get()
    self.color_scheme = self.config.colors_dict[self.config.color_scheme.get()]
    self.width = int(self.canvas['width'])
    self.height = int(self.canvas['height'])
    self.bar_array = []
    self.last_compared = []
    self.sorted_check_i = 0
    self.sorted_check_j = 1
    self.comparisons = 0
    self.swaps = 0
    self.algo_name = None
    self.statlabel = self.canvas.create_text(5, 0, anchor='nw', fill=self.color_scheme[-3])
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
    self.Build_Bars()

  def Build_Bars(self):
    vals = []
    if self.config.arr_few_unique.get():
      uniq = 4
      for i in range(1, uniq):
        vals = vals + [int(i * (float(self.size) / (uniq - 1)))] * (self.size // (uniq- 1))
      vals = vals + [self.size] * (self.size % (uniq- 1))
      assert len(vals) == (self.size)
    else:
      vals = range(self.size)

    if self.config.arr_sorting.get() == 0:
      #array is randomized      
      random.shuffle(vals)
    elif self.config.arr_sorting.get() == 1:
      #array is reverse ordered
      vals.reverse()
    elif self.config.arr_sorting.get() == 3:
      #array is almost sorted
      for i in range(int(math.ceil(self.size * 0.125))):
        i = random.randrange(0, self.size)
        j = random.randrange(0, self.size)
        vals[i], vals[j] = vals[j], vals[i]
    if self.bar_width <= 1:
      x0 = 0
      x1 = 0
      y1 = self.height - 1
      
      for val in vals:
        y0 = self.height - (val * self.bar_slope)
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_line(x0, y0, x1, y1, fill=color, tags=color)))
        x0 += 1
        x1 += 1
    else:
      x0 = 0
      x1 = self.bar_width
      y1 = self.height + 1
      for val in vals:
        y0 = self.height - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=color, width=0)))
        x0 = x1 + self.bar_spacer_width
        x1 = x0 + self.bar_width
        
  def get_y(self, val):
    if self.bar_width <= 1:
      return self.height - (val * self.bar_slope)
    else:
      return self.height - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))
  def updatestats(self):
    stats = "{0}:\nComparisons: {1}  Swaps: {2}  Delay: {3}ms".format(self.algo_name, self.comparisons, self.swaps, self.config.delay.get())
    self.canvas.itemconfig(self.statlabel, text=stats)
    self.canvas.update_idletasks()

  def get_color(self, val):
    color_count = len(self.color_scheme) - 3
    x = int(math.floor(val / (float(self.size) / color_count)))
    # if x == color_count: x = color_count - 1
    return self.color_scheme[x]

  def swap(self, i, j):
    """Swaps the bars at positions i and j"""
    i_x0, i_y0, i_x1, i_y1 = self.canvas.coords(self.rec(i))
    j_x0, j_y0, j_x1, j_y1 = self.canvas.coords(self.rec(j))
    self.canvas.move(self.rec(i), j_x0 - i_x0, 0)
    self.canvas.move(self.rec(j), i_x0 - j_x0, 0)
    self.bar_array[i], self.bar_array[j] = self.bar_array[j], self.bar_array[i]
    self.swaps += 1
    self.canvas.update_idletasks()
    self.updatestats()

  def rec_chg_color(self, addr, color):
    """Changes the color of the bar at position i"""
    self.canvas.itemconfig(addr, fill=color)

  def chg_color(self, i, color):
    self.canvas.itemconfig(self.rec(i), fill=color)

  def revert_color(self, i):
    self.chg_color(i, self.canvas.gettags(self.rec(i))[0])

  def val(self, i):
    """returns the val of the bar at index i """
    return self.bar_array[i][0]

  def rec(self, i):
    return self.bar_array[i][1]

  def compared(self, *args):
    """colors two bars red to show they're being compared"""
    args = map(self.rec, args)
      
    for i in range(len(self.last_compared) - 1, -1, -1):
      self.canvas.gettags(self.last_compared[i])
      if self.last_compared[i] not in args:
        self.rec_chg_color(self.last_compared[i], self.canvas.gettags(self.last_compared[i])[0])
        self.last_compared.pop(i)

    for arg in args:
      self.rec_chg_color(arg, self.color_scheme[-2])
      if arg not in self.last_compared:
        self.last_compared.append(arg)

    self.comparisons += 1
    self.canvas.update_idletasks()
    self.updatestats()

  def clear_compared(self):
    for bar in self.last_compared:
      self.rec_chg_color(bar, self.canvas.gettags(bar)[0])
    self.last_compared = []

  def check_sorted(self):
    self.chg_color(self.sorted_check_i, 'green')
    if self.sorted_check_j <= self.size - 1:
      if(self.val(self.sorted_check_i) <= self.val(self.sorted_check_j)):
        self.sorted_check_i += 1
        self.sorted_check_j += 1
        self.config.last_inst = self.master.after(self.config.delay.get(), self.check_sorted)
      else:
        pass # Maybe Implement something to deal with the error case in which the array is not sorted
    else:
      if self.sorted_check_j == self.size:
        self.sorted_check_j += 1
        self.config.last_inst = self.master.after(750, self.check_sorted)
      else:
        for i in range(len(self.bar_array)):
          self.revert_color(i)
        self.config.running = False



