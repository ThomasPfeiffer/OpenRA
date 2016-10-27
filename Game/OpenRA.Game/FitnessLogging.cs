using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public class FitnessLogging
    {
        private string logFile;

        private static readonly FitnessLogging instance = new FitnessLogging();

        private FitnessLogging()
        {
            if (!string.IsNullOrEmpty(RunSettings.FitnessLog))
            {
                logFile = RunSettings.FitnessLog;
                LogLine($"# Log Started at {DateTime.Now:s}");
            }
        }

        public static FitnessLogging Instance
        {
            get
            {
                return instance;
            }
        }

        public void LogLine(string message)
        {
            Console.WriteLine(message);
            if (!string.IsNullOrEmpty(logFile))
            {
                using (StreamWriter log = File.AppendText(logFile))
                {
                    if (log != null)
                    {
                        log.WriteLine(message);
                    }
                }
            }
        }
    }
}
