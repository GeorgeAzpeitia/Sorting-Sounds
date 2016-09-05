import math
import pyaudio
import numpy
class Bubble_Sort(object):
  """A basic implementation of bubble sort.
     We have to use a step function to correctly
     implement the bubble sort in a manner that
     allows the canvas object to callback the step
     function for every step of animation
  """
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.arr.algo_name = 'Bubble Sort'
    self.arr.updatestats()
    self.finished = False
    self.swapping = False
 
    self.i = 0
    self.j = 0
    self.n = self.arr.size - 1
    self.swap_cnt = 0
  def step(self):
    if not self.swapping:
      self.arr.compared(self.j, self.j + 1)
      if self.arr.val(self.j) > self.arr.val(self.j + 1):
        self.swapping = True
    else:
        self.swap_cnt += 1
        self.arr.swap(self.j, self.j + 1)
        self.swapping = False

    if not self.swapping: 
      self.j += 1
      if self.j >= self.n:
        if self.swap_cnt == 0:
          self.finished = True
        else:
          self.swap_cnt = 0
        self.j = 0
        self.n -= 1
        self.i += 1

    if self.i <= self.arr.size - 1 and not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()

class Selection_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Selection Sort'
    self.arr.updatestats()

    self.min_idx = 0
    self.sorted_idx = 0
    self.j = 1
    self.n = self.arr.size

  def step(self):
    if not self.swapping:
      self.arr.compared(self.min_idx, self.j)
      if self.arr.val(self.min_idx) > self.arr.val(self.j):
        self.min_idx = self.j
      self.j += 1
      if self.j == self.n:
        self.swapping = True
    else:
        if self.sorted_idx != self.min_idx:
          self.arr.swap(self.sorted_idx, self.min_idx)
        self.swapping = False
        self.sorted_idx += 1
        self.min_idx = self.sorted_idx
        self.j = self.min_idx + 1

    if self.sorted_idx < self.n - 1 and not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()

class Cocktail_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Cocktail Sort'
    self.arr.updatestats()

    self.i = 0
    self.j = 1
    self.top = self.arr.size - 1
    self.bottom = 0
    self.up = True
    self.swap_cnt = 0
  def step(self):
    if self.up:
      if not self.swapping:
        self.arr.compared(self.i, self.j)
        if self.arr.val(self.i) > self.arr.val(self.j):
          self.swapping = True
      else:
          self.swap_cnt += 1
          self.arr.swap(self.i, self.j)
          self.swapping = False
      if not self.swapping: 
        self.j += 1
        self.i += 1
        if self.j > self.top:
          if self.swap_cnt == 0:
            self.finished = True
          else:
            self.swap_cnt = 0
          self.top -= 1
          self.j = self.top
          self.i = self.j - 1
          self.up = False
    else:
      if not self.swapping:
        self.arr.compared(self.i, self.j)
        if self.arr.val(self.j) < self.arr.val(self.i):
          self.swapping = True
      else:
          self.swap_cnt += 1
          self.arr.swap(self.i, self.j)
          self.swapping = False
      if not self.swapping: 
        self.j -= 1
        self.i -= 1
        if self.i <= self.bottom:
          if self.swap_cnt == 0:
            self.finished = True
          else:
            self.swap_cnt = 0
          self.i = self.bottom
          self.j = self.i + 1
          self.bottom += 1
          self.up = True

    if self.bottom < self.top and not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()

class Insertion_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Insertion Sort'
    self.arr.updatestats()

    self.sorted_idx = 0
    self.i = 0
    self.j = 1

  def step(self):
    if not self.swapping:
      self.arr.compared(self.i, self.j)
      if (self.arr.val(self.j)) < self.arr.val(self.i):
        self.swapping = True
      else:
        self.sorted_idx += 1
        self.i = self.sorted_idx
        self.j = self.sorted_idx + 1
        
    else:
      self.arr.swap(self.i, self.j)
      self.swapping = False
      self.i -= 1
      self.j -= 1
      if self.i == -1:
        self.sorted_idx += 1
        self.i = self.sorted_idx
        self.j = self.sorted_idx + 1

    if self.sorted_idx < self.arr.size - 1:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True

