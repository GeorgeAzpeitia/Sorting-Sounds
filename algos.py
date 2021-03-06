"""
This is the implementation of all the sorting algorithms to be used by the visualizer.
Every algorithm must have a step function which calls itself until it is finished.
The step function serves to perform one step of the algorithm, update the canvas,
and then schedule a callback after a delay. Each step function works as a dispatch
to run the correct portion of the algorithm depending on its state.
"""
import math
import random
class Bubble_Sort(object):
  """
  An implementation of bubble sort with early termination if it detects an
  already sorted array.
  """
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.arr.algo_name = 'Bubble Sort'
    self.finished = False
    self.swapping = False
 
    self.bubbling = True
    self.i = 0
    self.j = 1
    self.n = self.arr.size - 1
    self.swap_cnt = 0
    self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))


  def bubble_up(self):
    if self.n == 0:
      self.bubbling = False
      self.finished = True
      return

    if self.j > self.n:
      if self.swap_cnt == 0:
        self.bubbling = False
        self.finished = True
        return
      else:
        self.swap_cnt = 0
        self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))

      self.j = 1
      self.n -= 1
      self.i += 1
  
    self.arr.compared(self.j, self.j - 1)
    if self.arr.val(self.j - 1) > self.arr.val(self.j):
      self.bubbling = False
      self.swapping = True
    else:
      self.j += 1

  def swap(self):
    self.swap_cnt += 1
    self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))
    self.arr.swap(self.j, self.j-1)
    self.swapping = False
    self.bubbling = True
    self.j += 1

  def step(self):
    if self.bubbling:
      self.bubble_up()
    elif self.swapping:
      self.swap()        
    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()

class Selection_Sort(object):
  """
  Selection sort works by continously finding the smallest element in the array
  and pushing it to the top of the sorted sub-array.
  """
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Selection Sort'

    self.min_idx = 0
    self.sorted_idx = 0
    self.j = 1
    self.n = self.arr.size
    self.arr.updatestats("Current Min: " + str(self.arr.val(self.min_idx)))

  def step(self):
    if not self.swapping:
      self.arr.compared(self.min_idx, self.j)
      if self.arr.val(self.min_idx) > self.arr.val(self.j):
        self.min_idx = self.j
        self.arr.updatestats("Current Min: " + str(self.arr.val(self.min_idx)))
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
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()

class Cocktail_Sort(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Cocktail Sort'

    self.i = 0
    self.j = 1
    self.top = self.arr.size - 1
    self.bottom = 0
    self.up = True
    self.swap_cnt = 0
    self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))

  def step(self):
    if self.up:
      if not self.swapping:
        self.arr.compared(self.i, self.j)
        if self.arr.val(self.i) > self.arr.val(self.j):
          self.swapping = True
      else:
          self.swap_cnt += 1
          self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))
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
            self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))

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
          self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))
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
            self.arr.updatestats("Swaps this pass: " + str(self.swap_cnt))
          self.i = self.bottom
          self.j = self.i + 1
          self.bottom += 1
          self.up = True

    if self.bottom < self.top and not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.finished = True
      self.arr.check_sorted()

