from model.db_models import Individual
import settings


def pick_best(indis, nr):
    sorted_indis = sorted(indis, key=lambda individual: individual.fitness, reverse=False)
    return sorted_indis[0:nr]


def wtf():
    indilist = Individual.select().where(Individual.run == 98)
    with open(settings.workspace_path + '/output.csv','w') as outf:
        population = []
        index = -4
        j = 0
        for individual in indilist:
            population.append(individual)
            index+=1
            if index != 0 and index % 6 == 0:
                index = 1
                population = pick_best(population,6)
                outf.write(str(j))
                j += 1
                for p in population:
                    outf.write(';'+str(p.fitness))
                outf.write('\n')

wtf()