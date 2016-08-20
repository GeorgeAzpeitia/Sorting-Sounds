import math

class Canvas_Array(object):
  """docstring for Array"""
  #determines the size of the gap between bars, should be kept between 0 and 0.25
  spacer_ratio = 0.05

  def __init__(self, canvas, size):
    self.canvas = canvas;
    self.size = size
    self.width = int(self.canvas['width'])
    self.height = int(self.canvas['height'])

    #Temporary solution until I figure out how to display an array with more elements
    #than the width of the window
    if self.size > self.width: 
      self.size = self.width
    
    self.bar_width = self.width / self.size
    print self.bar_width
    if (self.bar_width * Canvas_Array.spacer_ratio) < 0.25:
      self.bar_spacer_width = 0
    else:
      self.bar_spacer_width = math.ceil(self.bar_width * Canvas_Array.spacer_ratio)
    
    self.bar_width -= self.bar_spacer_width
    print self.bar_width
    self.left_padding = (self.width % self.size) + self.bar_spacer_width
    if self.left_padding / self.size >= 1:
      self.bar_width += self.left_padding // self.size
      self.left_padding = self.left_padding % self.size

    self.bar_slope = float(self.height) / float(self.width)
    #bar_width should never be < 1
    if self.bar_width <= 1:
      x0 = 0
      y0 = self.height - 1
      x1 = 0
      y1 = self.height + 1
      self.bar_array = [ (0, self.canvas.create_line(x0, y0, x1, y1, fill="white")) ]
      for i in xrange(1, self.size):
        x0 += 1
        y0 = self.height - math.ceil(x0 * self.bar_slope)
        x1 = x0
        self.bar_array.append((i, self.canvas.create_line(x0, y0, x1, y1, fill="white")))
    else:
      x0 = self.left_padding
      y0 = self.height - math.ceil(self.bar_slope * (self.left_padding + self.bar_width))
      x1 = self.left_padding + self.bar_width
      y1 = self.height + 1
      self.bar_array = [ (0, self.canvas.create_rectangle(x0, y0, x1, y1, fill='white')) ]
      for i in xrange(1, self.size):
        
        fill = 'white'
        if (i + 1) % 5 == 0:
          fill = 'blue'
          print "i % 5 = " + str(i)
        if (i + 1) % 10 == 0: 
          fill = 'red'
          print "i % 9 = " + str(i)

        x0 = x1 + self.bar_spacer_width
        x1 = x0 + self.bar_width
        y0 = self.height - math.ceil(self.bar_slope * x1)
        self.bar_array.append((i, self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=0)))

