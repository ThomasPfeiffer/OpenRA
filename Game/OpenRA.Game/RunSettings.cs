using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public sealed class RunSettings
    {
        public const bool Headless = true;
        public const bool Autostart = true;
        public const int Max_Ticks = 100000;
        public const int Timestep = 1; // Default 40
        public const string Default_Mod = "ra";
        public const string Default_Map = ""; // ma_temperat
        public static List<Tuple<string,string>> AI_LIST = new List<Tuple<string, string>>
        {
            Tuple.Create("Rush AI", "england"),
            Tuple.Create("Rush AI", "ukraine"),
        };


        public static string FitnessLog = "C:\\temp\\log.log";
        public static string Game_ID = "";

    }
}
