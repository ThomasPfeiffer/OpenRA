using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public sealed class RunSettings
    {
        public const bool Headless = false;
        public const bool Autostart = true;
        public const int Max_Ticks = 200000;
        public const int Timestep = 40; // Default 40
        public const string Default_Mod = "";
        public const string Default_Map = "ma_temperat";
        public const string AI = "Naval AI";

    }
}
