-- average buildings destroyed
select avg(buildings_killed) from raplayer;

-- Game Duration
select ragame.run_id, ticks, avg((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id == 98;

-- Number of games per run
select ragame.run_id, count(*) from ragame group by ragame.run_id;

select name, value, run_id,max_ticks_reached, fitness, raparameter.game_id  from raparameter join ragame, run where ragame.id == raparameter.game_id and run.id == ragame.run_id and run.id == 1;

-- fitness list for a run
select ragame.id, fitness from ragame where ragame.run_id =108;

-- best game of a run
select ragame.id, min(fitness) from ragame where ragame.run_id  =95;

-- best games of a run
select ragame.id, fitness from ragame where ragame.run_id  =98 order by fitness limit 10;

-- worst games of a run
select ragame.id, fitness from ragame where ragame.run_id  =98 order by fitness desc limit 10;

-- Game count for a run
select count(*) from ragame where ragame.run_id == 16;

-- Wins per faction
select raplayer.faction, count(*) from raplayer join ragame on raplayer.game_id = ragame.id where ragame.run_id  = 98 and raplayer.winner = 1 group by raplayer.faction;


-- Select run parameter list for excel analysis
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where run_id = 95;
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where ragame.id = 16316;
select ragame.id, fitness, rules_e1_cost,rules_e1_health,rules_e1_speed,rules_e2_cost,rules_e2_health,rules_e2_speed,rules_medi_cost,rules_medi_health,rules_medi_speed,rules_1tnk_cost,rules_1tnk_health,rules_1tnk_speed,rules_3tnk_cost,rules_3tnk_health,rules_3tnk_speed,weapon_M1Carbine_reload,weapon_M1Carbine_damage,weapon_Grenade_reload,weapon_Grenade_damage,weapon_Heal_reload,weapon_25mm_reload,weapon_25mm_damage,weapon_105mm_reload,weapon_105mm_damage
from ragame
join (select raparameter.game_id, value as 'rules_e1_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_health') as s1
on ragame.id == s1.game_id
join (select raparameter.game_id, value as 'rules_e1_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_cost') as s2
on ragame.id == s2.game_id
join (select raparameter.game_id, value as 'rules_e1_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_speed') as s3
on ragame.id == s3.game_id
join (select raparameter.game_id, value as 'rules_e2_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_cost') as s4
on ragame.id == s4.game_id
join (select raparameter.game_id, value as 'rules_e2_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_health') as s5
on ragame.id == s5.game_id
join (select raparameter.game_id, value as 'rules_e2_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_speed') as s6
on ragame.id == s6.game_id
join (select raparameter.game_id, value as 'rules_medi_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_cost') as s7
on ragame.id == s7.game_id
join (select raparameter.game_id, value as 'rules_medi_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_health') as s8
on ragame.id == s8.game_id
join (select raparameter.game_id, value as 'rules_medi_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_speed') as s9
on ragame.id == s9.game_id
join (select raparameter.game_id, value as 'rules_1tnk_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_cost') as s10
on ragame.id == s10.game_id
join (select raparameter.game_id, value as 'rules_1tnk_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_health') as s11
on ragame.id == s11.game_id
join (select raparameter.game_id, value as 'rules_1tnk_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_speed') as s12
on ragame.id == s12.game_id
join (select raparameter.game_id, value as 'rules_3tnk_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_cost') as s13
on ragame.id == s13.game_id
join (select raparameter.game_id, value as 'rules_3tnk_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_health') as s14
on ragame.id == s14.game_id
join (select raparameter.game_id, value as 'rules_3tnk_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_speed') as s15
on ragame.id == s15.game_id
join (select raparameter.game_id, value as 'weapon_M1Carbine_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_M1Carbine_reload') as s16
on ragame.id == s16.game_id
join (select raparameter.game_id, value as 'weapon_M1Carbine_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_M1Carbine_damage') as s17
on ragame.id == s17.game_id
join (select raparameter.game_id, value as 'weapon_Grenade_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Grenade_reload') as s18
on ragame.id == s18.game_id
join (select raparameter.game_id, value as 'weapon_Grenade_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Grenade_damage') as s19
on ragame.id == s19.game_id
join (select raparameter.game_id, value as 'weapon_Heal_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Heal_reload') as s20
on ragame.id == s20.game_id
join (select raparameter.game_id, value as 'weapon_25mm_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_25mm_reload') as s21
on ragame.id == s21.game_id
join (select raparameter.game_id, value as 'weapon_25mm_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_25mm_damage') as s22
on ragame.id == s22.game_id
join (select raparameter.game_id, value as 'weapon_105mm_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_reload') as s23
on ragame.id == s23.game_id
join (select raparameter.game_id, value as 'weapon_105mm_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_damage') as s24
on ragame.id == s24.game_id
where ragame.id in (14212,16316,14628,17203,16706,16827,15099,15919,15987,14220);

-- Avg param value
select value, avg(fitness), count(ragame.id) from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_damage' group by value;

-- Selected individuals of a run
select id, fitness from individual where individual.age > 0 and individual.run_id = 98;


select player_name, raplayer.faction, count(raplayer.id) from raplayer join ragame on ragame.id = raplayer.game_id where ragame.run_id = 112 and winner = 1 group by raplayer.player_name;