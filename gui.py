
import sort_array
import algos
import sound
import Tkinter as tk
import sys
import time

class Config(object):
  """docstring for Config"""
  def __init__(self):
    self.width = 1200
    self.height = 900
    self.arr_size = tk.IntVar()
    self.arr_size.set(10)
    self.arr_sorting = tk.IntVar()
    self.arr_few_unique = tk.IntVar()
    self.colors = ['white', 'rainbow']
    self.color_scheme = tk.StringVar()
    self.color_scheme.set(self.colors[0])
    self.algorithms = ['Bubble Sort', 'Selection Sort']
    self.algorithm = tk.StringVar()
    self.algorithm.set(self.algorithms[0])
    self.delay = tk.IntVar()
    self.delay.set(10)
    self.paused = True
    self.step = False
    self.running = False

class App(object):
  def __init__(self, master):
    self.master = master
    self.canvas = tk.Canvas(self.master, width=config.width, height=config.height, bg='black')
    self.canvas.pack(side='left', fill='both', expand='YES')
    self.arr = sort_array.Canvas_Array(self.master, self.canvas, config)

    tk.Label(self.master, text="Sorting Sounds").pack(pady=10)
    self.arr_ctl = tk.LabelFrame(self.master, text='Array Controls', padx=5, pady=5)
    self.arr_ctl.pack(padx=10, pady=5)

    self.arr_size_frame = tk.Frame(self.arr_ctl)
    self.arr_size_frame.pack(anchor='w')
    tk.Label(self.arr_size_frame, text='Array Size ').pack(side='left')
    self.arr_size_entry = tk.Entry(self.arr_size_frame, textvariable=config.arr_size, width=6)
    self.arr_size_entry.pack(side='left')

    self.arr_size_scale = tk.Scale(self.arr_ctl, 
      from_=1, to=config.width, orient=tk.HORIZONTAL, variable=config.arr_size, showvalue=0)
    self.arr_size_scale.pack(anchor='w', fill='x')

    self.arr_size_scale_frame = tk.Frame(self.arr_ctl)
    self.arr_size_scale_frame.pack(anchor='w', fill='x')
    tk.Label(self.arr_size_scale_frame, text='5').pack(pady=3, side='left')
    tk.Label(self.arr_size_scale_frame, text=config.width).pack(pady=3, side='right')

    def manual_size(event):
      self.arr_size_scale.set(int(config.arr_size.get()))
      self.generate()
    self.arr_size_entry.bind('<Return>', manual_size)


    # self.arr_size_scale = tk.Scale(self.arr_ctl, 
    #   from_=5, to=config.width, orient=tk.HORIZONTAL, label='Array Size', variable=config.arr_size)
    # self.arr_size_scale.pack(fill='x', padx=5)

    self.arr_sorting_ctl = tk.LabelFrame(self.arr_ctl, text='Sorting', padx=5)
    self.arr_sorting_ctl.pack(pady=5)
    
    self.arr_radio_random = tk.Radiobutton(self.arr_sorting_ctl, text='Random', variable=config.arr_sorting, value = 0)
    self.arr_radio_random.grid(row=0, column=0, sticky='w')
    self.arr_radio_reverse = tk.Radiobutton(self.arr_sorting_ctl, text='Reverse Sorted', variable=config.arr_sorting, value = 1)
    self.arr_radio_reverse.grid(row=0, column=1, sticky='w')
    self.arr_radio_sorted = tk.Radiobutton(self.arr_sorting_ctl, text='Sorted', variable=config.arr_sorting, value = 2)
    self.arr_radio_sorted.grid(row=1, column=0, sticky='w')
    self.arr_radio_almost = tk.Radiobutton(self.arr_sorting_ctl, text='Almost Sorted',variable=config.arr_sorting, value = 3)
    self.arr_radio_almost.grid(row=1, column=1, sticky='w')
    self.arr_check_few_uniq = tk.Checkbutton(self.arr_sorting_ctl, text='Few Unique', variable=config.arr_few_unique)
    self.arr_check_few_uniq.grid(row=2, column=0, sticky='w')

    self.arr_colors_frame = tk.Frame(self.arr_ctl)
    self.arr_colors_frame.pack(side='left', pady=5)
    tk.Label(self.arr_colors_frame, text='Color Scheme ').pack(side='left')
    self.arr_opt_colors = tk.OptionMenu(self.arr_colors_frame, config.color_scheme, *config.colors)
    self.arr_opt_colors.pack(side='left')

    self.algo_ctl = tk.LabelFrame(self.master, text='Algorithm Controls', pady=5, padx=5)
    self.algo_ctl.pack(padx=10, fill='x')

    tk.Label(self.algo_ctl, text='Sorting Algorithm').pack(pady=3, anchor='w')
    self.alg_opt = tk.OptionMenu(self.algo_ctl, config.algorithm, *config.algorithms)
    self.alg_opt.pack(anchor='w', fill='x')

    self.alg_delay_frame = tk.Frame(self.algo_ctl)
    self.alg_delay_frame.pack(anchor='w')
    tk.Label(self.alg_delay_frame, text='Delay (ms)').pack(side='left')
    self.alg_delay_entry = tk.Entry(self.alg_delay_frame, textvariable=config.delay, width=4)
    self.alg_delay_entry.pack(side='left')

    self.alg_delay_scale = tk.Scale(self.algo_ctl, 
      from_=1, to=1000, orient=tk.HORIZONTAL, variable=config.delay, showvalue=0)
    self.alg_delay_scale.pack(anchor='w', fill='x')
    tk.Label(self.algo_ctl, text='0 (ms)').pack(side='left')
    tk.Label(self.algo_ctl, text='1000 (ms)').pack(side='right')

    def manual_delay(event):
      self.alg_delay_scale.set(int(config.delay.get()))
    self.alg_delay_entry.bind('<Return>', manual_delay)
   
    self.btn_frame = tk.Frame(self.master)
    self.btn_frame.columnconfigure(0, weight=1)
    self.btn_frame.columnconfigure(1, weight=1)
    self.btn_frame.pack(fill='x')
    
    self.btn_pause = tk.Button(self.btn_frame, text='Pause', command=self.pause)
    self.btn_pause.grid(row=0, column=0, pady=5)
    self.btn_step = tk.Button(self.btn_frame, text='Step', command=self.step)
    self.btn_step.grid(row=0, column=1, pady=5)
    self.btn_generate = tk.Button(self.btn_frame, text='Generate', command=self.generate)
    self.btn_generate.grid(row=1, column=0)
    self.btn_run = tk.Button(self.btn_frame, text='Run', command=self.run)
    self.btn_run.grid(row=1, column=1)
    # self.master.after(500, self.test)

  def pause(self):
    config.pause = True
    config.running = False

  def step(self):
    self.pause()
    config.step = True
    self.run()

  def generate(self):

    self.canvas.delete('all')
    x = config.arr_size.get()
    self.arr = sort_array.Canvas_Array(self.master, self.canvas, config)

  def run(self):
    print config.running
    if(not config.running):
      self.algo = algos.Bubble_Sort(self.master, self.arr, config)
      config.running = True
      self.algo.begin()
    
  def test(self):
    self.bubs = algos.Selection_Sort(self.master, self.arr)
    self.bubs.begin()
    for k, v in self.arr.__dict__.items():
      print (k, v)
root = tk.Tk()
config = Config()
root.minsize(config.width, config.height)
app = App(root)
root.mainloop()



















