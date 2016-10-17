﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenRA.Traits;

namespace OpenRA.Mods.Common.Traits.Esu
{
    public class SignalGameOverInfo : ITraitInfo
    {
        public object Create(ActorInitializer init)
        {
            Log.AddChannel("end_game_fitness", "end_game_fitness.log");
            return new SignalGameOver();
        }
    }

    /** A simple callback to tell us when the game is over. */
    public class SignalGameOver : IGameOver
    {
        private const string FORMAT_STRING = "{0,-30} | {1,-30} | {2,-30} | {3, -30} | {4, -30}\n";

        public void GameOver(World world)
        {
            if (!RunSettings.Headless) return;
            Console.WriteLine("Game Complete!");
            PrintPlayerFitnessInformation(world);

            // Kill process.
            System.Environment.Exit(0);
        }

        private void PrintPlayerFitnessInformation(World world)
        {
            PrintToConsoleAndLog(String.Format(FORMAT_STRING, "PLAYER NAME", "KILL COST", "UNITS KILLED", "DEATH COST" , "UNITS DIED"));

            foreach (var p in world.Players.Where(a => !a.NonCombatant))
            {
                var stats = p.PlayerActor.TraitOrDefault<PlayerStatistics>();
                if (stats == null)
                {
                    continue;
                }
                
                PrintToConsoleAndLog(String.Format(FORMAT_STRING, p.PlayerName, stats.KillsCost, stats.UnitsKilled, stats.DeathsCost, stats.UnitsDead));
            }
        }

        private void PrintToConsoleAndLog(string message)
        {
            Console.WriteLine(message);
            Log.Write("end_game_fitness", message);
        }
    }
}
