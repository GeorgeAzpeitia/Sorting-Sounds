import sys
class Bubble_Sort(object):
  """A basic implementation of bubble sort.
     We have to use a step function to correctly
     implement the bubble sort in a manner that
     allows the canvas object to callback the step
     function for every step of animation
  """
  name = 'Bubble Sort'
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.arr.algo_name = self.name
    self.arr.updatestats()
    self.finished = False
    self.swapping = False

    self.i = 0
    self.j = 0
    self.n = self.arr.size - 1

  def step(self):
    if not self.swapping:
      self.arr.compared(self.j, self.j + 1)
      if self.arr.val(self.j) > self.arr.val(self.j + 1):
        self.swapping = True
    else:
        self.arr.swap(self.j, self.j + 1)
        self.swapping = False

    if not self.swapping: 
      self.j += 1
      if self.j >= self.n:
        self.j = 0
        self.n -= 1
        self.i += 1

    if self.i <= self.arr.size - 1:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False
      print 'done'

  def begin(self):
    self.step()

class Selection_Sort(object):
  """docstring for Selection_Sort"""
  name = 'Selection Sort'
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr
    self.finished = False
    self.arr.algo_name = self.name
    self.arr.updatestats()

    self.min_idx = 0
    self.sorted_idx = 0
    self.j = 1
    self.n = self.arr.size

  def begin(self):
    self.config.last_inst = self.master.after(0, self.step)

  def step(self):
    self.arr.compared(self.min_idx, self.j)
    if self.arr.val(self.min_idx) > self.arr.val(self.j):
      self.min_idx = self.j
    self.j += 1
    if self.j == self.n:
      self.arr.swap(self.sorted_idx, self.min_idx)
      self.sorted_idx += 1
      self.min_idx = self.sorted_idx
      self.j = self.min_idx + 1
    if self.sorted_idx != self.n - 1:
      self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()
      print "Selection Sort Complete"
    
class Insertion_Sort(object):
  """docstring for Insertion_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Heap_Sort(object):
  """docstring for Heap_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Merge_Sort(object):
  """docstring for Merge_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.config.last_inst = self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Quick_Sort(object):
  """
  docstring for Quick_Sort
  Not yet implemented
  """
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Shell_Sort(object):
  """docstring for Shell_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Radix_Sort(object):
  """docstring for Radix_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)

class Cocktail_Sort(object):
  """docstring for Cocktail_Sort"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr

  def begin(self):
    self.master.after(0, self.step)

  def step(self):
    pass
    #if not self.finished:
    # self.master.after(self.arr.delay, self.step)