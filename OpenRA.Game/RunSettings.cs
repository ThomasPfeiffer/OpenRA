using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public sealed class RunSettings
    {
        public static bool Headless = true;
        public static bool Autostart = true;
        public static int Max_Ticks = 200000;
    }
}
