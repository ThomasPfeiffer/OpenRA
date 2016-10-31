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

            // Kill process.
            System.Environment.Exit(0);
        }

        private void PrintPlayerFitnessInformation(World world)
        {
            FitnessLogging logger = FitnessLogging.Instance;
            logger.AddEntry("Ticks",world.WorldTick);
            logger.AddEntry("EndTimestamp",$"{DateTime.Now:O}");
            int i = 0;
            int fitness = 0;
            foreach (var p in world.Players.Where(a => !a.NonCombatant))
            {
                var stats = p.PlayerActor.TraitOrDefault<PlayerStatistics>();
                if (stats == null)
                {
                    continue;
                }
                fitness += stats.UnitsKilled;
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
            logger.AddEntry("Fitness",fitness);
        }

        
    }
}
