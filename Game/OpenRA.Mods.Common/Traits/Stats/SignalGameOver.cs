using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using OpenRA.Traits;

namespace OpenRA.Mods.Common.Traits.Stats
{
    public class SignalGameOverInfo : ITraitInfo
    {
        public object Create(ActorInitializer init)
        {
            return new SignalGameOver();
        }
    }

    /** A simple callback to tell us when the game is over. */
    public class SignalGameOver : IGameOver
    {
        private const string F_PLAYER_NAME = "Player{0}Stats: ";

        public void GameOver(World world)
        {
            if (!RunSettings.Autostart) return;
            Console.WriteLine("Game Complete!");
            PrintPlayerFitnessInformation(world);

            FitnessLogging.Instance.Flush();
            // Kill process.
            System.Environment.Exit(0);
        }

        private void PrintPlayerFitnessInformation(World world)
        {
            FitnessLogging logger = FitnessLogging.Instance;
            logger.AddEntry("Ticks",world.WorldTick);
            logger.AddEntry("EndTimestamp",$"{DateTime.Now:O}");
            int i = 0;
            var players = world.Players.Where(a => !a.NonCombatant);

            int unitsKilledOverall = players.Where(p => p.PlayerActor.TraitOrDefault<PlayerStatistics>() != null)
                .Sum(p => p.PlayerActor.TraitOrDefault<PlayerStatistics>().UnitsKilled);

            int buildingsKilledOverall = players.Where(p => p.PlayerActor.TraitOrDefault<PlayerStatistics>() != null)
                .Sum(p => p.PlayerActor.TraitOrDefault<PlayerStatistics>().BuildingsKilled);

            double overallKillDeviation = 0;
            double averageKills = Convert.ToDouble(unitsKilledOverall)/players.Count();

            double overallBuildingsDeviation = 0;
            double averageBuildings = Convert.ToDouble(buildingsKilledOverall) / players.Count();

            foreach (var p in players)
            {
                var stats = p.PlayerActor.TraitOrDefault<PlayerStatistics>();
                if (stats == null)
                {
                    continue;
                }
                overallKillDeviation += Math.Abs(averageKills - Convert.ToDouble(stats.UnitsKilled));
                overallBuildingsDeviation += Math.Abs(averageBuildings - Convert.ToDouble(stats.BuildingsKilled));
                logger.AddParent(String.Format(F_PLAYER_NAME, i++));
                logger.AddEntry("PlayerName", p.PlayerName);
                logger.AddEntry("Faction", p.Faction.Name);
                logger.AddEntry("Winner", (p.WinState == WinState.Won));
                logger.AddEntry("BuildingsDead", stats.BuildingsDead);
                logger.AddEntry("BuildingsKilled", stats.BuildingsKilled);
                logger.AddEntry("DeathsCost", stats.DeathsCost);
                logger.AddEntry("KillsCost", stats.KillsCost);
                logger.AddEntry("OrderCount", stats.OrderCount);
                logger.AddEntry("UnitsDead", stats.UnitsDead);
                logger.AddEntry("UnitsKilled", stats.UnitsKilled);
                logger.EndParent();
            }
            double fitness = overallKillDeviation + overallBuildingsDeviation*5;
            logger.AddEntry("Fitness", fitness);
        }

        private void PrintPlayerFitnessInformation_alt(World world)
        {
            FitnessLogging logger = FitnessLogging.Instance;
            logger.AddEntry("Ticks", world.WorldTick);
            logger.AddEntry("EndTimestamp", $"{DateTime.Now:O}");
            int i = 0;
            var players = world.Players.Where(a => !a.NonCombatant);

            int fitness = 0;
            foreach (var p in players)
            {
                var stats = p.PlayerActor.TraitOrDefault<PlayerStatistics>();
                if (stats == null)
                {
                    continue;
                }
                fitness += Math.Abs(70 - stats.UnitsKilled);
                fitness += Math.Abs(10 - stats.BuildingsKilled);
                logger.AddParent(String.Format(F_PLAYER_NAME, i++));
                logger.AddEntry("PlayerName", p.PlayerName);
                logger.AddEntry("Faction", p.Faction.Name);
                logger.AddEntry("Winner", (p.WinState == WinState.Won));
                logger.AddEntry("BuildingsDead", stats.BuildingsDead);
                logger.AddEntry("BuildingsKilled", stats.BuildingsKilled);
                logger.AddEntry("DeathsCost", stats.DeathsCost);
                logger.AddEntry("KillsCost", stats.KillsCost);
                logger.AddEntry("OrderCount", stats.OrderCount);
                logger.AddEntry("UnitsDead", stats.UnitsDead);
                logger.AddEntry("UnitsKilled", stats.UnitsKilled);
                logger.EndParent();
            }
            logger.AddEntry("Fitness", fitness);
        }


    }
}
