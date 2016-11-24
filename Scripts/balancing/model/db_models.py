from peewee import *
from balancing import settings
import datetime

db = SqliteDatabase(settings.database)
fitness_function = None
run = None
ra_map = None


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


class DBModel(Model):
    class Meta:
        database = db


class FitnessFunction(DBModel):
    function = CharField()
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


def save_as_ra_param(game, param):
    return RAParameter.create(
        name=param.name,
        game=game,
        file_string=param.file_string,
        min_value=param.min_value,
        max_value=param.max_value,
        value=param.value
    )


def get_fitness_function():
    global fitness_function
    if not fitness_function:
        fitness_function = FitnessFunction.get(FitnessFunction.id == settings.fitness_function_id)
    return fitness_function


def get_run():
    global run
    if not run:
        run = Run.create(fitness_function=get_fitness_function(), description=settings.run_description)
    return run


def get_map():
    global ra_map
    if not ra_map:
        ra_map = RAMap.create(name=settings.map_name)
    return ra_map


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


