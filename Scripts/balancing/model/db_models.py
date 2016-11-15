from peewee import *
from balancing import settings

db = SqliteDatabase(settings.database)


def initialize_database():
    db.connect()
    RAGame.create_table(True)
    RAPlayer.create_table(True)
    RAParameter.create_table(True)


class DBModel(Model):
    class Meta:
        database = db


class RAGame(DBModel):
    game_id = CharField()
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


