class Bubble_Sort(object):
  """docstring for Bubble"""
  def __init__(self, master, arr):
    self.master = master
    self.arr = arr
    self.finished = False
    self.i = 0
    self.j = 0
    self.n = self.arr.size - 1
    self.master.after(1000, self.step)

  def step(self):
    self.arr.compared(self.j, self.j + 1)
    if self.arr.val(self.j) > self.arr.val(self.j + 1):
      self.arr.swap(self.j, self.j + 1)
    self.j += 1
    if self.j >= self.n:
      self.j = 0
      self.n -= 1
      self.i += 1
    if self.i <= self.arr.size - 1:
      self.master.after(1, self.step)
    else:
      print 'done'