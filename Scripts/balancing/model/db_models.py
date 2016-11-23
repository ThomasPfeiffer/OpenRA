from peewee import *
from balancing import settings
import datetime

db = SqliteDatabase(settings.database)


def initialize_database():
    db.connect()
    FitnessFunction.create_table(True)
    Run.create_table(True)
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


class RAGame(DBModel):
    game_id = CharField()
    run = ForeignKeyField(Run, null=True)
    start_timestamp = DateTimeField()
    end_timestamp = DateTimeField()
    max_ticks_reached = BooleanField()
    ticks = IntegerField()
    fitness = IntegerField()


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
    min_value = DoubleField()
    max_value = DoubleField()
    value = DoubleField()


def get_fitness_function():
    return FitnessFunction.select().where(FitnessFunction.id == settings.fitness_function).get()


def save_as_ra_param(game, param):
    return RAParameter.create(
        name=param.name,
        game=game,
        file_string=param.file_string,
        min_value=param.min_value,
        max_value=param.max_value,
        value=param.value
    )


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

