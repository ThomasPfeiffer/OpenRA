-- average buildings destroyed
select avg(buildings_killed) from raplayer;

-- Game Duration
select ragame.run_id, ticks, ((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id==14 or ragame.run_id == 11;

-- Number of games per run
select ragame.run_id, count(*) from ragame group by ragame.run_id;

select name, value, run_id,max_ticks_reached, fitness, raparameter.game_id  from raparameter join ragame, run where ragame.id == raparameter.game_id and run.id == ragame.run_id and run.id == 1;

-- fitness list for a run
select ragame.id, fitness from ragame where ragame.run_id =49;

-- best game of a run
select ragame.id, min(fitness) from ragame join run where ragame.run_id == run.id and run.id =47;

-- Game count for a run
select count(*) from ragame where ragame.run_id == 16;


-- Select run parameter list for excel analysis
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where run_id = 40;