class Heap_Sort(object):
  """docstring for Selection_Sort"""

  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Heap Sort'
    self.arr.updatestats()

    self.heap_size = self.arr.size - 1
    self.build_heap_cnt = self.parent(self.heap_size)
    self.heap_built = False
    self.leaf = self.heap_size
    self.leaves_colored = False
    self.heapifying = False
    self.sorting = True
    self.heap_var = -1
    self.swapping_i = -1
    self.swapping_j = -1
    self.layer_colors = ['#2c0b41', '#3f1b5b', '#4e1472', '#601c8a', '#752098', '#982f92', '#ba3f8d', '#dd4d87', '#eb688c', '#f18b97', '#f5aca0', '#facdaa']

  def parent(self, i):
    return (i - 1) >> 1
  def right(self, i):
    return ((i + 1) << 1)
  def left(self, i):
    return ((i + 1) << 1) - 1
  def get_layer(self, i):
    return int(math.floor(math.log(i + 1, 2)))
  def color_leaves(self):
    if self.leaf > self.build_heap_cnt:
      self.arr.canvas.itemconfig(self.arr.rec(self.leaf), tags=self.layer_colors[self.get_layer(self.leaf)])
      self.arr.chg_color(self.leaf, self.layer_colors[self.get_layer(self.leaf)])
      self.leaf -= 1
    else:
      self.leaves_colored = True

  def build_heap(self):
    if self.build_heap_cnt >= 0:
      self.heapify(self.build_heap_cnt)
      self.build_heap_cnt -= 1
    else:
      self.heap_built = True

  def heapify(self, i):
    if i <= self.heap_size and self.arr.canvas.gettags(self.arr.rec(i))[0] != self.layer_colors[self.get_layer(i)]:
      self.arr.canvas.itemconfig(self.arr.rec(i), tags=self.layer_colors[self.get_layer(i)])

    if self.left(i) <= self.heap_size:
      if self.right(i) <= self.heap_size:
        self.arr.compared(i, self.left(i), self.right(i))
      else:
        self.arr.compared(i, self.left(i))
    elif self.right(i) <= self.heap_size:
        self.arr.compared(i, self.right(i))
    else:
      self.arr.compared(i)
    if self.left(i) <= self.heap_size and self.arr.val(self.left(i)) > self.arr.val(i):
      biggest = self.left(i)
    else:
      biggest = i

    if self.right(i) <= self.heap_size and self.arr.val(self.right(i)) > self.arr.val(biggest):
      biggest = self.right(i)
    if biggest != i:
      self.swapping = True
      self.swapping_i = i
      self.swapping_j = biggest
      self.heapifying = True
      self.heap_var = biggest
    else:
      self.swapping = False
      self.heapifying = False
      self.heap_var = -1
      self.sorting = True

  def step(self):
    if not self.leaves_colored:
      self.color_leaves()
    elif not self.heap_built:
      if self.swapping:
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_j), tags=self.layer_colors[self.get_layer(self.swapping_i)])
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_i), tags=self.layer_colors[self.get_layer(self.swapping_j)])
        # self.arr.clear_compared()
        self.arr.swap(self.swapping_i, self.swapping_j)
        self.swapping = False
      elif self.heapifying:
        self.heapify(self.heap_var)
      else:
        self.build_heap()
    else:
      if self.sorting:
        self.arr.canvas.itemconfig(self.arr.rec(0), tags=self.arr.get_color(self.arr.val(0)))
        self.arr.swap(0, self.heap_size)
        self.arr.clear_compared()
        self.arr.revert_color(self.heap_size)
        self.sorting = False
        self.heapifying = True
        self.heap_var = 0
        self.heap_size -= 1
      elif self.swapping:
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_j), tags=self.layer_colors[self.get_layer(self.swapping_i)])
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_i), tags=self.layer_colors[self.get_layer(self.swapping_j)])
        self.arr.swap(self.swapping_i, self.swapping_j)
        self.swapping = False
      elif self.heapifying:
        self.heapify(self.heap_var)
    if self.heap_size > 0:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.canvas.itemconfig(self.arr.rec(0), tags=self.arr.get_color(self.arr.val(0)))
      self.arr.revert_color(0)
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True