class Insertion_Sort(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Insertion Sort'

    self.sorted_idx = 0
    self.i = 0
    self.j = 1
    self.arr.updatestats("Sorted Sub-Array Size: " + str(self.sorted_idx + 1))

  def step(self):
    if not self.swapping:
      self.arr.compared(self.i, self.j)
      if (self.arr.val(self.j)) < self.arr.val(self.i):
        self.swapping = True
      else:
        self.sorted_idx += 1
        self.arr.updatestats("Sorted Sub-Array Size: " + str(self.sorted_idx + 1))
        self.i = self.sorted_idx
        self.j = self.sorted_idx + 1
        
    else:
      self.arr.swap(self.i, self.j)
      self.swapping = False
      self.i -= 1
      self.j -= 1
      if self.i == -1:
        self.sorted_idx += 1
        self.arr.updatestats("Sorted Sub-Array Size: " + str(self.sorted_idx + 1))
        self.i = self.sorted_idx
        self.j = self.sorted_idx + 1

    if self.sorted_idx < self.arr.size - 1:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True

class Shell_Sort(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Shell Sort'

    self.inserting = True
    self.gap = (self.arr.size-1) / 2
    self.sorted_top = self.gap
    self.i = 0
    self.j = self.gap
    self.arr.updatestats("Gap Size: " + str(self.gap))

  def insert(self):
    
    if self.sorted_top > self.arr.size - 1:
      self.gap /= 2
      self.arr.updatestats("Gap Size: " + str(self.gap))
      if self.gap == 0:
        self.inserting = False
        self.finished = True
        return
      else:
        self.sorted_top = self.gap
        self.j = self.sorted_top
        self.i = 0

    self.arr.compared(self.i, self.j)
    if self.arr.val(self.j) < self.arr.val(self.i):
      self.inserting = False
      self.swapping = True
    else:
      self.j += 1
      self.i += 1
    self.sorted_top += 1

  def swap_down(self):
    self.arr.swap(self.i, self.j)
    if self.i - self.gap > -1:
      self.i -= self.gap
      self.j -= self.gap

      self.arr.compared(self.i, self.j)
      if self.arr.val(self.j) >= self.arr.val(self.i):
        self.swapping = False
        self.inserting = True
        self.j = self.sorted_top
        self.i = self.sorted_top - self.gap
    else:
      self.swapping = False
      self.inserting = True
      self.j = self.sorted_top
      self.i = self.sorted_top - self.gap

  def step(self):
    if self.inserting:
      self.insert()
    elif self.swapping:
      self.swap_down()
    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False


class Heap_Sort(object):
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
    self.layer_colors = ['#2c0b41', '#3f1b5b', '#4e1472', '#601c8a', '#752098', '#982f92', '#ba3f8d', '#dd4d87', '#eb688c', '#f18b97', '#f5aca0', '#facdaa', '#fee8c8']
    self.arr.updatestats("Building Heap")

  def parent(self, i):
    return (i - 1) >> 1
  def right(self, i):
    return ((i + 1) << 1)
  def left(self, i):
    return ((i + 1) << 1) - 1
  def get_layer(self, i):
    return int(math.log(i + 1, 2))
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
        self.arr.updatestats("Heap Size: " + str(self.heap_size + 1) + " Layers: " + str(self.get_layer(self.heap_size) + 1))
      elif self.swapping:
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_j), tags=self.layer_colors[self.get_layer(self.swapping_i)])
        self.arr.canvas.itemconfig(self.arr.rec(self.swapping_i), tags=self.layer_colors[self.get_layer(self.swapping_j)])
        self.arr.swap(self.swapping_i, self.swapping_j)
        self.swapping = False
      elif self.heapifying:
        self.heapify(self.heap_var)

    if not self.finished and self.heap_size > 0:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.canvas.itemconfig(self.arr.rec(0), tags=self.arr.get_color(self.arr.val(0)))
      self.arr.updatestats(' ')
      self.arr.revert_color(0)
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True


class Merge_Sort(object):
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
    self.arr.updatestats("Merging [%d - %d] with [%d - %d]".format(self.color_left, self.color_mid, self.color_mid+1, self.color_right))
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
      self.arr.replace_val(self.merge_k, self.backing_arr[self.merge_k])
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
    self.arr.updatestats("Merging [{} - {}] with [{} - {}]".format(self.color_left, self.color_mid, self.color_mid+1, self.color_right))

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
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True

