﻿using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Dynamic;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public sealed class RunSettings
    {
        public static int Timestep = 40; // Default 40
        public const string Default_Mod = "ra";

        public static bool Headless = false;
        public static bool Autostart = false;
        public static int MaxTicks = 400000;
        public static string GameMap; // ma_temperat
        public static string FitnessLog;
        public static string Game_ID;
        public static List<Tuple<string,string>> AI_LIST;

        public static void ReadArgs(Arguments args)
        {
            Headless = bool.Parse(args.GetValue("--headless","false"));
            Autostart = bool.Parse(args.GetValue("--autostart", "false"));
            MaxTicks = int.Parse(args.GetValue("--max-ticks", "100000"));
            GameMap = args.GetValue("--map", "ma_temperat");
            FitnessLog = args.GetValue("--fitness-log", "");
            Game_ID = args.GetValue("--game-id", "no_id_set");
            Timestep = int.Parse(args.GetValue("--timestep", "40"));
            AI_LIST = new List<Tuple<string, string>>
            {
                Tuple.Create(args.GetValue("--ai1", "Rush AI"), args.GetValue("--ai1-faction", "england")),
                Tuple.Create(args.GetValue("--ai2", "Rush AI"), args.GetValue("--ai2-faction", "ukraine")),
            };
        }
    }
    
}
