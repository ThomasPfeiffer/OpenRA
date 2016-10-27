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
        private const string F_STAT = "\t{0}: {1}";

        public void GameOver(World world)
        {
            if (!RunSettings.Autostart) return;
            Console.WriteLine("Game Complete!");
            PrintPlayerFitnessInformation(world);

            // Kill process.
            System.Environment.Exit(0);
        }

        private void PrintPlayerFitnessInformation(World world)
        {
            FitnessLogging logger = FitnessLogging.Instance;
            logger.LogLine($"Ticks:  + {world.WorldTick}");
            logger.LogLine("EndTimestamp: " + $"{DateTime.Now:O}");
            int i = 0;
            foreach (var p in world.Players.Where(a => !a.NonCombatant))
            {
                var stats = p.PlayerActor.TraitOrDefault<PlayerStatistics>();
                if (stats == null)
                {
                    continue;
                }
                logger.LogLine(String.Format(F_PLAYER_NAME, i++));
                logger.LogLine(String.Format(F_STAT, "PlayerName", p.PlayerName));
                logger.LogLine(String.Format(F_STAT, "Faction", p.Faction.Name));
                logger.LogLine(String.Format(F_STAT, "Winner", (p.WinState == WinState.Won)));
                logger.LogLine(String.Format(F_STAT, "BuildingsDead", stats.BuildingsDead));
                logger.LogLine(String.Format(F_STAT, "BuildingsKilled", stats.BuildingsKilled));
                logger.LogLine(String.Format(F_STAT, "DeathsCost", stats.DeathsCost));
                logger.LogLine(String.Format(F_STAT, "KillsCost", stats.KillsCost));
                logger.LogLine(String.Format(F_STAT, "OrderCount", stats.OrderCount));
                logger.LogLine(String.Format(F_STAT, "UnitsDead", stats.UnitsDead));
                logger.LogLine(String.Format(F_STAT, "UnitsKilled", stats.UnitsKilled));
            }
        }

        
    }
}