class Merge_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Merge Sort'
    self.arr.updatestats()

    self.backing_arr = [None] * self.arr.size
    self.call_stack = [(0, (self.arr.size -1) / 2, self.arr.size - 1)]

    self.last_right = None
    self.splitting = True
    self.merging = False
    self.copying = False
    self.color_left = self.call_stack[0][0]
    self.color_mid = self.call_stack[0][1]
    self.color_right = self.call_stack[0][2]
    self.merge_left = None
    self.merge_mid = None
    self.merge_right = None
    self.merge_i = None
    self.merge_j = None
    self.merge_k = None

  def merge(self):

    if self.merge_i <= self.merge_mid and self.merge_j <= self.merge_right:
      self.arr.compared(self.merge_i, self.merge_j)
      if self.arr.val(self.merge_i) < self.arr.val(self.merge_j):
        self.backing_arr[self.merge_k] = self.arr.val(self.merge_i)
        self.merge_i += 1
        self.merge_k += 1
      else:
        self.backing_arr[self.merge_k] = self.arr.val(self.merge_j)
        self.merge_j += 1
        self.merge_k += 1
    elif self.merge_j > self.merge_right and self.merge_k <= self.merge_right:
      self.backing_arr[self.merge_k] = self.arr.val(self.merge_i)
      self.merge_i += 1
      self.merge_k += 1
    elif self.merge_i > self.merge_mid and self.merge_k <= self.merge_right:
      self.backing_arr[self.merge_k] = self.arr.val(self.merge_j)
      self.merge_j += 1
      self.merge_k += 1
    else:
      self.last_right = self.merge_right
      self.merge_k = self.merge_left
      self.arr.clear_compared()
      self.merging = False
      self.copying = True
      self.copy()



  def copy(self):
    if self.merge_k <= self.merge_right:

      new_val = self.backing_arr[self.merge_k]
      self.backing_arr[self.merge_k] = None
      new_y = self.arr.get_y(new_val)
      rec = self.arr.rec(self.merge_k)
      x0, y0, x1, y1 = self.arr.canvas.coords(rec)
      if self.arr.graph_mode:
        y1 = new_y - 2 * self.arr.radius
      self.arr.canvas.coords(rec, x0, new_y, x1, y1)
      self.arr.canvas.itemconfig(rec, tags=self.arr.get_color(new_val))
      self.arr.revert_color(self.merge_k)
      self.arr.bar_array[self.merge_k] = (new_val, rec)

      self.merge_k += 1
      self.arr.swaps += 1
      self.arr.updatestats()
    else:
      self.copying = False
      self.splitting = True
      self.split()

  def split_left(self):
    l = self.call_stack[-1][0]
    r = self.call_stack[-1][1]
    mid = (l + r) / 2
    self.call_stack.append((l, mid, r))

  def split_right(self):
    l = self.call_stack[-1][1] + 1
    r = self.call_stack[-1][2]
    mid = (l + r) / 2
    self.call_stack.append((l, mid, r))

  def makeBounds(self, l, mid, r):

    self.arr.canvas.itemconfig(self.arr.rec(self.color_left), tags=self.arr.get_color(self.arr.val(self.color_left)))
    self.arr.canvas.itemconfig(self.arr.rec(self.color_mid), tags=self.arr.get_color(self.arr.val(self.color_mid)))
    self.arr.canvas.itemconfig(self.arr.rec(self.color_right), tags=self.arr.get_color(self.arr.val(self.color_right)))
    self.arr.revert_color(self.color_left)
    self.arr.revert_color(self.color_right)
    self.arr.revert_color(self.color_mid)

    self.color_left, self.color_mid, self.color_right = l, mid, r

    self.arr.canvas.itemconfig(self.arr.rec(self.color_left), tags='green')
    self.arr.canvas.itemconfig(self.arr.rec(self.color_mid), tags='blue')
    self.arr.canvas.itemconfig(self.arr.rec(self.color_right), tags='green')
    self.arr.chg_color(self.color_left, 'green')
    self.arr.chg_color(self.color_mid, 'blue')
    self.arr.chg_color(self.color_right, 'green')

  def split(self):
    if len(self.call_stack) == 0:
      self.finished = True
      return
    l, mid, r = self.call_stack[-1]
    self.makeBounds(l, mid, r)

    if r - l == 0 or r - l == 1:
      self.merge_left = l
      self.merge_mid = mid
      self.merge_right = r
      self.merge_i = l
      self.merge_k = l
      self.merge_j = mid + 1
      self.call_stack.pop()
      self.splitting = False
      self.merging = True
      self.merge()
      #pop and merge

    elif self.last_right == r:
      #pop and merge
      self.merge_left = l
      self.merge_mid = mid
      self.merge_right = r
      self.merge_i = l
      self.merge_k = l
      self.merge_j = mid + 1
      self.call_stack.pop()
      self.splitting = False
      self.merging = True
      self.merge()
    elif self.last_right == mid:
      #split right
      self.split_right()
    else:
      self.split_left()
      #split left

  def step(self):
    if self.splitting:
      self.split()
    elif self.merging:
      self.merge()
    elif self.copying:
      self.copy()
    else:
      self.finished = True

    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True

