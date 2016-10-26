from pyevolve import G1DList
from pyevolve import GSimpleGA
import logging

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