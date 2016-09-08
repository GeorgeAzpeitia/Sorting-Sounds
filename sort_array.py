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
    self.graph_mode = self.config.appearance.get() == 1
    self.spirals = self.config.appearance.get() == 2
    self.statlabel = self.canvas.create_text(5, 0, anchor='nw', fill=self.color_scheme[-3])
    self.radius = 2 + 15 * pow((1 - (self.size / 5000.0)), 3)

    
    self.bar_width = float(self.width) / float(self.size)
   
    if (self.bar_width * Canvas_Array.spacer_ratio) < 0.25:
      self.bar_spacer_width = 0
    else:
      self.bar_spacer_width = math.ceil(self.bar_width * Canvas_Array.spacer_ratio)

    self.bar_width = (float(self.width) - (self.size - 1) * self.bar_spacer_width) / self.size 
    self.bar_slope = float(self.height - 50) / float(self.width)
    self.Build_Bars()

  def Build_Bars(self):
    vals = []
    if self.config.arr_few_unique.get():
      uniq = 4
      for i in range(1, uniq):
        vals = vals + [int(i * (float(self.size - 1) / (uniq - 1)))] * (self.size // (uniq- 1))
      vals = vals + [self.size - 1] * (self.size % (uniq- 1))
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
    #Bar Graph
    if self.config.appearance.get() == 0:    
      x0 = 0
      x1 = self.bar_width
      y1 = self.height + 1
      for val in vals:
        y0 = self.height - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=color, width=0)))
        x0 = x1 + self.bar_spacer_width
        x1 = x0 + self.bar_width
    #Point Graph
    elif self.graph_mode:
      x_bar_left = 0
      x_bar_right = self.bar_width
      for val in vals:
        x_center = float(x_bar_left + x_bar_right) / 2
        y0 = self.height - self.radius - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))
        x0 = x_center - self.radius
        x1 = x_center + self.radius
        y1 = y0 + 2 * self.radius 
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags=color, width=0)))
        x_bar_left = x_bar_right + self.bar_spacer_width
        x_bar_right = x_bar_left + self.bar_width
    #Spiral Graph
    elif self.spirals:
      self.x_center = (self.width / 2)
      self.y_center = self.height / 2
      for i in range(len(vals)):
        val = vals[i]
        x0, y0, x1, y1 = self.translate(i, val)
        # print (x, y)
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags=color, width=0)))

    

  def translate(self, x, val):
    """Takes in an array index x, and the value at that x and returns the bbox coords"""
    x = float(x) / (self.size - 1)
    val = (self.height - 20) / 2 * (float(val) / (self.size - 1))
    x, val = val * math.cos(2*math.pi*x), val * math.sin(2*math.pi*x)

    x0 = self.x_center + x - self.radius
    y0 = self.height - self.y_center + val - self.radius
    x1 = self.x_center + x + self.radius
    y1 = y0 + 2 * self.radius
    return x0, y0, x1, y1

  def get_y(self, val):
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
    if self.spirals:
      self.spiral_swap(i, j)
    else:
      self.bar_swap(i, j)
  def spiral_swap(self, i, j):
    i_val = self.val(i)
    j_val = self.val(j)
    i_x0, i_y0, i_x1, i_y1 = self.translate(j, i_val)
    j_x0, j_y0, j_x1, j_y1 = self.translate(i, j_val)
    self.canvas.coords(self.rec(i), i_x0, i_y0, i_x1, i_y1)
    self.canvas.coords(self.rec(j), j_x0, j_y0, j_x1, j_y1)
    self.bar_array[i], self.bar_array[j] = self.bar_array[j], self.bar_array[i]
    self.swaps += 1
    self.canvas.update_idletasks()
    self.updatestats()

  def bar_swap(self, i, j):
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
    for arg in args:
      self.config.sound.sound_access(self.val(arg))
      
    args = map(self.rec, args)
      
    for i in range(len(self.last_compared) - 1, -1, -1):
      self.canvas.gettags(self.last_compared[i])
      if self.last_compared[i] not in args:
        self.rec_chg_color(self.last_compared[i], self.canvas.gettags(self.last_compared[i])[0])
        self.last_compared.pop(i)

    for arg in args:
      self.canvas.tag_raise(arg)
      self.rec_chg_color(arg, self.color_scheme[-2])
      if arg not in self.last_compared:
        self.last_compared.append(arg)
    if not False:
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
        self.config.sound.sound_access(self.sorted_check_i)
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

  def replace_val(self, i, val):
    rec = self.rec(i)
    if self.spirals:
      self.canvas.coords(rec, *self.translate(i, val))
      self.bar_array[i] = (val, rec)
    else:
      y = self.get_y(val)
      x0, y0, x1, y1 = self.canvas.coords(rec)
      if self.graph_mode:
        y1 = y - 2 * self.radius
      self.canvas.coords(rec, x0, y, x1, y1)  
      self.canvas.coords(rec, x0, y, x1, y1)
      self.bar_array[i] = (val, rec)
    self.canvas.itemconfig(rec, tags=self.get_color(val))
    self.revert_color(i)
    self.canvas.update_idletasks()

    self.swaps +=1
    self.updatestats()
    



