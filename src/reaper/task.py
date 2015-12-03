import time
from threading import Timer

def print_time():
  print "From print_time", time.time()

class ReaperTask:
  def __init__(self, dao):
    self_dao = dao
    self._timer = Timer(5, print_time, ())
    self._timer.start()