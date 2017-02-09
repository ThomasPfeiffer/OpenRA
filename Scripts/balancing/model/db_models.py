from peewee import *
import settings
import datetime

db = SqliteDatabase(settings.database)
fitness_function = None
ra_map = None
run = None

def initialize_database():
    db.connect()
    FitnessFunction.create_table(True)
    Run.create_table(True)
    TemplateFile.create_table(True)
    RunHasTemplateFile.create_table(True)
    RAMap.create_table(True)
    RAGame.create_table(True)
    RAPlayer.create_table(True)
    RAParameter.create_table(True)
    Individual.create_table(True)
    IndividualParameter.create_table(True)


class DBModel(Model):
    class Meta:
        database = db


class FitnessFunction(DBModel):
    function = CharField(null=True)
    description = CharField(null=True)


class Run(DBModel):
    start_timestamp = DateTimeField(default=datetime.datetime.now)
    end_timestamp = DateTimeField(null=True)
    description = CharField(null=True)
    fitness_function = ForeignKeyField(FitnessFunction)

    def end(self):
        self.end_timestamp = datetime.datetime.now()
        self.save()


class TemplateFile(DBModel):
    read_file = CharField()
    write_file = CharField()
    file_content = CharField()


class RunHasTemplateFile(DBModel):
    run = ForeignKeyField(Run)
    template_file = ForeignKeyField(TemplateFile)


class RAMap(DBModel):
    name = CharField()


class RAGame(DBModel):
    game_id = CharField()
    run = ForeignKeyField(Run, null=True)
    start_timestamp = DateTimeField()
    end_timestamp = DateTimeField()
    max_ticks_reached = BooleanField()
    ticks = IntegerField()
    fitness = IntegerField()
    map = ForeignKeyField(RAMap, null=True)


class RAPlayer(DBModel):
    game = ForeignKeyField(RAGame)
    player_name = CharField()
    faction = CharField()
    winner = BooleanField()
    buildings_dead = IntegerField()
    buildings_killed = IntegerField()
    deaths_cost = IntegerField()
    kills_cost = IntegerField()
    order_count = IntegerField()
    units_dead = IntegerField()
    units_killed = IntegerField()


class RAParameter(DBModel):
    name = CharField()
    game = ForeignKeyField(RAGame)
    file_string = CharField()
    min_value = IntegerField()
    max_value = IntegerField()
    value = IntegerField()


class Individual(DBModel):
    id_in_run = IntegerField()
    run = ForeignKeyField(Run)
    fitness = IntegerField(null=True)
    age = IntegerField(null=True)
    date_of_birth = IntegerField(null=True)


class IndividualParameter(DBModel):
    name = CharField()
    individual = ForeignKeyField(Individual)
    file_string = CharField()
    min_value = IntegerField()
    max_value = IntegerField()
    value = IntegerField()


def save_as_ra_param(game, param):
    return RAParameter.create(
        name=param.name,
        game=game,
        file_string=param.file_string,
        min_value=param.min_value,
        max_value=param.max_value,
        value=param.value
    )


def save_as_individual_param(individual, param):
    return IndividualParameter.create(
        name=param.name,
        individual=individual,
        file_string=param.file_string,
        min_value=param.min_value,
        max_value=param.max_value,
        value=param.value
    )


def init():
    initialize_database()
    global fitness_function
    fitness_function, _ = FitnessFunction.get_or_create(id=settings.fitness_function_id)
    global ra_map
    ra_map, _ = RAMap.get_or_create(name=settings.map_name)
    run = Run.create(fitness_function=fitness_function, description=settings.run_description)


def get_fitness_function():
    global fitness_function
    return fitness_function


def get_map():
    return ra_map


def get_run():
    global run
    if not run:
        run = Run.select().order_by(Run.id.desc()).get()
    return run


def new_game_id():
    curr_max_id = RAGame.select(fn.MAX(RAGame.id).alias('max')).get().max
    if curr_max_id is None:
        return 1
    else:
        return curr_max_id+1


def main():
    initialize_database()

if __name__ == "__main__":
    main()