class Merge_Sort_Iter(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Merge Sort (Iterative)'

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
    self.arr.updatestats("Merging sub-arrays of size {} into sub-array of size {}".format(self.merge_size, min(self.merge_size * 2, self.arr.size)))

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
      self.arr.replace_val(self.merge_k, self.backing_arr[self.merge_k])

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
      self.arr.updatestats("Merging sub-arrays of size {} into sub-array of size {}".format(self.merge_size, min(self.merge_size * 2, self.arr.size)))

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
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True


class Quick_Sort(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Quick Sort'

    self.partitioning = True
    self.part_swapping = False
    self.call_stack = [(0, self.arr.size-1)]
    
    self.part_left = -1
    self.pivot = self.arr.size - 1
    self.arr.updatestats("Pivot: "+str(self.arr.val(self.pivot)))
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
      self.arr.updatestats("Pivot: "+str(self.arr.val(self.pivot)))

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
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False



class Quick_Sort_Rand(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Quick Sort'

    self.partitioning = True
    self.part_swapping = False
    self.call_stack = [(0, self.arr.size -1)]
    orig_pivot = self.arr.val(self.arr.size-1)
    rand = random.randrange(0, self.arr.size-1)
    self.arr.swap(rand, self.arr.size-1)
    self.pivot = self.arr.size - 1
    self.arr.updatestats("Pivot before random swap: {} Pivot after swap: {}".format(orig_pivot, self.arr.val(self.pivot)))
    self.part_left = -1
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
      self.part_right = top[0]
      orig_pivot = self.arr.val(top[1])
      rand = random.randrange(top[0], top[1])
      self.arr.swap(rand, top[1])
      self.pivot = top[1]
      self.arr.updatestats("Pivot before random swap: {} Pivot after swap: {}".format(orig_pivot, self.arr.val(self.pivot)))

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
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False






class Radix_Sort(object):
  def __init__(self, master, arr, config):
    self.master = master
    self.arr = arr
    self.config = config
    self.finished = False
    self.swapping = False
    self.arr.algo_name = 'Radix Sort'

    self.digit_count = [0] * 10
    self.backing_arr = [0] * self.arr.size
    self.digit_place = 10
    self.i = 0
    self.counting = True
    self.copying = False
    self.arr.updatestats('Counting...')
  def count(self):
    digit = (self.arr.val(self.i) % self.digit_place) / (self.digit_place / 10)
    self.digit_count[digit] += 1
    self.arr.compared(self.i)
    self.i += 1

    if self.i >= self.arr.size:
      self.i = self.arr.size - 1
      
      self.counting = False
      self.copying = True
      for i in range(self.arr.size):
        self.backing_arr[i] = self.arr.val(i)
      count_str = "Number of vals with x in {}'s digit: ".format(self.digit_place/10)
      for x in range(len(self.digit_count)):
        count_str += "[{}] {} ".format(x, self.digit_count[x])
      self.arr.updatestats(count_str)
      for x in range(1, len(self.digit_count)):
        self.digit_count[x] += self.digit_count[x-1]
      for x in range(len(self.digit_count)):
        if self.digit_count[x] > 0:
          self.digit_count[x] -= 1

  def copy(self):
    if self.i >= 0:
      new_val = self.backing_arr[self.i]
      digit = (new_val % self.digit_place) / (self.digit_place / 10)
      x = self.digit_count[digit]
      self.digit_count[digit] -= 1
      self.arr.replace_val(x, new_val)

      self.i -= 1
      self.arr.swaps += 1
      self.arr.updatestats()
    else:
      self.copying = False

      self.digit_place *= 10
      if ((self.arr.size - 1)%self.digit_place)/(self.digit_place/10) == 0 and self.digit_place > self.arr.size - 1:
        self.finished = True
      else:
        self.i = 0
        for i in range(len(self.digit_count)):
          self.digit_count[i] = 0
        self.counting = True
        self.arr.updatestats("Counting...")

  def step(self):
    if self.counting:
      self.count()
    elif self.copying:
      self.copy()

    if not self.finished:
      if not self.config.paused:
        self.config.last_inst = self.master.after(self.config.delay.get(), self.step)
    else:
      self.arr.updatestats(' ')
      self.arr.clear_compared()
      self.arr.check_sorted()
      self.finished = True
      self.config.running = False