class Merge_Sort_Iter(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Merge Sort (Iterative)'
    self.arr.updatestats()

    self.backing_arr = [None] * self.arr.size
    self.merge_size = 1
    self.splitting = True
    self.merging = False
    self.copying = False
    self.color_left = 0
    self.color_mid = 0
    self.color_right = 0
    self.merge_l_start = 0
    self.merge_left = 0
    self.merge_mid = None
    self.merge_right = None
    self.merge_i = None
    self.merge_j = None
    self.merge_k = None

  def merge(self):
    if self.merge_i <= self.merge_mid and self.merge_j <= self.merge_right:
      self.arr.compared(self.merge_i, self.merge_j)
      if self.arr.val(self.merge_i) < self.arr.val(self.merge_j):
        self.backing_arr[self.merge_k] = self.arr.val(self.merge_i)
        self.merge_i += 1
        self.merge_k += 1
      else:
        self.backing_arr[self.merge_k] = self.arr.val(self.merge_j)
        self.merge_j += 1
        self.merge_k += 1
    elif self.merge_j > self.merge_right and self.merge_k <= self.merge_right:
      self.backing_arr[self.merge_k] = self.arr.val(self.merge_i)
      self.merge_i += 1
      self.merge_k += 1
    elif self.merge_i > self.merge_mid and self.merge_k <= self.merge_right:
      self.backing_arr[self.merge_k] = self.arr.val(self.merge_j)
      self.merge_j += 1
      self.merge_k += 1
    else:
      self.merge_k = self.merge_left
      self.arr.clear_compared()
      self.merging = False
      self.copying = True
      self.copy()



  def copy(self):
    if self.merge_k <= self.merge_right:
      new_val = self.backing_arr[self.merge_k]
      self.backing_arr[self.merge_k] = None
      new_y = self.arr.get_y(new_val)
      rec = self.arr.rec(self.merge_k)
      x0, y0, x1, y1 = self.arr.canvas.coords(rec)
      if self.arr.graph_mode:
        y1 = new_y - 2 * self.arr.radius
      self.arr.canvas.coords(rec, x0, new_y, x1, y1)
      self.arr.canvas.itemconfig(rec, tags=self.arr.get_color(new_val))
      self.arr.revert_color(self.merge_k)
      self.arr.bar_array[self.merge_k] = (new_val, rec)

      self.merge_k += 1
      self.arr.swaps += 1
      self.arr.updatestats()
    else:
      self.copying = False
      self.splitting = True
      self.split()

  def makeBounds(self, l, mid, r):

    self.arr.canvas.itemconfig(self.arr.rec(self.color_left), tags=self.arr.get_color(self.arr.val(self.color_left)))
    self.arr.canvas.itemconfig(self.arr.rec(self.color_mid), tags=self.arr.get_color(self.arr.val(self.color_mid)))
    self.arr.canvas.itemconfig(self.arr.rec(self.color_right), tags=self.arr.get_color(self.arr.val(self.color_right)))
    self.arr.revert_color(self.color_left)
    self.arr.revert_color(self.color_right)
    self.arr.revert_color(self.color_mid)

    self.color_left, self.color_mid, self.color_right = l, mid, r

    self.arr.canvas.itemconfig(self.arr.rec(self.color_mid), tags='blue')
    self.arr.canvas.itemconfig(self.arr.rec(self.color_left), tags='green')
    self.arr.canvas.itemconfig(self.arr.rec(self.color_right), tags='green')
    self.arr.chg_color(self.color_mid, 'blue')
    self.arr.chg_color(self.color_left, 'green')
    self.arr.chg_color(self.color_right, 'green')

  def split(self):
    if self.merge_size > self.arr.size - 1:
      self.finished = True
      return
    self.merge_left = self.merge_l_start
    self.merge_mid = min(self.merge_left + self.merge_size - 1, self.arr.size - 1)
    self.merge_right = min(self.merge_left + (2 * self.merge_size) - 1, self.arr.size - 1)
    self.makeBounds(self.merge_left, self.merge_mid, self.merge_right)
    self.merge_i = self.merge_left
    self.merge_j = self.merge_mid + 1
    self.merge_k = self.merge_left

    self.splitting = False
    self.merging = True

    self.merge_l_start += 2 * self.merge_size
    if self.merge_l_start >= self.arr.size - 1:
      self.merge_l_start = 0
      self.merge_size *= 2

  def step(self):
    if self.splitting:
      self.split()
    elif self.merging:
      self.merge()
    elif self.copying:
      self.copy()
    else:
      self.finished = True

    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True


class Quick_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Quick Sort'
    self.arr.updatestats()

    self.partitioning = True
    self.part_swapping = False
    self.call_stack = [(0, self.arr.size -1)]
    self.part_left = -1
    self.pivot = self.arr.size - 1
    self.part_right = 0

  def partition(self):
    if self.part_right < self.pivot:
      self.arr.compared(self.part_right, self.pivot)
      if self.arr.val(self.part_right) <= self.arr.val(self.pivot):
        self.part_left += 1
        self.partitioning = False
        self.part_swapping = True
      else:
        self.part_right += 1
    else:
      self.partitioning = False
      self.swapping = True
  def part_swap(self):
    self.arr.swap(self.part_left, self.part_right)
    self.part_right += 1
    self.part_swapping = False
    self.partitioning = True

  def pivot_swap(self):
    self.arr.swap(self.part_left + 1, self.pivot)
    self.pivot = self.part_left + 1
    last = self.call_stack.pop()
    if self.pivot + 1 < last[1]:
      self.call_stack.append((self.pivot + 1, last[1]))
    if last[0] < self.pivot - 1:
      self.call_stack.append((last[0], self.pivot - 1))
    if len(self.call_stack) == 0:
      self.finished = True
      self.swapping = False
      return
    else:
      self.swapping = False
      self.partitioning = True
      top = self.call_stack[-1]
      self.part_left = top[0] - 1
      self.pivot = top[1]
      self.part_right = top[0]

  def step(self):
    if self.partitioning:
      self.partition()
    elif self.part_swapping:
      self.part_swap()
    elif self.swapping:
      self.pivot_swap()

    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False

class Shell_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Shell Sort'
    self.arr.updatestats()

  def step(self):

    if False:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False


class Radix_Sort(object):
  """docstring for Selection_Sort"""
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Radix Sort'
    self.arr.updatestats()

  def step(self):

    if False:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False

