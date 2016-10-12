using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public sealed class RunSettings
    {
        public static bool Headless = false;
        public static bool Autostart = false;
        public static int Max_Ticks = 200000;
        public static string Default_Mod = "";
    }
}
