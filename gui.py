
import sort_array
import algos
import sound
import Tkinter as tk
import ttk
import sys
import time
import colors
import pyaudio
import time

class Config(object):
  """docstring for Config"""
  def __init__(self):
    self.width = 1200
    self.height = 940
    self.arr_size = tk.IntVar()
    self.arr_size.set(10)
    self.arr_sorting = tk.IntVar()
    self.arr_few_unique = tk.IntVar()
    self.colors = colors._keys
    self.colors_dict = colors._dict
    self.color_scheme = tk.StringVar()
    self.color_scheme.set(self.colors[0])
    self.graph_mode = tk.IntVar()
    self.algorithms = {
                      'Bubble Sort'             : algos.Bubble_Sort, 
                      'Selection Sort'          : algos.Selection_Sort,
                      'Cocktail Sort'           : algos.Cocktail_Sort,
                      'Insertion Sort'          : algos.Insertion_Sort,
                      'Shell Sort'              : algos.Shell_Sort,
                      'Heap Sort'               : algos.Heap_Sort,
                      'Merge Sort'              : algos.Merge_Sort,
                      'Merge Sort (Iterative)'  : algos.Merge_Sort_Iter,
                      'Quick Sort'              : algos.Quick_Sort,
                      'Quick Sort (Randomized)' : algos.Quick_Sort_Rand,
                      'Radix Sort'              : algos.Radix_Sort
                      }
    #alg_keys is used purely because I wanted to preserve this particular or of algos in the option menu
    self.alg_keys = [
                    'Bubble Sort', 'Selection Sort', 'Cocktail Sort', 'Insertion Sort', 
                    'Shell Sort','Heap Sort', 'Merge Sort', 'Merge Sort (Iterative)', 
                    'Quick Sort', 'Quick Sort (Randomized)' , 'Radix Sort'
                    ]
    self.algorithm = tk.StringVar()

    self.algorithm.set('Bubble Sort')
    self.delay = tk.IntVar()
    self.delay.set(10)
    self.first_run = True
    self.paused = False
    self.running = False
    self.done_checking_sort = False
    self.last_inst = None
    self.sound = None
    self.sound_on = tk.IntVar()
    #0 = Bars, 1 = Points, 2 = Spiral
    self.appearance = tk.IntVar()

class App(object):
  def __init__(self, master):
    self.master = master
    self.canvas = tk.Canvas(self.master, width=config.width, height=config.height, bg=config.colors_dict[config.color_scheme.get()][-1])
    self.canvas.pack(side='left', fill='both', expand='YES')
    self.arr = sort_array.Canvas_Array(self.master, self.canvas, config)
    self.algo = algos.Bubble_Sort(self.master, self.arr, config)
    config.sound = sound.s(self.arr, config)
    sound.sound_on = False
    #Sound
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=1, rate=44100,
                    output=True, stream_callback=config.sound.sound_callback)
    self.stream.start_stream()

    tk.Label(self.master, text="Sorting Sounds").pack(pady=10)
    self.arr_ctl = tk.LabelFrame(self.master, text='Array Controls', padx=5, pady=5)
    self.arr_ctl.pack(padx=10, pady=5)

    self.arr_size_frame = tk.Frame(self.arr_ctl)
    self.arr_size_frame.pack(anchor='w')
    tk.Label(self.arr_size_frame, text='Array Size ').pack(side='left')
    self.arr_size_entry = tk.Entry(self.arr_size_frame, textvariable=config.arr_size, width=6)
    self.arr_size_entry.pack(side='left')

    self.arr_size_scale = tk.Scale(self.arr_ctl, 
      from_=1, to=5000, orient=tk.HORIZONTAL, variable=config.arr_size, showvalue=0)
    self.arr_size_scale.pack(anchor='w', fill='x')

    self.arr_size_scale_frame = tk.Frame(self.arr_ctl)
    self.arr_size_scale_frame.pack(anchor='w', fill='x')
    tk.Label(self.arr_size_scale_frame, text='3').pack(pady=3, side='left')
    tk.Label(self.arr_size_scale_frame, text=5000).pack(pady=3, side='right')

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

    self.arr_appearance_ctl = tk.LabelFrame(self.arr_ctl, text='Appearance', padx=5)
    self.arr_appearance_ctl.pack(pady=5, fill='x')
    
    self.arr_colors_frame = tk.Frame(self.arr_appearance_ctl)
    self.arr_colors_frame.pack(fill='x', pady=5)
    tk.Label(self.arr_colors_frame, text='Color Scheme ').pack(side='left')
    self.arr_opt_colors = tk.OptionMenu(self.arr_colors_frame, config.color_scheme, *config.colors)
    self.arr_opt_colors.pack(side='left')
    self.arr_bar = tk.Radiobutton(self.arr_appearance_ctl, text='Bars', variable=config.appearance, value = 0)
    self.arr_bar.pack(side='left')
    self.arr_graph = tk.Radiobutton(self.arr_appearance_ctl, text='Points', variable=config.appearance, value = 1)
    self.arr_graph.pack(side='left')
    self.arr_spiral = tk.Radiobutton(self.arr_appearance_ctl, text='Spiral', variable=config.appearance, value = 2)
    self.arr_spiral.pack(side='left')

    self.arr_sound = tk.Checkbutton(self.arr_ctl, text='Sound (Experimental)', variable=config.sound_on)
    self.arr_sound.pack(side='left')

    def change_sound(*args):
      sound.sound_on = config.sound_on.get()

    config.sound_on.trace('w', change_sound)
    self.algo_ctl = tk.LabelFrame(self.master, text='Algorithm Controls', pady=5, padx=5)
    self.algo_ctl.pack(padx=10, fill='x')

    tk.Label(self.algo_ctl, text='Sorting Algorithm').pack(pady=3, anchor='w')
    self.alg_opt = tk.OptionMenu(self.algo_ctl, config.algorithm, *config.alg_keys)
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
    if config.running:
     
      self.master.after_cancel(config.last_inst)
      
      config.running = False
      config.paused = True

  def step(self):
    if config.running:
      self.pause()
    if config.first_run:
      config.paused = True
      config.first_run = False
      self.algo = config.algorithms[config.algorithm.get()](self.master, self.arr, config)
      self.algo.step()
    elif not self.algo.finished:
      self.algo.step()


  def generate(self):
    if not config.running:
      self.canvas.delete('all')
      config.first_run = True
      self.canvas.config(bg=config.colors_dict[config.color_scheme.get()][-1])
      if config.arr_size.get() < 3:
        config.arr_size.set(3)
      self.arr = sort_array.Canvas_Array(self.master, self.canvas, config)
      config.sound.arr = self.arr
      self.algo = config.algorithms[config.algorithm.get()](self.master, self.arr, config)
    else:
      self.pause()
      self.generate()

  def run(self):
    if not config.running:
      if config.first_run:
        config.first_run = False
        config.done_checking_sort = False
        self.algo = config.algorithms[config.algorithm.get()](self.master, self.arr, config)
        config.running = True
        config.paused = False
        self.algo.step()
      else:
        if self.algo.finished:
          self.generate()
          self.run()
        else:
          config.running = True
          config.paused = False
          self.algo.step()


root = tk.Tk()
root.wm_title("Sorting Sounds")
root.style = ttk.Style()
root.style.theme_use("clam")

config = Config()
root.minsize(config.width, config.height)
app = App(root)
root.mainloop()

config.sound.done = True
while app.stream.is_active():
    time.sleep(0.1)
app.stream.stop_stream()
app.stream.close()
app.p.terminate()



















