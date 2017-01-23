-- average buildings destroyed
select avg(buildings_killed) from raplayer;

-- Game Duration
select ((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id == 86;

-- Avg Game Duration
select ragame.run_id, ticks, avg((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id == 98;

-- Number of games per run
select ragame.run_id, count(*) from ragame group by ragame.run_id;

-- fitness list for a run
select ragame.id,ragame.game_id, fitness from ragame where ragame.run_id =155;

-- Wins per faction
select raplayer.faction, count(*) from raplayer join ragame on raplayer.game_id = ragame.id where ragame.run_id  = 195 and raplayer.winner = 1 group by raplayer.faction;


-- Select run parameter list for excel analysis
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where run_id = 95;
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where ragame.id = 16316;
select ragame.id, fitness, rules_arty_cost, rules_arty_health, rules_pbox_cost, rules_pbox_health, rules_ftur_cost, rules_ftur_health, weapons_scud_damage,weapons_155mm_damage , weapons_fireball_damage, weapons_vulcan_damage 
from ragame
left join (select raparameter.game_id, value as 'rules_arty_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_arty_cost') as s1
on ragame.id == s1.game_id
left join (select raparameter.game_id, value as 'rules_arty_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_arty_health') as s2
on ragame.id == s2.game_id
left join (select raparameter.game_id, value as 'rules_pbox_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_pbox_cost') as s3
on ragame.id == s3.game_id
left join (select raparameter.game_id, value as 'rules_pbox_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_pbox_health') as s4
on ragame.id == s4.game_id
left join (select raparameter.game_id, value as 'rules_ftur_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_ftur_cost') as s5
on ragame.id == s5.game_id
left join (select raparameter.game_id, value as 'rules_ftur_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_ftur_health') as s6
on ragame.id == s6.game_id
left join (select raparameter.game_id, value as 'weapons_scud_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapons_scud_damage') as s7
on ragame.id == s7.game_id
left join (select raparameter.game_id, value as 'weapons_155mm_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapons_155mm_damage') as s8
on ragame.id == s8.game_id
left join (select raparameter.game_id, value as 'weapons_fireball_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapons_fireball_damage') as s9
on ragame.id == s9.game_id
left join (select raparameter.game_id, value as 'weapons_vulcan_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapons_vulcan_damage') as s10
on ragame.id == s10.game_id
where ragame.run_id = 185;

-- Avg param value
select value, avg(fitness), count(ragame.id) from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_damage' group by value;

-- Selected individuals of a run
select fitness, age from individual where individual.age > 0 and individual.run_id = 98;

-- best individuals of a run
select id, fitness from individual where individual.run_id = 186 order by fitness limit 10;

select player_name, raplayer.faction, count(raplayer.id) from raplayer join ragame on ragame.id = raplayer.game_id where ragame.run_id = 112 and winner = 1 group by raplayer.player_name;


-- Individual parameters for excel 
select individual.individual_id, fitness, name, value from individualparameter join individual on individual.id = individualparameter.individual_id where run_id = 95;
select individual.individual_id, fitness, name, value from individualparameter join individual on individual.id = individualparameter.individual_id where individual.id = 16316;
select individual.id, fitness, rules_v2rl_cost, rules_v2rl_health, rules_arty_cost, rules_arty_health, rules_pbox_cost, rules_pbox_health, rules_ftur_cost, rules_ftur_health, weapons_scud_damage,weapons_155mm_damage , weapons_fireball_damage, weapons_vulcan_damage 
from individual
left join (select individualparameter.individual_id, value as 'rules_v2rl_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_v2rl_cost') as s1
on individual.id == s1.individual_id
left join (select individualparameter.individual_id, value as 'rules_v2rl_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_v2rl_health') as s2
on individual.id == s2.individual_id
left join (select individualparameter.individual_id, value as 'rules_arty_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_arty_cost') as s11
on individual.id == s11.individual_id
left join (select individualparameter.individual_id, value as 'rules_arty_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_arty_health') as s12
on individual.id == s12.individual_id
left join (select individualparameter.individual_id, value as 'rules_pbox_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_pbox_cost') as s3
on individual.id == s3.individual_id
left join (select individualparameter.individual_id, value as 'rules_pbox_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_pbox_health') as s4
on individual.id == s4.individual_id
left join (select individualparameter.individual_id, value as 'rules_ftur_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_ftur_cost') as s5
on individual.id == s5.individual_id
left join (select individualparameter.individual_id, value as 'rules_ftur_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_ftur_health') as s6
on individual.id == s6.individual_id
left join (select individualparameter.individual_id, value as 'weapons_scud_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapons_scud_damage') as s7
on individual.id == s7.individual_id
left join (select individualparameter.individual_id, value as 'weapons_155mm_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapons_155mm_damage') as s8
on individual.id == s8.individual_id
left join (select individualparameter.individual_id, value as 'weapons_fireball_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapons_fireball_damage') as s9
on individual.id == s9.individual_id
left join (select individualparameter.individual_id, value as 'weapons_vulcan_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapons_vulcan_damage') as s10
on individual.id == s10.individual_id
where individual.id in (select id from individual where individual.run_id = 186 order by fitness limit 10);