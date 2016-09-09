"""
The sound module for the animation. This is almost directly ported over from
original Sound of Sorting at http://panthema.net/2013/sound-of-sorting/
that this project was based on.
The original source code for this sound module can be found at 
http://panthema.net/2013/sound-of-sorting/sound-of-sorting-0.6.5/src/SortSound.cpp.html
Credit goes to the original author, Tino Bingmann.
 * Copyright (C) 2013-2014 Timo Bingmann <tb@panthema.net>
 *
 * This program is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import math
import sys
import threading
import pyaudio
import numpy

samplerate = 44100
sound_on = False
sound_sustain = 2.0
max_oscillators = 512

class Oscillator(object):
  def __init__(self, freq, tstart, duration=44100/8):
    self.freq = freq
    self.time_start = tstart
    self.time_end = tstart + duration
    self.duration = duration
    

  def wave_triangle(self, x):
    x = math.fmod(x, 1.0)

    if x <= 0.25: return 4.0 * x
    if x <= 0.75: return 2.0 - 4.0 * x
    return 4.0 * x - 4.0

  def envelope(self, i):
    x = float(i) / self.duration
    if x > 1.0 : x = 1.0

    attack = 0.025
    decay = 0.1
    sustain = 0.9
    release = 0.3

    if x < attack:
      return 1.0 / attack * x
    if x < attack + decay:
      return 1.0 - (x - attack) / decay * (1.0 - sustain)
    if x < 1.0 - release:
      return sustain

    return sustain /release * (1.0 - x)

  def mix(self, data, size, p):

    for i in xrange(size):
      if (p+i < self.time_start):
       continue
      if (p+i >= self.time_end):
        break
      trel = (p + i - self.time_start)

      data[i] += self.envelope(trel) * self.wave_triangle(float(trel) / samplerate * self.freq)

  def is_done(self, p):
    return p >= self.time_end


class s(object):
  def __init__(self, arr, config):
    self.s_pos = 0
    self.access_list = []
    self.oscillator_list = []
    self.lock = threading.RLock()
    self.arr = arr
    self.config = config
    self.done = False

  def add_oscillator(self, freq, p, pstart, duration):
    oldest = 0
    toldest = sys.maxsize
    for i in xrange(len(self.oscillator_list)):
      if (self.oscillator_list[i].is_done(p)):
        self.oscillator_list[i] = Oscillator(freq, pstart, duration)
        return
      if (self.oscillator_list[i].time_start < toldest):
        oldest = i
        toldest = self.oscillator_list[i].time_start

    if len(self.oscillator_list) < max_oscillators:
      self.oscillator_list.append(Oscillator(freq, pstart, duration))
    else:
      self.oscillator_list[oldest] = Oscillator(freq, pstart, duration)


  def sound_access(self, *args):
    if not sound_on:
      return
    else:
      # with self.lock:
      for arg in args:
        self.access_list.append(arg)

  def sound_reset(self):
    self.s_pos = 0
    self.oscillator_list = []

  def sound_callback(self, stream_in, frame_count, time_info, status_flag):
    stream = [0] * frame_count
    if self.done:
      a = numpy.array(stream)
      return (a.astype(numpy.int16), pyaudio.paComplete)
    if not sound_on:
      a = numpy.array(stream)
      return (a.astype(numpy.int16), pyaudio.paContinue)
    with self.lock:
      if len(self.access_list) >= 1:
        pscale = float(len(stream)) / len(self.access_list)
        for i in xrange(len(self.access_list)):
          freq = 120 + 1200 * (float(self.access_list[i]) / self.arr.size) * (float(self.access_list[i]) / self.arr.size)
          duration = min(30 / 1000.0 , self.config.delay.get() / 1000.0) * sound_sustain * samplerate
          self.add_oscillator(freq, self.s_pos, self.s_pos + i * pscale, 10 / 1000.0 * sound_sustain * samplerate)
        self.access_list = []

    wave = [0.0] * len(stream)
    wavecount = 0
    for osc in self.oscillator_list:
      if not osc.is_done(self.s_pos):
        osc.mix(wave, len(wave), self.s_pos)
        wavecount += 1
    if wavecount == 0:
      for i in xrange(len(stream)):
          stream[i] = 0
    else:
      vol = max(wave)
      oldvol = 1.0
      if vol <= oldvol:
        vol = 0.9 * oldvol

      for i in xrange(len(stream)):
        v = int(24000 * wave[i] /(oldvol + (vol - oldvol) * (i/float(len(stream)))))
        if v > 32200: v = 32200
        if v < -32200: v = -32200
        stream[i] = v
      oldvol = vol

    self.s_pos += len(stream)
    a = numpy.array(stream)
    return (a.astype(numpy.int16).tostring(), pyaudio.paContinue)

