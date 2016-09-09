
import random
import math
class Sort_Array(object):
  
  """
  This is the backing array that holds the data to be sorted by the
  sorting algorithms in algos.py as a tuple of the value at that index
  and the canvas shape id. It creates the necessary shapes upon the
  tkinter Canvas passed into it and updates them via methods like swap
  and replace_val. It is able to scale the shape of its figures to
  match that of the canvas that is passed in.
  """

  
  
  def __init__(self, master, canvas, config):
    self.master = master
    self.canvas = canvas
    self.config = config

    self.size = self.config.arr_size.get()
    self.color_scheme = self.config.colors_dict[self.config.color_scheme.get()]
    self.width = int(self.canvas['width'])
    self.height = int(self.canvas['height'])
    self.bar_array = []

    #A list that holds the canvas id of the last few elements that have been compared
    self.last_compared = []

    #indices used to verify that an array is sorted
    self.sorted_check_i = 0
    self.sorted_check_j = 1

    #Variables used in the display of algorithm stats
    self.comparisons = 0
    self.swaps = 0
    self.algo_name = None
    self.statlabel = self.canvas.create_text(5, 0, anchor='nw', fill=self.color_scheme[-3])

    #Which mode to be display the data in, if both false then we use bars
    self.graph_mode = self.config.appearance.get() == 1
    self.spirals = self.config.appearance.get() == 2

    #Constants scaled to the size of the array
    self.radius = 2 + 15 * pow((1 - (self.size / 5000.0)), 3)
    self.bar_width = float(self.width) / float(self.size)

    #size of the gap between bars as a percentage of bar size
    self.spacer_ratio = 0.05
    
    #The if the array has too many elements the spacer takes up too much space
    #so we just get rid of it
    if (self.bar_width * self.spacer_ratio) < 0.15:
      self.bar_spacer_width = 0
    else:
      self.bar_spacer_width = math.ceil(self.bar_width * self.spacer_ratio)

    #However, we now need to recalculate the width of the bars with the new spacer in mind
    self.bar_width = (float(self.width) - (self.size - 1) * self.bar_spacer_width) / self.size 
    self.bar_slope = float(self.height - 50) / float(self.width)
    self.Build_Display()

  def Build_Display(self):
    """
    Constructs the initial array and then creates the necessary shapes on the
    on the canvas. It reads the selected display style and initial sorting from
    user selections in the interface.
    """
    vals = []

    if self.config.arr_few_unique.get():
      #array is to have few unique values
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
        color = self.get_color(val)
        self.bar_array.append((val, self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags=color, width=0)))

  def translate(self, i, val):
    """
    Translates a given index and value into bbox coordinates of where the point
    should be in the polar coordinate plane.
    """
    i = float(i) / (self.size - 1)
    val = (self.height - 30) / 2 * (float(val) / (self.size - 1))
    i, val = val * math.cos(2*math.pi*i), val * math.sin(2*math.pi*i)

    x0 = self.x_center + i - self.radius
    y0 = self.height - self.y_center + val - self.radius
    x1 = self.x_center + i + self.radius
    y1 = y0 + 2 * self.radius
    return x0, y0, x1, y1

  def get_y(self, val):
    """
    Takes a value and returns the y canvas coordinate for that value, only to be
    used with the bar and point graph display modes. Val is expected to be within
    [0, size)
    """
    return self.height - (self.bar_slope * (self.bar_width + ((self.bar_width + self.bar_spacer_width) * val)))

  def updatestats(self, extra=''):
    """
    Updates the label containing all the stats for the array, takes an optional
    string parameter to display algorithm specific statistics.
    """
    stats = "{0}:\nComparisons: {1}  Swaps: {2}  Delay: {3}ms\n{4}".format(self.algo_name, self.comparisons, self.swaps, self.config.delay.get(), extra)
    self.canvas.itemconfig(self.statlabel, text=stats)
    self.canvas.update_idletasks()

  def get_color(self, val):
    """
    Matches a value with its corresponding color, this allows for proper display
    of the color gradients used in the various color schemes.
    """
    color_count = len(self.color_scheme) - 3
    x = int(math.floor(val / (float(self.size) / color_count)))
    return self.color_scheme[x]

  def swap(self, i, j):
    """
    A dispatch function for swaps, needed because the spiral display
    cannot be swapped normally.
    """
    if self.spirals:
      self.spiral_swap(i, j)
    else:
      self.bar_swap(i, j)

  def spiral_swap(self, i, j):
    """
    Swaps the position of two points at indices i and j, only to be used with 
    the spiral display mode.
    """
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
    """Swaps the bars/points at indices i and j"""
    i_x0, i_y0, i_x1, i_y1 = self.canvas.coords(self.rec(i))
    j_x0, j_y0, j_x1, j_y1 = self.canvas.coords(self.rec(j))
    self.canvas.move(self.rec(i), j_x0 - i_x0, 0)
    self.canvas.move(self.rec(j), i_x0 - j_x0, 0)
    self.bar_array[i], self.bar_array[j] = self.bar_array[j], self.bar_array[i]
    self.swaps += 1
    self.canvas.update_idletasks()
    self.updatestats()

  def rec_chg_color(self, addr, color):
    """Changes the color of a shape given the canvas id of that shape"""
    self.canvas.itemconfig(addr, fill=color)

  def chg_color(self, i, color):
    """Changes the color of a shape at index i"""
    self.canvas.itemconfig(self.rec(i), fill=color)

  def revert_color(self, i):
    """
    Reverts the color of a shape to the color it was tagged with. This will 
    usually be the color corresponding to the value of that shape
    """
    self.chg_color(i, self.canvas.gettags(self.rec(i))[0])

  def val(self, i):
    """returns the val of the shape at index i """
    return self.bar_array[i][0]

  def rec(self, i):
    """returns the canvas id of shape at index i"""
    return self.bar_array[i][1]

  def compared(self, *args):
    """
    Changes the color of any number of shapes to denote that they're being compared
    and increments the comparison counter accordingly. It reverts shapes back to
    their original color if they're not being compared in subsequent calls of this
    function.
    """
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
    """
    Reverts the colors of all the shapes that were last compared.
    """
    for bar in self.last_compared:
      self.rec_chg_color(bar, self.canvas.gettags(bar)[0])
    self.last_compared = []

  def check_sorted(self):
    """
    This will check the elements of the array to verify that they're in sorted 
    order. Once called it will continue to call itself in order to finish the
    operation. When it is done it will wait for 0.75s and then revert the array
    to its original colors. 
    """
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
    """
    Given a value and an index it will replace the value at that that index and
    adjust the shape accordingly.
    """
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
    



