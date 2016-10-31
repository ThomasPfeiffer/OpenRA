using System;
using System.Collections.Generic;
using System.Drawing.Drawing2D;
using System.IO;
using System.Linq;
using System.Text;

namespace OpenRA
{
    public class FitnessLogging
    {
        private string logFile;
        private int indent;

        private static readonly FitnessLogging instance = new FitnessLogging();

        private FitnessLogging()
        {
            if (!string.IsNullOrEmpty(RunSettings.FitnessLog))
            {
                indent = 0;
                logFile = RunSettings.FitnessLog;
                AddParent($"Game{RunSettings.Game_ID}");
            }
        }

        public static FitnessLogging Instance
        {
            get
            {
                return instance;
            }
        }

        private string addIndent(string msg)
        {
            for (int i = 0; i < indent; i++)
            {
                msg = "\t" + msg;
            }
            return msg;
        }

        public void AddComment(string comment)
        {
            string line = addIndent(comment);
            Write(line);
        }

        public void AddEntry(string name, object value)
        {
            string line = addIndent($"{name}: {value}");
            Write(line);
        }

        public void AddParent(string name)
        {
            string line = addIndent($"{name}:");
            Write(line);
            indent++;
        }

        public void EndParent()
        {
            indent--;
        }

        private void Write(string line)
        {
            if (!string.IsNullOrEmpty(logFile))
            {
                using (StreamWriter log = File.AppendText(logFile))
                {
                    log.WriteLine(line);
                }
            }
        }
    }
}
