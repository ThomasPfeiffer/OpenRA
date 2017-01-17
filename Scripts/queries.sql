-- average buildings destroyed
select avg(buildings_killed) from raplayer;

-- Game Duration
select ((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id == 86;

-- Avg Game Duration
select ragame.run_id, ticks, avg((julianday(ragame.end_timestamp) - julianday(ragame.start_timestamp)) * 86400.0) as duration from ragame where ragame.run_id == 98;

-- Run Duration
select run.id, ((julianday(run.end_timestamp) - julianday(run.start_timestamp)) * 86400.0) as duration from run where run.id == 98;

-- Number of games per run
select ragame.run_id, count(*) from ragame group by ragame.run_id;

select name, value, run_id,max_ticks_reached, fitness, raparameter.game_id  from raparameter join ragame, run where ragame.id == raparameter.game_id and run.id == ragame.run_id and run.id == 1;

-- fitness list for a run
select ragame.id,ragame.game_id, fitness from ragame where ragame.run_id =155;

-- best game of a run
select ragame.id, min(fitness) from ragame where ragame.run_id  =95;

-- best games of a run
select ragame.id, fitness from ragame where ragame.run_id  =128 order by fitness limit 10;

-- worst games of a run
select ragame.id, fitness from ragame where ragame.run_id  =98 order by fitness desc limit 10;

-- Game count for a run
select count(*) from ragame where ragame.run_id == 98;

-- Wins per faction
select raplayer.faction, count(*) from raplayer join ragame on raplayer.game_id = ragame.id where ragame.run_id  = 138 and raplayer.winner = 1 group by raplayer.faction;


-- Select run parameter list for excel analysis
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where run_id = 95;
select ragame.game_id, fitness, name, value from raparameter join ragame on ragame.id = raparameter.game_id where ragame.id = 16316;
select ragame.id, fitness, rules_e1_cost,rules_e1_health,rules_e1_speed,rules_e2_cost,rules_e2_health,rules_e2_speed,rules_medi_cost,rules_medi_health,rules_medi_speed,rules_1tnk_cost,rules_1tnk_health,rules_1tnk_speed,rules_3tnk_cost,rules_3tnk_health,rules_3tnk_speed,weapon_M1Carbine_reload,weapon_M1Carbine_damage,weapon_Grenade_reload,weapon_Grenade_damage,weapon_Heal_reload,weapon_25mm_reload,weapon_25mm_damage,weapon_105mm_reload,weapon_105mm_damage
from ragame
left join (select raparameter.game_id, value as 'rules_e1_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_health') as s1
on ragame.id == s1.game_id
left join (select raparameter.game_id, value as 'rules_e1_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_cost') as s2
on ragame.id == s2.game_id
left join (select raparameter.game_id, value as 'rules_e1_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e1_speed') as s3
on ragame.id == s3.game_id
left join (select raparameter.game_id, value as 'rules_e2_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_cost') as s4
on ragame.id == s4.game_id
left join (select raparameter.game_id, value as 'rules_e2_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_health') as s5
on ragame.id == s5.game_id
left join (select raparameter.game_id, value as 'rules_e2_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_e2_speed') as s6
on ragame.id == s6.game_id
left join (select raparameter.game_id, value as 'rules_medi_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_cost') as s7
on ragame.id == s7.game_id
left join (select raparameter.game_id, value as 'rules_medi_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_health') as s8
on ragame.id == s8.game_id
left join (select raparameter.game_id, value as 'rules_medi_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_medi_speed') as s9
on ragame.id == s9.game_id
left join (select raparameter.game_id, value as 'rules_1tnk_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_cost') as s10
on ragame.id == s10.game_id
left join (select raparameter.game_id, value as 'rules_1tnk_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_health') as s11
on ragame.id == s11.game_id
left join (select raparameter.game_id, value as 'rules_1tnk_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_1tnk_speed') as s12
on ragame.id == s12.game_id
left join (select raparameter.game_id, value as 'rules_3tnk_cost' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_cost') as s13
on ragame.id == s13.game_id
left join (select raparameter.game_id, value as 'rules_3tnk_health' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_health') as s14
on ragame.id == s14.game_id
left join (select raparameter.game_id, value as 'rules_3tnk_speed' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'rules_3tnk_speed') as s15
on ragame.id == s15.game_id
left join (select raparameter.game_id, value as 'weapon_M1Carbine_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_M1Carbine_reload') as s16
on ragame.id == s16.game_id
left join (select raparameter.game_id, value as 'weapon_M1Carbine_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_M1Carbine_damage') as s17
on ragame.id == s17.game_id
left join (select raparameter.game_id, value as 'weapon_Grenade_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Grenade_reload') as s18
on ragame.id == s18.game_id
left join (select raparameter.game_id, value as 'weapon_Grenade_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Grenade_damage') as s19
on ragame.id == s19.game_id
left join (select raparameter.game_id, value as 'weapon_Heal_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_Heal_reload') as s20
on ragame.id == s20.game_id
left join (select raparameter.game_id, value as 'weapon_25mm_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_25mm_reload') as s21
on ragame.id == s21.game_id
left join (select raparameter.game_id, value as 'weapon_25mm_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_25mm_damage') as s22
on ragame.id == s22.game_id
left join (select raparameter.game_id, value as 'weapon_105mm_reload' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_reload') as s23
on ragame.id == s23.game_id
left join (select raparameter.game_id, value as 'weapon_105mm_damage' from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_damage') as s24
on ragame.id == s24.game_id
where ragame.run_id = 138;

-- Avg param value
select value, avg(fitness), count(ragame.id) from raparameter join ragame on ragame.id = raparameter.game_id where raparameter.name like 'weapon_105mm_damage' group by value;

-- Selected individuals of a run
select fitness, age from individual where individual.age > 0 and individual.run_id = 98;

-- best individuals of a run
select id, fitness from individual where individual.run_id = 98 order by fitness limit 200;

select player_name, raplayer.faction, count(raplayer.id) from raplayer join ragame on ragame.id = raplayer.game_id where ragame.run_id = 112 and winner = 1 group by raplayer.player_name;


-- Individual parameters for excel 
select individual.id, fitness, rules_e1_cost,rules_e1_health,rules_e1_speed,rules_e2_cost,rules_e2_health,rules_e2_speed,rules_medi_cost,rules_medi_health,rules_medi_speed,rules_1tnk_cost,rules_1tnk_health,rules_1tnk_speed,rules_3tnk_cost,rules_3tnk_health,rules_3tnk_speed,weapon_M1Carbine_reload,weapon_M1Carbine_damage,weapon_Grenade_reload,weapon_Grenade_damage,weapon_Heal_reload,weapon_25mm_reload,weapon_25mm_damage,weapon_105mm_reload,weapon_105mm_damage
from individual
left join (select individualparameter.individual_id, value as 'rules_e1_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e1_health') as s1
on individual.id == s1.individual_id
left join (select individualparameter.individual_id, value as 'rules_e1_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e1_cost') as s2
on individual.id == s2.individual_id
left join (select individualparameter.individual_id, value as 'rules_e1_speed' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e1_speed') as s3
on individual.id == s3.individual_id
left join (select individualparameter.individual_id, value as 'rules_e2_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e2_cost') as s4
on individual.id == s4.individual_id
left join (select individualparameter.individual_id, value as 'rules_e2_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e2_health') as s5
on individual.id == s5.individual_id
left join (select individualparameter.individual_id, value as 'rules_e2_speed' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_e2_speed') as s6
on individual.id == s6.individual_id
left join (select individualparameter.individual_id, value as 'rules_medi_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_medi_cost') as s7
on individual.id == s7.individual_id
left join (select individualparameter.individual_id, value as 'rules_medi_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_medi_health') as s8
on individual.id == s8.individual_id
left join (select individualparameter.individual_id, value as 'rules_medi_speed' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_medi_speed') as s9
on individual.id == s9.individual_id
left join (select individualparameter.individual_id, value as 'rules_1tnk_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_1tnk_cost') as s10
on individual.id == s10.individual_id
left join (select individualparameter.individual_id, value as 'rules_1tnk_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_1tnk_health') as s11
on individual.id == s11.individual_id
left join (select individualparameter.individual_id, value as 'rules_1tnk_speed' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_1tnk_speed') as s12
on individual.id == s12.individual_id
left join (select individualparameter.individual_id, value as 'rules_3tnk_cost' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_3tnk_cost') as s13
on individual.id == s13.individual_id
left join (select individualparameter.individual_id, value as 'rules_3tnk_health' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_3tnk_health') as s14
on individual.id == s14.individual_id
left join (select individualparameter.individual_id, value as 'rules_3tnk_speed' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'rules_3tnk_speed') as s15
on individual.id == s15.individual_id
left join (select individualparameter.individual_id, value as 'weapon_M1Carbine_reload' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_M1Carbine_reload') as s16
on individual.id == s16.individual_id
left join (select individualparameter.individual_id, value as 'weapon_M1Carbine_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_M1Carbine_damage') as s17
on individual.id == s17.individual_id
left join (select individualparameter.individual_id, value as 'weapon_Grenade_reload' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_Grenade_reload') as s18
on individual.id == s18.individual_id
left join (select individualparameter.individual_id, value as 'weapon_Grenade_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_Grenade_damage') as s19
on individual.id == s19.individual_id
left join (select individualparameter.individual_id, value as 'weapon_Heal_reload' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_Heal_reload') as s20
on individual.id == s20.individual_id
left join (select individualparameter.individual_id, value as 'weapon_25mm_reload' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_25mm_reload') as s21
on individual.id == s21.individual_id
left join (select individualparameter.individual_id, value as 'weapon_25mm_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_25mm_damage') as s22
on individual.id == s22.individual_id
left join (select individualparameter.individual_id, value as 'weapon_105mm_reload' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_105mm_reload') as s23
on individual.id == s23.individual_id
left join (select individualparameter.individual_id, value as 'weapon_105mm_damage' from individualparameter join individual on individual.id = individualparameter.individual_id where individualparameter.name like 'weapon_105mm_damage') as s24
on individual.id == s24.individual_id
where individual.id in (3446, 3451, 3257, 3283, 3388, 3438, 3557, 3296, 3309, 3310);