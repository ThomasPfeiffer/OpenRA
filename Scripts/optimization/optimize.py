from pyevolve import G1DList
from pyevolve import GSimpleGA
import subprocess
import errno
import threading
import time

def timeout( p ):
    if p.poll() is None:
        try:
            p.kill()
            print 'Error: process taking too long to complete--terminating'
        except OSError as e:
            if e.errno != errno.ESRCH:
                raise

class Counter:
    def __init__(self):
        self.count = 0

    def inc(self):
        self.count +=1

    def get(self):
        return self.count

counter = Counter()
# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0
   counter.inc()
   # iterate over the chromosome elements (items)
   for value in chromosome:
      if value==0:
         score += 1.0

   return score

def do_optimization():
    # Genome instance
    genome = G1DList.G1DList(20)

    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)
    ga = GSimpleGA.GSimpleGA(genome)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.setPopulationSize(5)
    ga.setGenerations(10)
    ga.evolve(freq_stats=0)
    print '----'
    print genome
    print '----'

    # Best individual
    #print ga.bestIndividual()
    print "Count: " + str(counter.get())

#do_optimization()

class TimerClass(threading.Thread):
    def __init__(self, proc):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 300 # Seconds for forced kill
        self.proc = proc

    def run(self):
        while self.count > 0 and not self.event.is_set():
            self.event.wait( 1 )
            self.count -= 1
        if not self.event.is_set():
            print "Killing due to timeout"
        self.proc.kill()

    def stop(self):
        self.event.set()


def exec_ra(game_id):
    proc = subprocess.Popen(["C:\\dev\\OpenRA\\Game\\OpenRA.exe", "--fitness-log=C:\\temp\\games.yaml", "--game-id="+str(game_id)])
    tmr = TimerClass(proc)
    tmr.start()
    proc.wait()
    tmr.stop()


for i in range(50):
    exec_ra(i)



print "finished"
